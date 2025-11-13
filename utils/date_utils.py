"""
Date utility functions for email processing.
"""
from datetime import datetime
from typing import Optional
from dateutil import parser


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
        datetime object or None if parsing fails
    """
    if not date_str:
        return None

    try:
        # Try ISO format first (YYYY-MM-DD)
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        pass

    try:
        # Try DD/MM/YYYY
        return datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        pass

    try:
        # Try DD-MM-YYYY
        return datetime.strptime(date_str, '%d-%m-%Y')
    except ValueError:
        pass

    try:
        # Try using dateutil parser as fallback
        return parser.parse(date_str, dayfirst=True)
    except Exception:
        print(f"Error: No se pudo interpretar la fecha '{date_str}'")
        print("Formatos aceptados: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY")
        return None


def get_date_for_filtering(email) -> Optional[datetime]:
    """
    Get date from email for filtering purposes.
    Tries multiple date fields.

    Args:
        email: Outlook email object

    Returns:
        datetime object or None if no date found
    """
    # Try ReceivedTime first
    try:
        if hasattr(email, 'ReceivedTime') and email.ReceivedTime:
            return email.ReceivedTime
    except Exception:
        pass

    # Try SentOn
    try:
        if hasattr(email, 'SentOn') and email.SentOn:
            return email.SentOn
    except Exception:
        pass

    # Try CreationTime
    try:
        if hasattr(email, 'CreationTime') and email.CreationTime:
            return email.CreationTime
    except Exception:
        pass

    return None
