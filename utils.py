import os
from typing import Any, List

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import Client
from google.genai.types import GenerateContentConfig


def get_env_variable(var_name: str) -> Any:
    """
    Retrieves an environment variable and returns its value.

    Args:
        var_name (str): The name of the environment variable to retrieve.

    Returns:
        Any: The value of the environment variable.
    """
    load_dotenv()
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not found.")
    return value

def get_all_currency_codes() -> dict:
    """Get all supported currency codes from ExchangeRate-API.com.

    Returns:
        A dictionary containing a list of supported currency codes, or an error message.
    """
    url = f"https://v6.exchangerate-api.com/v6/{get_env_variable('EXCHANGERATE_API_KEY')}/codes"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("result") == "success":
            supported_codes_with_names = data["supported_codes"]
            # The API returns a list of lists, e.g., [['USD', 'US Dollar'], ...]
            return {"supported_codes": supported_codes_with_names}
        else:
            return {"error": data.get("error-type", "Unknown error.")}

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred during the API request: {str(e)}."}

def get_genai_client() -> genai.Client:
    return genai.Client(api_key=get_env_variable("GOOGLE_API_KEY"))


def generate_streaming_response(client: Client, chatbot: List,  model_name: str, config: GenerateContentConfig, contents: List):
    """
    Generate a streaming response from a specified model, updating the conversation incrementally.

    Args:
        client (Client): The client to use.
        model_name (str): The name of the model to use (e.g., "gemini-2.5-flash").
        config (dict): Configuration for the model.
        contents (str): The contents of the conversation to pass to the model.

    Yields:
        chatbot: Updated chatbot responses incrementally.
    """
    response = client.models.generate_content_stream(
        model=model_name,
        config=config,
        contents=contents,
    )

    full_response = ""
    for chunk in response:
        chunk_text = ""

        # Handle the response structure properly
        if hasattr(chunk, 'candidates') and chunk.candidates:
            candidate = chunk.candidates[0]
            if hasattr(candidate, 'content') and candidate.content:
                for part in candidate.content.parts:
                    if hasattr(part, 'text') and part.text:
                        # Regular text content
                        chunk_text += part.text

        # Fallback for simple text responses
        elif hasattr(chunk, 'text'):
            chunk_text = chunk.text

        # Update response if we got new text
        if chunk_text:
            full_response += chunk_text
            if chatbot:
                chatbot[-1] = [chatbot[-1][0], full_response]
                yield chatbot