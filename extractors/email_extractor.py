"""
Email extractor - extracts data from Outlook email objects.
"""
from models import EmailData, Location
from utils.text_utils import clean_body_text, extract_email_address
from extractors.location_extractor import LocationExtractor


class EmailExtractor:
    """Extracts structured data from Outlook email objects."""

    def __init__(self):
        self.location_extractor = LocationExtractor()

    def extract(self, email) -> EmailData:
        """
        Extract all relevant data from an email.

        Args:
            email: Outlook email object

        Returns:
            EmailData object with extracted information
        """
        email_data = EmailData()
        error_tags = []

        # Extract basic fields
        try:
            email_data.from_name = email.SenderName or ""
        except Exception:
            error_tags.append("ERROR_FROM_NAME")

        try:
            email_data.from_email = extract_email_address(email.SenderEmailAddress or "")
        except Exception:
            error_tags.append("ERROR_FROM_EMAIL")

        try:
            email_data.to = email.To or ""
        except Exception:
            error_tags.append("ERROR_TO")

        try:
            email_data.cc = email.CC or ""
        except Exception:
            error_tags.append("ERROR_CC")

        try:
            if hasattr(email, 'ReceivedTime') and email.ReceivedTime:
                email_data.date = email.ReceivedTime.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            error_tags.append("ERROR_DATE")

        try:
            email_data.subject = email.Subject or ""
        except Exception:
            error_tags.append("ERROR_SUBJECT")

        try:
            email_data.body = clean_body_text(email.Body or "")
        except Exception:
            error_tags.append("ERROR_BODY")

        # Extract attachments
        try:
            attachments = []
            if hasattr(email, 'Attachments'):
                for attachment in email.Attachments:
                    try:
                        attachments.append(attachment.FileName)
                    except Exception:
                        pass
            email_data.attachments = "; ".join(attachments) if attachments else ""
        except Exception:
            error_tags.append("ERROR_ATTACHMENTS")

        # Extract location
        try:
            email_data.location = self.location_extractor.extract(
                email_data.subject,
                email_data.body,
                email_data.from_email
            )
        except Exception:
            error_tags.append("ERROR_LOCATION")

        email_data.error_tags = error_tags
        return email_data
