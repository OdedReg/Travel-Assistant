import os
from datetime import datetime, timedelta

import requests

from src.constants import NOT_FOUND_ERROR_INSTRUCTION
from src.tools_input import Date
from utils import get_env_variable

OPENWEATHER_API_KEY = get_env_variable('OPENWEATHER_API_KEY')
AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY')
AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET')
OPEN_TRIP_MAP_API_KEY = get_env_variable('OPEN_TRIP_MAP_API_KEY')
EXCHANGERATE_API_KEY = get_env_variable('EXCHANGERATE_API_KEY')

def get_local_attractions_opentripmap(destination: str, kind: str, radius: int = 10000, limit: int = 5) -> dict:
    f"""
     Retrieve top-rated local attractions near a given destination using the OpenTripMap API.

     Args:
         destination (str): The name of the city or location to search around (e.g., "Rome", "Tokyo").
         kind (str):  attraction type to filter by. Allowed values: [
    "natural",
    "beaches",
    "waterfalls",
    "nature_reserves",
    "volcanoes",
    "caves",
    "mountain_peaks",
    "museums",
    "art_galleries",
    "theatres_and_entertainments",
    "sculptures",
    "gardens_and_parks",
    "aquariums",
    "zoos",
    "castles",
    "historic_districts",
    "monuments",
    "archaeology",
    "pyramids",
    "battlefields",
    "churches",
    "mosques",
    "synagogues",
    "hindu_temples",
    "monasteries",
    "towers",
    "bridges",
    "lighthouses",
    "skyscrapers",
    "palaces",
    "amusement_parks",
    "water_parks",
    "cinemas",
    "nightclubs",
    "view_points",
    "sundials",
    "unclassified_objects"
    ].
         radius (int, optional): The search radius in meters. Default is 10,000 (10 km).
         limit (int, optional): The maximum number of attractions to return. Default is 5.

     Returns:
         dict: A dictionary containing:
             - 'attractions': A list of dictionaries, each containing:
                 - 'name': Name of the attraction
                 - 'kind': Types/categories
                 - 'description': Short Wikipedia-style summary (if available)
                 - 'url': Link to a Wikipedia article (if available)
     """
    print("get_local_attractions_opentripmap")
    try:
        # Step 1: Get coordinates of the destination
        geocode_url = f"https://api.opentripmap.com/0.1/en/places/geoname"
        geocode_params = {'name': destination, 'apikey': OPEN_TRIP_MAP_API_KEY}
        geo_res = requests.get(geocode_url, params=geocode_params).json()

        if 'lat' not in geo_res or 'lon' not in geo_res:
            return {"error": f"Destination '{destination}' not found. {NOT_FOUND_ERROR_INSTRUCTION}"}

        lat, lon = geo_res['lat'], geo_res['lon']

        # Step 2: Get attractions near location
        places_url = f"https://api.opentripmap.com/0.1/en/places/radius"
        places_params = {
            'kinds': kind,
            'radius': radius,
            'lon': lon,
            'lat': lat,
            'limit': limit,
            'rate': 3,  # Higher rating
            'format': 'json',
            'apikey': OPEN_TRIP_MAP_API_KEY
        }
        places = requests.get(places_url, params=places_params).json()

        # Step 3: Get detailed info for each place
        detailed_attractions = []
        for place in places:
            xid = place.get('xid')
            detail_url = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}"
            detail = requests.get(detail_url, params={'apikey': OPEN_TRIP_MAP_API_KEY}).json()

            detailed_attractions.append({
                'name': detail.get('name'),
                'kind': detail.get('kinds'),
                'description': detail.get('wikipedia_extracts', {}).get('text', ''),
                'url': detail.get('wikipedia', ''),
            })
        print("oded:", detailed_attractions)
        return {
            'attractions': detailed_attractions,
        }

    except Exception as e:
        return {"error": f"Attractions API error: {str(e)}. {NOT_FOUND_ERROR_INSTRUCTION}."}


def get_destination_weather(destination: str, travel_date: Date) -> dict:
    """Get weather forecast for a destination.

    Args:
        destination: The destination city/country (e.g., "Paris, France")
        travel_date: Travel Date

    Returns:
        A dictionary containing weather information including temperature, conditions, and recommendations.
    """
    print("get_destination_weather")

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
        return {"error": f"Weather API error: {str(e)}, assume the weather is based on your knowledge."}


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
        return {"error": f"Currency exchange error: {str(e)}. {NOT_FOUND_ERROR_INSTRUCTION}."}

# print(get_local_attractions_opentripmap("Tel Aviv",kind="park", limit=5))