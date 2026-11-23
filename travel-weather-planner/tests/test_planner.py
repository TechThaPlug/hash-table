
import unittest
from datetime import date, timedelta

from planner import (
    create_travel_plan,
    get_packing_recommendations,
)


class TestTravelPlanner(unittest.TestCase):

    def test_hot_weather_recommendations(self):
        recommendations = get_packing_recommendations(
            25,
            35,
            10,
            10,
            [0],
        )

        self.assertTrue(
            any("lightweight clothing" in item for item in recommendations)
            or any("sunglasses" in item for item in recommendations)
        )

    def test_rain_recommendations(self):
        recommendations = get_packing_recommendations(
            15,
            22,
            90,
            10,
            [61],
        )

        self.assertTrue(
            any("umbrella" in item for item in recommendations)
        )

    def test_cold_weather_recommendations(self):
        recommendations = get_packing_recommendations(
            5,
            12,
            10,
            10,
            [0],
        )

        self.assertTrue(
            any("warm jacket" in item for item in recommendations)
        )

    def test_travel_plan_creation(self):
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=1)

        forecast_dates = [
            start.isoformat(),
            end.isoformat(),
        ]

        forecast = {
            "daily": {
                "time": forecast_dates,
                "temperature_2m_min": [15, 16],
                "temperature_2m_max": [25, 27],
                "precipitation_probability_max": [20, 80],
                "wind_speed_10m_max": [10, 15],
                "weather_code": [1, 61],
            }
        }

        plan = create_travel_plan(
            forecast,
            start,
            end,
        )

        self.assertEqual(plan["number_of_days"], 2)
        self.assertEqual(len(plan["daily_summary"]), 2)
        self.assertEqual(
            plan["daily_summary"][1]["condition"],
            "Slight rain",
        )

    def test_missing_forecast_data(self):
        start = date.today() + timedelta(days=1)

        with self.assertRaises(ValueError):
            create_travel_plan(
                {"daily": {}},
                start,
                start,
            )

    def test_invalid_forecast_type(self):
        start = date.today() + timedelta(days=1)

        with self.assertRaises(TypeError):
            create_travel_plan(
                [],
                start,
                start,
            )


if __name__ == "__main__":
    unittest.main()
