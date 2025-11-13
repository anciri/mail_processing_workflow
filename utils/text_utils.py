"""
Text utility functions for email processing.
"""
import re


def clean_body_text(body: str, max_length: int = 5000) -> str:
    """
    Clean and truncate email body text.

    Args:
        body: Raw email body text
        max_length: Maximum length to keep (default 5000 chars)

    Returns:
        Cleaned body text
    """
    if not body:
        return ""

    # Remove excessive whitespace
    body = re.sub(r'\s+', ' ', body)

    # Remove common email artifacts
    body = re.sub(r'(\r\n|\r|\n)+', ' ', body)

    # Truncate if too long
    if len(body) > max_length:
        body = body[:max_length] + "... [truncated]"

    return body.strip()


def extract_email_address(email_str: str) -> str:
    """
    Extract email address from string that may contain name and email.

    Examples:
        "John Doe <john@example.com>" -> "john@example.com"
        "john@example.com" -> "john@example.com"

    Args:
        email_str: String containing email address

    Returns:
        Cleaned email address
    """
    if not email_str:
        return ""

    # Look for email in angle brackets
    match = re.search(r'<([^>]+)>', email_str)
    if match:
        return match.group(1).strip()

    # Look for email pattern
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', email_str)
    if match:
        return match.group(0).strip()

    return email_str.strip()
