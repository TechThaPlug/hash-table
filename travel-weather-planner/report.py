
from datetime import datetime, timezone
from pathlib import Path
import re


def generate_travel_report(
    destination,
    country,
    travel_plan,
    currency_unit="°C",
):
    """Generate a professional travel weather report."""

    if not isinstance(destination, str) or not destination.strip():
        raise ValueError("Destination is required.")

    if len(destination) > 100:
        raise ValueError("Destination cannot exceed 100 characters.")

    if not isinstance(country, str) or not country.strip():
        raise ValueError("Country is required.")

    if len(country) > 100:
        raise ValueError("Country cannot exceed 100 characters.")

    if not isinstance(travel_plan, dict):
        raise TypeError("Travel plan must be a dictionary.")

    required_fields = [
        "start_date",
        "end_date",
        "number_of_days",
        "daily_summary",
        "packing_recommendations",
    ]

    for field in required_fields:
        if field not in travel_plan:
            raise ValueError(f"Travel plan is missing: {field}")

    number_of_days = travel_plan["number_of_days"]

    if (
        isinstance(number_of_days, bool)
        or not isinstance(number_of_days, int)
        or not 1 <= number_of_days <= 16
    ):
        raise ValueError("Invalid travel duration.")

    daily_summary = travel_plan["daily_summary"]
    recommendations = travel_plan["packing_recommendations"]

    if not isinstance(daily_summary, list) or not daily_summary:
        raise ValueError("Daily weather summary cannot be empty.")

    if len(daily_summary) != number_of_days:
        raise ValueError("Travel plan day count does not match its summary.")

    if not isinstance(recommendations, list):
        raise ValueError("Packing recommendations must be a list.")

    if not all(
        isinstance(item, str) and item.strip()
        for item in recommendations
    ):
        raise ValueError("Invalid packing recommendation.")

    if currency_unit not in {"°C", "°F"}:
        raise ValueError("Temperature unit must be °C or °F.")

    required_daily_fields = [
        "date",
        "temperature_min",
        "temperature_max",
        "rain_probability",
        "wind_speed",
        "condition",
    ]

    lines = [
        "=" * 65,
        "                 TRAVEL WEATHER PLANNER",
        "                    WEATHER REPORT",
        "=" * 65,
        f"Destination: {destination.strip()}",
        f"Country: {country.strip()}",
        f"Travel period: {travel_plan['start_date']} to "
        f"{travel_plan['end_date']}",
        f"Duration: {number_of_days} day(s)",
        f"Generated: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}",
        "=" * 65,
        "",
        "DAILY WEATHER FORECAST",
        "-" * 65,
    ]

    for day in daily_summary:
        if not isinstance(day, dict):
            raise ValueError("Invalid daily forecast information.")

        for field in required_daily_fields:
            if field not in day:
                raise ValueError(
                    f"Daily forecast is missing: {field}"
                )

        temperature_min = day["temperature_min"]
        temperature_max = day["temperature_max"]
        rain_probability = day["rain_probability"]
        wind_speed = day["wind_speed"]

        numeric_values = [
            temperature_min,
            temperature_max,
            rain_probability,
            wind_speed,
        ]

        for value in numeric_values:
            if isinstance(value, bool) or not isinstance(
                value, (int, float)
            ):
                raise ValueError("Invalid numerical weather data.")

        if temperature_min > temperature_max:
            raise ValueError("Minimum temperature exceeds maximum.")

        if not 0 <= rain_probability <= 100:
            raise ValueError("Invalid precipitation probability.")

        if wind_speed < 0:
            raise ValueError("Wind speed cannot be negative.")

        if not isinstance(day["condition"], str):
            raise ValueError("Invalid weather condition.")

        lines.extend([
            f"Date: {day['date']}",
            f"Weather: {day['condition']}",
            f"Temperature: {temperature_min} to "
            f"{temperature_max}{currency_unit}",
            f"Rain probability: {rain_probability}%",
            f"Maximum wind speed: {wind_speed} km/h",
            "-" * 65,
        ])

    lines.extend([
        "",
        "PACKING RECOMMENDATIONS",
        "-" * 65,
    ])

    for number, recommendation in enumerate(
        recommendations,
        start=1,
    ):
        lines.append(f"{number}. {recommendation}")

    lines.extend([
        "",
        "=" * 65,
        "Travel smart. Stay prepared. Enjoy your journey!",
        "=" * 65,
    ])

    return "\n".join(lines)


def save_travel_report(
    report,
    filename,
    directory="reports",
):
    """Save a report securely without overwriting existing files."""

    if not isinstance(report, str) or not report.strip():
        raise ValueError("Report content cannot be empty.")

    if not isinstance(filename, str):
        raise TypeError("Filename must be text.")

    if (
        not filename.strip()
        or Path(filename).name != filename
        or filename in {".", ".."}
        or "/" in filename
        or "\\" in filename
    ):
        raise ValueError("Invalid report filename.")

    if not re.fullmatch(
        r"[a-zA-Z0-9_-]+\.txt",
        filename,
        flags=re.IGNORECASE,
    ):
        raise ValueError("Invalid report filename format.")

    report_directory = Path(directory).resolve()
    report_directory.mkdir(parents=True, exist_ok=True)

    destination = report_directory / filename

    with destination.open("x", encoding="utf-8") as file:
        file.write(report)

    return destination
