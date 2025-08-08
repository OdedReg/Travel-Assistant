from datetime import datetime

from google import genai
from google.genai import types

from src.travel_tools import get_destination_weather, get_currency_exchange, get_local_attractions_opentripmap
from utils import get_env_variable, get_all_currency_codes

# Configure the client
client = genai.Client(api_key=get_env_variable("GOOGLE_API_KEY"))


system_prompt = f"""
You are a Travel Assistant tasked with answering user questions with effective answers that feel natural and helpful.

You are provided with multiple tools to help you answer the user questions. Beside of them ,you can add your own knowledge to the answer.
If you dont find any of the tools relevant, try to answer using your own knowledge.

Today is {datetime.now()}. 
Currency codes: {get_all_currency_codes()}

Answer with concise and relevant responses.
"""

user_prompt = "what are the most famous waters parks near tel aviv?"

config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=[get_local_attractions_opentripmap, get_destination_weather, get_currency_exchange]
)

# Make the request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=config,
    contents=user_prompt,
)
print(response)
print("-"*50)
print(response.text)
