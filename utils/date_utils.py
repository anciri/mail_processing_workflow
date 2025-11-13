"""
Date utility functions for email processing.
"""
from datetime import datetime
from typing import Optional
from dateutil import parser


def normalize_datetime(dt: datetime) -> datetime:
    """
    Normalize datetime to be timezone-naive for comparison.

    Args:
        dt: datetime object (can be timezone-aware or naive)

    Returns:
        Timezone-naive datetime object
    """
    if dt is None:
        return None

    # If datetime has timezone info, remove it (use local time)
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)

    return dt


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse date string in various formats.

    Supported formats:
    - YYYY-MM-DD
    - DD/MM/YYYY
    - DD-MM-YYYY

    Args:
        date_str: Date string to parse

    Returns:
        Timezone-naive datetime object or None if parsing fails
    """
    if not date_str:
        return None

    try:
        # Try ISO format first (YYYY-MM-DD)
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return normalize_datetime(dt)
    except ValueError:
        pass

    try:
        # Try DD/MM/YYYY
        dt = datetime.strptime(date_str, '%d/%m/%Y')
        return normalize_datetime(dt)
    except ValueError:
        pass

    try:
        # Try DD-MM-YYYY
        dt = datetime.strptime(date_str, '%d-%m-%Y')
        return normalize_datetime(dt)
    except ValueError:
        pass

    try:
        # Try using dateutil parser as fallback
        dt = parser.parse(date_str, dayfirst=True)
        return normalize_datetime(dt)
    except Exception:
        print(f"Error: No se pudo interpretar la fecha '{date_str}'")
        print("Formatos aceptados: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY")
        return None


def get_date_for_filtering(email) -> Optional[datetime]:
    """
    Get date from email for filtering purposes.
    Tries multiple date fields and normalizes to timezone-naive.

    Args:
        email: Outlook email object

    Returns:
        Timezone-naive datetime object or None if no date found
    """
    # Try ReceivedTime first
    try:
        if hasattr(email, 'ReceivedTime') and email.ReceivedTime:
            return normalize_datetime(email.ReceivedTime)
    except Exception:
        pass

    # Try SentOn
    try:
        if hasattr(email, 'SentOn') and email.SentOn:
            return normalize_datetime(email.SentOn)
    except Exception:
        pass

    # Try CreationTime
    try:
        if hasattr(email, 'CreationTime') and email.CreationTime:
            return normalize_datetime(email.CreationTime)
    except Exception:
        pass

    return None
