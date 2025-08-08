from google import genai
from google.genai import types

from src.constants import system_prompt
from src.travel_tools import get_destination_weather_forecast, get_currency_exchange, get_local_attractions_opentripmap
from utils import get_env_variable

client = genai.Client(api_key=get_env_variable("GOOGLE_API_KEY"))


class ConversationManager:
    def __init__(self, max_history=10):
        self.max_history = max_history  # Limit conversation history to prevent token overflow

    def build_conversation_history(self, chatbot):
        """
        Convert Gradio chatbot format to Gemini conversation format
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


# Initialize conversation manager
conv_manager = ConversationManager()

config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=[get_local_attractions_opentripmap, get_destination_weather_forecast, get_currency_exchange]
)


def chat_with_agent(chatbot):
    """
    Stream the response from Gemini API to the chatbot with conversation memory
    """
    try:
        # Build conversation history
        conversation_history = conv_manager.build_conversation_history(chatbot)

        # Make the streaming request with conversation history
        response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            config=config,
            contents=conversation_history,
        )

        # Initialize the response text
        full_response = ""

        # Stream the response
        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                # Update the last message in chatbot with the accumulated response
                if chatbot:
                    chatbot[-1] = [chatbot[-1][0], full_response]  # Properly update the tuple
                    yield chatbot

    except Exception as e:
        error_message = f"Sorry, I encountered an error: {str(e)}"
        if chatbot:
            chatbot[-1] = [chatbot[-1][0], error_message]  # Properly update the tuple
        yield chatbot