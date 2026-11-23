
import unittest
from unittest.mock import Mock, patch
from weather import validate_coordinates
import requests

from weather import (
    describe_weather,
    get_destination_coordinates,
    get_weather_forecast,
    WeatherAPIError,
)


class TestWeatherEngine(unittest.TestCase):

    @patch("weather.requests.get")
    def test_destination_lookup(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [{
                "name": "Nairobi",
                "country": "Kenya",
                "latitude": -1.2864,
                "longitude": 36.8172,
                "timezone": "Africa/Nairobi",
            }]
        }
        mock_get.return_value = mock_response

        result = get_destination_coordinates("Nairobi")

        self.assertEqual(result["name"], "Nairobi")
        self.assertEqual(result["country"], "Kenya")
        self.assertEqual(result["latitude"], -1.2864)

    @patch("weather.requests.get")
    def test_destination_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            get_destination_coordinates("Unknown Place")

    @patch("weather.requests.get")
    def test_destination_api_failure(self, mock_get):
        mock_get.side_effect = requests.Timeout

        with self.assertRaises(WeatherAPIError):
            get_destination_coordinates("Nairobi")

    @patch("weather.requests.get")
    def test_forecast_retrieval(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "current": {"temperature_2m": 25},
            "daily": {"time": ["2026-11-20"]},
        }
        mock_get.return_value = mock_response

        result = get_weather_forecast(
            -1.2864,
            36.8172,
        )

        self.assertEqual(
            result["current"]["temperature_2m"],
            25,
        )

    def test_weather_code_description(self):
        self.assertEqual(
            describe_weather(0),
            "Clear sky",
        )

    def test_unknown_weather_code(self):
        self.assertEqual(
            describe_weather(999),
            "Unknown conditions",
        )

    def test_valid_coordinates(self):
        result = validate_coordinates(-1.2864, 36.8172)

        self.assertEqual(result, (-1.2864, 36.8172))

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            validate_coordinates(100, 36.8172)

    def test_invalid_longitude(self):
        with self.assertRaises(ValueError):
            validate_coordinates(-1.2864, 200)

    def test_non_numeric_coordinates(self):
        with self.assertRaises(ValueError):
            validate_coordinates("invalid", 36.8172)

    def test_infinite_coordinates(self):
        with self.assertRaises(ValueError):
            validate_coordinates(float("inf"), 36.8172)
if __name__ == "__main__":
    unittest.main()
