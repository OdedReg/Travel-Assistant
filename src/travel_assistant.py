import json
from typing import List, Dict, Generator, Tuple

from google.genai import types

from src.constants import VERIFIER_MODEL, TRAVELER_MODEL
from src.prompts.prompts import corrected_traveler_system_prompt, travel_system_prompt, verifier_system_prompt
from src.prompts.schemas import VERIFICATION_SCHEMA
from src.travel_tools import get_destination_weather_forecast, get_currency_exchange, get_local_attractions_opentripmap
from src.utils.utils import get_genai_client, generate_streaming_response


class ConversationManager:
    def __init__(self, max_history=10):
        self.max_history = max_history  # Limit conversation history to prevent token overflow
        self.client = get_genai_client()

    def build_conversation_history(self, chatbot: List[List[str]]) -> List:
        """
        Convert the Gradio chatbot format to the Gemini conversation format.

        Args:
            chatbot (List[List[str]]): The current chat history.

        Returns:
            List: A list of dictionaries representing the conversation history in Gemini format.
        """
        conversation = []

        # Get recent conversation history (limit to max_history exchanges)
        recent_chatbot = chatbot[-self.max_history:] if len(chatbot) > self.max_history else chatbot

        for user_msg, assistant_msg in recent_chatbot[:-1]:  # Exclude current incomplete exchange
            if user_msg:
                conversation.append({
                    "role": "user",
                    "parts": [{"text": user_msg}]
                })
            if assistant_msg:  # Only add if assistant_msg is not None or empty
                conversation.append({
                    "role": "model",
                    "parts": [{"text": assistant_msg}]
                })

        # Add the current user message
        if chatbot and chatbot[-1][0]:
            conversation.append({
                "role": "user",
                "parts": [{"text": chatbot[-1][0]}]
            })

        return conversation

    def verify(self, chatbot: List[List[str]], conversation_history: List) -> Generator[List[List[str]], None, None]:
        """
        Verify the last response in the conversation for accuracy using the Gemini 2.5 Pro model.

        Args:
            chatbot (List[List[str]]): The current chat history.
            conversation_history (List): The entire conversation history to use as context.

        Yields:
            List[List[str]]: Updated chatbot history with corrections if necessary.
        """
        if chatbot:
            # Get current conversation for verification (no UI indication)
            conversation_for_verification = []
            for user_msg, bot_msg in chatbot:
                if user_msg and bot_msg:
                    conversation_for_verification.append((user_msg, bot_msg))

            # Verify silently in background
            verification = self.verify_response(conversation_for_verification)

            if verification["needs_correction"]:
                # Replace with error message and start regeneration
                error_message = "I apologize, but my response contained inaccurate information. Let me provide you with a corrected answer..."
                chatbot[-1] = [chatbot[-1][0], error_message]
                yield chatbot

                # Regenerate with feedback (silently)
                formatted_corrected_traveler_system_prompt = corrected_traveler_system_prompt.format(
                    travel_system_prompt=travel_system_prompt, feedback=verification['feedback'])
                regenerate_config = types.GenerateContentConfig(
                    system_instruction=formatted_corrected_traveler_system_prompt,
                    tools=[get_local_attractions_opentripmap, get_destination_weather_forecast, get_currency_exchange]
                )
                for chatbot in generate_streaming_response(self.client, chatbot, TRAVELER_MODEL, regenerate_config,
                                                           conversation_history):
                    yield chatbot

    def verify_response(self, conversation_history: List[Tuple[str, str]]) -> Dict[str, str]:
        """
        Verify ONLY the last response in the conversation using Gemini 2.5 Pro.

        Args:
            conversation_history (List): The entire conversation history.

        Returns:
            dict: A dictionary containing feedback and whether a correction is needed.
        """
        try:
            # Build context for verification - full conversation for context
            context = "FULL CONVERSATION FOR CONTEXT:\n\n"
            for i, (user_msg, bot_msg) in enumerate(conversation_history[:-1]):  # All except last
                if user_msg:
                    context += f"User {i + 1}: {user_msg}\n"
                if bot_msg:
                    context += f"Assistant {i + 1}: {bot_msg}\n"
                context += "\n"

            # Highlight the last exchange that needs verification
            if conversation_history:
                last_user, last_bot = conversation_history[-1]
                context += "=" * 50 + "\n"
                context += "LAST EXCHANGE TO VERIFY:\n"
                context += "=" * 50 + "\n"
                if last_user:
                    context += f"User: {last_user}\n"
                if last_bot:
                    context += f"Assistant: {last_bot}\n"
                context += "=" * 50 + "\n"

            context += "\nPlease analyze ONLY the last assistant response above for accuracy and appropriateness, using the full conversation as context."
            verification_config = types.GenerateContentConfig(
                system_instruction=verifier_system_prompt,
                response_mime_type="application/json",
                response_schema=VERIFICATION_SCHEMA
            )

            # Get verification from Gemini 2.5 Pro
            verification_response = self.client.models.generate_content(
                model=VERIFIER_MODEL,
                config=verification_config,
                contents=context
            )
            # Parse the JSON response
            verification_result = json.loads(verification_response.text)
            return verification_result

        except Exception as e:
            # Return safe default on error
            return {
                "needs_correction": False,
                "feedback": f"Verification failed: {str(e)}"
            }


conv_manager = ConversationManager()


def chat_with_agent(chatbot: List[List[str]]) -> Generator[List[List[str]], None, None]:
    """
    Stream the response from Gemini API with proper handling of function calls and thoughts.

    Args:
        chatbot (List[List[str]]): The current chat history.

    Yields:
        List[List[str]]: Updated chatbot history with responses from the agent.
    """
    # Build conversation history
    conversation_history = conv_manager.build_conversation_history(chatbot)
    config = types.GenerateContentConfig(
        system_instruction=travel_system_prompt,
        tools=[get_local_attractions_opentripmap, get_destination_weather_forecast, get_currency_exchange]
    )

    for chatbot in generate_streaming_response(conv_manager.client, chatbot, TRAVELER_MODEL, config,
                                               conversation_history):
        yield chatbot

    for chatbot in conv_manager.verify(chatbot, conversation_history):
        yield chatbot
