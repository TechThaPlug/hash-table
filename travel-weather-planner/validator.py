
import re
from datetime import date, datetime


def validate_destination(value):
    """Validate and clean a travel destination."""

    if not isinstance(value, str):
        raise TypeError("Destination must be text.")

    destination = value.strip()

    if not destination:
        raise ValueError("Destination cannot be empty.")

    if len(destination) > 100:
        raise ValueError("Destination cannot exceed 100 characters.")

    if not re.fullmatch(
        r"[\w][\w\s,.'-]*",
        destination,
        flags=re.UNICODE,
    ):
        raise ValueError("Destination contains invalid characters.")

    return destination


def validate_travel_date(value):
    """Validate a travel date in YYYY-MM-DD format."""

    if not isinstance(value, str):
        raise TypeError("Travel date must be text.")

    try:
        travel_date = datetime.strptime(
            value.strip(),
            "%Y-%m-%d",
        ).date()
    except ValueError:
        raise ValueError("Enter a valid date in YYYY-MM-DD format.")

    if travel_date < date.today():
        raise ValueError("Travel date cannot be in the past.")

    return travel_date


def validate_forecast_range(start_date, end_date):
    """Validate the requested travel date range."""

    if not isinstance(start_date, date):
        raise TypeError("Start date must be a date.")

    if not isinstance(end_date, date):
        raise TypeError("End date must be a date.")

    if end_date < start_date:
        raise ValueError("End date cannot be before start date.")

    if (end_date - start_date).days > 15:
        raise ValueError("Travel period cannot exceed 16 days.")

    return True


def validate_temperature_unit(value):
    """Validate the preferred temperature unit."""

    if not isinstance(value, str):
        raise TypeError("Temperature unit must be text.")

    unit = value.strip().lower()

    if unit not in {"celsius", "fahrenheit"}:
        raise ValueError("Choose Celsius or Fahrenheit.")

    return unit
