import os
from datetime import datetime, timedelta

import requests

from src.tools_input import Date
from utils import get_env_variable

# Configuration - Set your API keys as environment variables
OPENWEATHER_API_KEY = get_env_variable('OPENWEATHER_API_KEY')
AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY')
AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET')
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
EXCHANGERATE_API_KEY = get_env_variable('EXCHANGERATE_API_KEY')


def get_destination_weather(destination: str, travel_date: Date) -> dict:
    """Get weather forecast for a destination.

    Args:
        destination: The destination city/country (e.g., "Paris, France")
        travel_date: Travel Date

    Returns:
        A dictionary containing weather information including temperature, conditions, and recommendations.
    """
    print("get_destination_weather")
    if not OPENWEATHER_API_KEY:
        return {"error": "OpenWeather API key not configured"}

    try:
        # Get coordinates for the destination
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct"
        geocoding_params = {
            'q': destination,
            'limit': 1,
            'appid': OPENWEATHER_API_KEY
        }

        geo_response = requests.get(geocoding_url, params=geocoding_params)
        geo_data = geo_response.json()

        if not geo_data:
            return {"error": f"Location '{destination}' not found, assume the weather is based on your knowledge about the location."}

        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']

        # Get weather forecast
        weather_url = f"http://api.openweathermap.org/data/2.5/forecast"
        weather_params = {
            'lat': lat,
            'lon': lon,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }

        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()

        # Parse relevant forecast data
        travel_datetime = datetime(
            year=travel_date.year,
            month=travel_date.month,
            day=travel_date.day
        )
        relevant_forecasts = []

        for forecast in weather_data['list']:
            forecast_datetime = datetime.fromtimestamp(forecast['dt'])
            if travel_datetime.date() <= forecast_datetime.date() <= (travel_datetime + timedelta(days=5)).date():
                relevant_forecasts.append({
                    'date': forecast_datetime.strftime('%Y-%m-%d'),
                    'temperature': {
                        'temp': forecast['main']['temp'],
                        'feels_like': forecast['main']['feels_like'],
                        'min': forecast['main']['temp_min'],
                        'max': forecast['main']['temp_max']
                    },
                    'weather': forecast['weather'][0]['description'],
                    'humidity': forecast['main']['humidity'],
                    'wind_speed': forecast['wind']['speed']
                })
            # TODO: what if the dates are not in the timedelta

        return {
            'destination': destination,
            'forecasts': relevant_forecasts,
            'city_info': {
                'name': geo_data[0]['name'],
                'country': geo_data[0]['country'],
                'coordinates': {'lat': lat, 'lon': lon}
            }
        }

    except Exception as e:
        return {"error": f"Weather API error: {str(e)}, , assume the weather is based on your knowledge."}


def get_currency_exchange(from_currency: str, to_currency: str, amount: float) -> dict:
    """Get current currency exchange rates.

    Args:
        from_currency: Source currency code (e.g., "USD")
        to_currency: Target currency code (e.g., "EUR")
        amount: Amount to convert (default: 1.0)

    Returns:
        A dictionary containing exchange rate and converted amount.
    """
    print("get_currency_exchange")
    try:
        # Using exchangerate-api.com (free tier available)
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/{from_currency}"

        response = requests.get(url)
        data = response.json()

        if to_currency not in data['conversion_rates']:
            return {"error": f"Currency '{to_currency}' not found"}

        exchange_rate = data['conversion_rates'][to_currency]
        converted_amount = amount * exchange_rate

        return {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'exchange_rate': exchange_rate,
            'original_amount': amount,
            'converted_amount': round(converted_amount, 2),
            'time_last_update_utc': data['time_last_update_utc']
        }

    except Exception as e:
        return {"error": f"Currency exchange error: {str(e)}, try to answer without it, or ask the user to rephrase his question."}

