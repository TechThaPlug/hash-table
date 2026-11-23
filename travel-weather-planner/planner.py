
from datetime import date

from validator import validate_forecast_range
from weather import describe_weather


def get_packing_recommendations(
    temperature_min,
    temperature_max,
    precipitation_probability,
    wind_speed,
    weather_codes,
):
    """Generate packing recommendations from weather conditions."""

    recommendations = []

    if temperature_min < 10:
        recommendations.append(
            "Pack a warm jacket, sweater, and warm clothing."
        )
    elif temperature_min < 18:
        recommendations.append(
            "Pack a light jacket or sweater."
        )

    if temperature_max >= 30:
        recommendations.append(
            "Pack lightweight clothing, sunglasses, and a hat."
        )
    elif temperature_max >= 24:
        recommendations.append(
            "Pack comfortable, breathable clothing."
        )

    if precipitation_probability >= 50:
        recommendations.append(
            "Pack an umbrella or waterproof raincoat."
        )

    if precipitation_probability >= 80:
        recommendations.append(
            "Prepare for a high chance of rain."
        )

    if wind_speed >= 30:
        recommendations.append(
            "Pack a wind-resistant jacket."
        )

    if any(code in {71, 73, 75} for code in weather_codes):
        recommendations.append(
            "Pack warm clothing and suitable footwear for snow."
        )

    if any(code in {45, 48} for code in weather_codes):
        recommendations.append(
            "Pack suitable clothing for foggy conditions."
        )

    if any(code in {95, 96, 99} for code in weather_codes):
        recommendations.append(
            "Monitor storm warnings and plan indoor activities."
        )

    if not recommendations:
        recommendations.append(
            "Pack comfortable everyday clothing and walking shoes."
        )

    recommendations.append(
        "Carry personal essentials, identification, and travel documents."
    )

    return recommendations


def create_travel_plan(
    forecast,
    start_date,
    end_date,
):
    """Create a travel plan from weather forecast data."""

    if not isinstance(forecast, dict):
        raise TypeError("Forecast must be a dictionary.")

    validate_forecast_range(start_date, end_date)

    daily = forecast.get("daily")

    if not isinstance(daily, dict):
        raise ValueError("Forecast does not contain daily weather data.")

    required_fields = [
        "time",
        "temperature_2m_min",
        "temperature_2m_max",
        "precipitation_probability_max",
        "wind_speed_10m_max",
        "weather_code",
    ]

    for field in required_fields:
        if field not in daily:
            raise ValueError(
                f"Forecast is missing required field: {field}"
            )

    dates = daily["time"]

    if not dates:
        raise ValueError("Forecast contains no daily records.")

    for field in required_fields[1:]:
        if len(daily[field]) != len(dates):
            raise ValueError(
                f"Forecast data has inconsistent lengths: {field}"
            )

    start_index = dates.index(start_date.isoformat()) if (
        start_date.isoformat() in dates
    ) else None

    end_index = dates.index(end_date.isoformat()) if (
        end_date.isoformat() in dates
    ) else None

    if start_index is None or end_index is None:
        raise ValueError(
            "Selected travel dates are outside the available forecast."
        )

    if end_index < start_index:
        raise ValueError("Invalid travel date range.")

    selected_dates = dates[start_index:end_index + 1]

    selected_forecast = {}

    for field in required_fields[1:]:
        selected_forecast[field] = daily[field][
            start_index:end_index + 1
        ]

    temperatures_min = selected_forecast["temperature_2m_min"]
    temperatures_max = selected_forecast["temperature_2m_max"]
    rain_probabilities = selected_forecast[
        "precipitation_probability_max"
    ]
    wind_speeds = selected_forecast["wind_speed_10m_max"]
    weather_codes = selected_forecast["weather_code"]

    recommendations = get_packing_recommendations(
        temperature_min=min(temperatures_min),
        temperature_max=max(temperatures_max),
        precipitation_probability=max(
            rain_probabilities
        ),
        wind_speed=max(wind_speeds),
        weather_codes=weather_codes,
    )

    daily_summary = []

    for index, travel_day in enumerate(selected_dates):
        daily_summary.append({
            "date": travel_day,
            "temperature_min": temperatures_min[index],
            "temperature_max": temperatures_max[index],
            "rain_probability": rain_probabilities[index],
            "wind_speed": wind_speeds[index],
            "weather_code": weather_codes[index],
"condition": describe_weather(weather_codes[index]),
        })

    return {
        "start_date": start_date,
        "end_date": end_date,
        "number_of_days": len(selected_dates),
        "daily_summary": daily_summary,
        "packing_recommendations": recommendations,
    }
