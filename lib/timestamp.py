"""
Utilities for dealing with timestamps <-> datetimes.
"""

from datetime import datetime, timedelta, timezone

pdt_tz = timezone(timedelta(hours=-7))  # Pacific Daylight Time, applies to May 24-25 data


def lcm_timestamp_to_seconds(timestamp: int) -> float:
    """
    Convert a timestamp from the LCM log to seconds.
    """
    return timestamp / 1e6


def pdt_timestamp_seconds_to_utc_datetime(seconds: float) -> datetime:
    """
    Convert a PDT timestamp in seconds to a UTC datetime object.
    """
    return datetime.fromtimestamp(seconds, tz=pdt_tz).astimezone(tz=timezone.utc)
