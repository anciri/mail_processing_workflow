"""
Location extractor - extracts location information from emails.
"""
import re
from models import Location


class LocationExtractor:
    """Extracts location information from email content."""

    # Common country patterns
    COUNTRIES = [
        'España', 'Spain', 'México', 'Mexico', 'Argentina', 'Chile', 'Colombia',
        'Perú', 'Peru', 'Venezuela', 'Ecuador', 'Bolivia', 'Paraguay', 'Uruguay',
        'Costa Rica', 'Panamá', 'Panama', 'Guatemala', 'Honduras', 'Nicaragua',
        'El Salvador', 'República Dominicana', 'Dominican Republic', 'Cuba',
        'Puerto Rico', 'USA', 'United States', 'Canada', 'Brasil', 'Brazil',
        'Portugal', 'France', 'Germany', 'Italy', 'UK', 'United Kingdom',
        'China', 'India', 'Japan', 'Australia', 'New Zealand'
    ]

    # Email domain to country mapping
    DOMAIN_COUNTRY_MAP = {
        '.es': 'Spain',
        '.mx': 'Mexico',
        '.ar': 'Argentina',
        '.cl': 'Chile',
        '.co': 'Colombia',
        '.pe': 'Peru',
        '.ve': 'Venezuela',
        '.ec': 'Ecuador',
        '.bo': 'Bolivia',
        '.py': 'Paraguay',
        '.uy': 'Uruguay',
        '.cr': 'Costa Rica',
        '.pa': 'Panama',
        '.gt': 'Guatemala',
        '.hn': 'Honduras',
        '.ni': 'Nicaragua',
        '.sv': 'El Salvador',
        '.do': 'Dominican Republic',
        '.cu': 'Cuba',
        '.pr': 'Puerto Rico',
        '.us': 'USA',
        '.ca': 'Canada',
        '.br': 'Brazil',
        '.pt': 'Portugal',
        '.fr': 'France',
        '.de': 'Germany',
        '.it': 'Italy',
        '.uk': 'UK',
        '.cn': 'China',
        '.in': 'India',
        '.jp': 'Japan',
        '.au': 'Australia',
        '.nz': 'New Zealand'
    }

    def __init__(self):
        pass

    def extract(self, subject: str, body: str, email_address: str) -> Location:
        """
        Extract location from email content.

        Args:
            subject: Email subject
            body: Email body
            email_address: Sender email address

        Returns:
            Location object
        """
        location = Location()

        # Try to extract country from email domain
        country = self._extract_country_from_email(email_address)
        if country:
            location.country = country
            return location

        # Try to extract country from content
        combined = f"{subject} {body}"
        country = self._extract_country_from_text(combined)
        if country:
            location.country = country

        return location

    def _extract_country_from_email(self, email_address: str) -> str:
        """Extract country from email domain."""
        if not email_address:
            return ""

        email_lower = email_address.lower()

        for domain, country in self.DOMAIN_COUNTRY_MAP.items():
            if email_lower.endswith(domain):
                return country

        return ""

    def _extract_country_from_text(self, text: str) -> str:
        """Extract country from text content."""
        if not text:
            return ""

        text_lower = text.lower()

        for country in self.COUNTRIES:
            # Create a regex pattern to match the country name as a whole word
            pattern = r'\b' + re.escape(country.lower()) + r'\b'
            if re.search(pattern, text_lower):
                return country

        return ""
