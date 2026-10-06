import requests


def get_weather(city: str):
    """
    Get the current weather for a city.

    Args:
        city: Name of the city.

    Returns:
        Dictionary containing weather information.
    """

    # Step 1: Find the city's coordinates
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(
        geocoding_url,
        params=geocoding_params,
        timeout=10
    )

    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if "results" not in geo_data or not geo_data["results"]:
        return {
            "error": f"Could not find the location '{city}'."
        }

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Step 2: Get weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ],
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=10
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

    current = weather_data["current"]

    return {
        "location": location["name"],
        "country": location.get("country"),
        "temperature_c": current["temperature_2m"],
        "feels_like_c": current["apparent_temperature"],
        "humidity_percent": current["relative_humidity_2m"],
        "precipitation_mm": current["precipitation"],
        "wind_speed_kmh": current["wind_speed_10m"],
        "weather_code": current["weather_code"]
    }