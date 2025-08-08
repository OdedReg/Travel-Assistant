import os
from typing import Any

import requests
from dotenv import load_dotenv


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
    print("get_all_currency_codes")
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