from datetime import datetime

from google import genai
from google.genai import types

from src.travel_tools import get_destination_weather_forecast, get_currency_exchange, get_local_attractions_opentripmap
from utils import get_env_variable, get_all_currency_codes

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
            if assistant_msg:
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

system_prompt = f"""
You are a Travel Assistant tasked with answering user questions with effective answers that feel natural and helpful.

You are provided with multiple tools to help you answer the user questions. Beside of them, you can add your own knowledge to the answer.
If you don't find any of the tools relevant, try to answer using your own knowledge.

You have access to conversation history, so you can refer to previous messages and maintain context throughout the conversation.
Feel free to reference previous questions or build upon earlier topics when relevant.

Today is {datetime.now()}. 
Currency codes: {get_all_currency_codes()}

Answer with concise and relevant responses.
"""

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

        print(f"Conversation history length: {len(conversation_history)} messages")  # Debug info
        x  = client.models.generate_content(
            model="gemini-2.5-flash",
            config=config,
            contents=conversation_history,
        )
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
                    chatbot[-1][1] = full_response
                    yield chatbot

    except Exception as e:
        error_message = f"Sorry, I encountered an error: {str(e)}"
        print(f"Error in chat_with_agent: {e}")  # Debug info
        if chatbot:
            chatbot[-1][1] = error_message
        yield chatbot
