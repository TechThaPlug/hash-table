
from datetime import date, datetime
import re

from validator import (
    validate_destination,
    validate_travel_date,
    validate_forecast_range,
    validate_temperature_unit,
)
from weather import (
    get_destination_coordinates,
    get_weather_forecast,
    WeatherAPIError,
)
from planner import create_travel_plan
from report import generate_travel_report, save_travel_report


def get_input(prompt, validator):
    """Repeatedly request input until validation succeeds."""

    while True:
        try:
            return validator(input(prompt))
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


def get_travel_dates():
    """Collect and validate travel dates."""

    while True:
        start_date = get_input(
            "\nTravel start date (YYYY-MM-DD): ",
            validate_travel_date,
        )

        end_date = get_input(
            "Travel end date (YYYY-MM-DD): ",
            validate_travel_date,
        )

        try:
            validate_forecast_range(start_date, end_date)
            return start_date, end_date

        except ValueError as error:
            print(f"Error: {error}")


def get_temperature_unit():
    """Ask for the preferred temperature unit."""

    while True:
        unit = input(
            "\nTemperature unit (Celsius/Fahrenheit): "
        ).strip()

        try:
            return validate_temperature_unit(unit)

        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


def display_report(report):
    """Display the generated travel report."""

    print("\n")
    print(report)


def run_application():
    """Run the Travel Weather Planner."""

    print("\n" + "=" * 65)
    print("                 TRAVEL WEATHER PLANNER")
    print("=" * 65)

    destination = get_input(
        "\nEnter your destination: ",
        validate_destination,
    )

    temperature_unit = get_temperature_unit()

    print("\nSearching for destination...")

    location = get_destination_coordinates(destination)

    print("\nDestination found!")
    print(f"City: {location['name']}")
    print(f"Country: {location['country']}")
    print(f"Timezone: {location['timezone']}")

    start_date, end_date = get_travel_dates()

    print("\nRetrieving weather forecast...")

    forecast = get_weather_forecast(
        latitude=location["latitude"],
        longitude=location["longitude"],
        temperature_unit=temperature_unit,
    )

    travel_plan = create_travel_plan(
        forecast=forecast,
        start_date=start_date,
        end_date=end_date,
    )

    unit_symbol = (
        "°C" if temperature_unit == "celsius" else "°F"
    )

    for day in travel_plan["daily_summary"]:
        day["temperature_unit"] = unit_symbol

    report = generate_travel_report(
        destination=location["name"],
        country=location["country"],
        travel_plan=travel_plan,
        currency_unit=unit_symbol,
    )

    display_report(report)

    save_choice = input(
        "\nWould you like to save this report? (y/n): "
    ).strip().lower()

    if save_choice == "y":
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        safe_destination = re.sub(
            r"[^a-zA-Z0-9_-]+",
            "_",
            location["name"],
        ).strip("_")[:40]

        filename = (
            f"travel_report_{safe_destination}_{timestamp}.txt"
        )

        try:
            saved_path = save_travel_report(
                report,
                filename,
            )

            print("\nReport saved successfully!")
            print(f"Location: {saved_path}")

        except (OSError, ValueError, TypeError) as error:
            print(f"\nCould not save report: {error}")

    print("\nThank you for using Travel Weather Planner!")


def main():
    """Application entry point."""

    try:
        run_application()

    except KeyboardInterrupt:
        print("\n\nTravel planning cancelled.")

    except WeatherAPIError as error:
        print(f"\nWeather service error: {error}")

    except (ValueError, TypeError) as error:
        print(f"\nTravel planning error: {error}")


if __name__ == "__main__":
    main()
