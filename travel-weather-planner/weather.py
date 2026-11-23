
import math

import requests

from validator import validate_destination, validate_temperature_unit


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

TIMEOUT = 15

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Heavy thunderstorm with hail",
}


class WeatherAPIError(Exception):
    """Raised when a weather API request fails."""


def validate_coordinates(latitude, longitude):
    """Validate geographical coordinates."""

    if isinstance(latitude, bool) or isinstance(longitude, bool):
        raise TypeError("Coordinates must be numeric.")

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (ValueError, TypeError):
        raise ValueError("Coordinates must be valid numbers.")

    if not math.isfinite(latitude) or not math.isfinite(longitude):
        raise ValueError("Coordinates must be finite numbers.")

    if not -90 <= latitude <= 90:
        raise ValueError("Latitude must be between -90 and 90.")

    if not -180 <= longitude <= 180:
        raise ValueError("Longitude must be between -180 and 180.")

    return latitude, longitude


def get_destination_coordinates(destination):
    """Find a destination's geographical coordinates."""

    destination = validate_destination(destination)

    parameters = {
        "name": destination,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    try:
        response = requests.get(
            GEOCODING_URL,
            params=parameters,
            timeout=TIMEOUT,
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as error:
        raise WeatherAPIError(
            "Could not connect to the destination search service."
        ) from error

    except ValueError as error:
        raise WeatherAPIError(
            "Destination search returned invalid data."
        ) from error

    if not isinstance(data, dict):
        raise WeatherAPIError("Invalid destination search response.")

    results = data.get("results", [])

    if not results:
        raise ValueError(
            f"No destination found for '{destination}'."
        )

    if not isinstance(results, list) or not isinstance(results[0], dict):
        raise WeatherAPIError("Invalid destination information.")

    location = results[0]

    try:
        latitude, longitude = validate_coordinates(
            location["latitude"],
            location["longitude"],
        )
    except (KeyError, TypeError, ValueError) as error:
        raise WeatherAPIError(
            "Destination returned invalid geographical coordinates."
        ) from error

    return {
        "name": location.get("name", destination),
        "country": location.get("country", "Unknown"),
        "latitude": latitude,
        "longitude": longitude,
        "timezone": location.get("timezone", "UTC"),
    }


def get_weather_forecast(
    latitude,
    longitude,
    temperature_unit="celsius",
):
    """Retrieve a 16-day weather forecast."""

    latitude, longitude = validate_coordinates(
        latitude,
        longitude,
    )

    unit = validate_temperature_unit(temperature_unit)

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": (
            "weather_code,"
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "precipitation_sum,"
            "wind_speed_10m_max"
        ),
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "temperature_unit": unit,
        "wind_speed_unit": "kmh",
        "timezone": "auto",
        "forecast_days": 16,
    }

    try:
        response = requests.get(
            FORECAST_URL,
            params=parameters,
            timeout=TIMEOUT,
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as error:
        raise WeatherAPIError(
            "Could not retrieve the weather forecast."
        ) from error

    except ValueError as error:
        raise WeatherAPIError(
            "Weather service returned invalid data."
        ) from error

    if not isinstance(data, dict):
        raise WeatherAPIError("Invalid weather forecast response.")

    if not isinstance(data.get("daily"), dict):
        raise WeatherAPIError(
            "Weather service returned incomplete daily data."
        )

    if not isinstance(data.get("current"), dict):
        raise WeatherAPIError(
            "Weather service returned incomplete current conditions."
        )

    return data


def describe_weather(code):
    """Convert a weather code into readable text."""

    if isinstance(code, bool) or not isinstance(code, int):
        return "Unknown conditions"

    return WEATHER_CODES.get(code, "Unknown conditions")
