"""
Data models for email processing.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Location:
    """Represents a location extracted from email."""
    city: str = ""
    state: str = ""
    country: str = ""

    def __str__(self):
        parts = [p for p in [self.city, self.state, self.country] if p]
        return ", ".join(parts) if parts else ""


@dataclass
class EmailData:
    """Represents extracted email data."""
    from_name: str = ""
    from_email: str = ""
    to: str = ""
    cc: str = ""
    date: str = ""
    subject: str = ""
    body: str = ""
    attachments: str = ""
    location: Optional[Location] = None
    error_tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary for DataFrame."""
        return {
            'From_Name': self.from_name,
            'From_Email': self.from_email,
            'To': self.to,
            'CC': self.cc,
            'Date': self.date,
            'Subject': self.subject,
            'Body': self.body,
            'Attachments': self.attachments,
            'Location': str(self.location) if self.location else "",
            'Error_Tags': "; ".join(self.error_tags) if self.error_tags else ""
        }


@dataclass
class ExcludedEmail:
    """Represents an excluded email with reason."""
    from_name: str = ""
    from_email: str = ""
    date: str = ""
    subject: str = ""
    body: str = ""
    location: Optional[Location] = None
    exclusion_reason: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary for DataFrame."""
        return {
            'From_Name': self.from_name,
            'From_Email': self.from_email,
            'Date': self.date,
            'Subject': self.subject,
            'Body': self.body,
            'Location': str(self.location) if self.location else "",
            'Exclusion_Reason': self.exclusion_reason
        }


@dataclass
class ProcessingError:
    """Represents a processing error."""
    error: str = ""
    subject: str = ""
    date: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary for DataFrame."""
        return {
            'Error': self.error,
            'Subject': self.subject,
            'Date': self.date
        }


@dataclass
class ProcessingStats:
    """Statistics for processing run."""
    total_items: int = 0
    extracted_count: int = 0
    excluded_count: int = 0
    error_count: int = 0
    filtered_by_date: int = 0
    complete_count: int = 0
    partial_error_count: int = 0
    error_breakdown: Dict[str, int] = field(default_factory=dict)

    def __str__(self) -> str:
        """Format statistics for display."""
        lines = [
            "\n" + "=" * 60,
            "PROCESSING STATISTICS",
            "=" * 60,
            f"Total items processed: {self.total_items}",
            f"Extracted emails (RFQ): {self.extracted_count}",
            f"  - Complete (no errors): {self.complete_count}",
            f"  - Partial (some errors): {self.partial_error_count}",
            f"Excluded emails (not RFQ): {self.excluded_count}",
            f"Errors (couldn't process): {self.error_count}",
        ]

        if self.filtered_by_date > 0:
            lines.append(f"Filtered by date: {self.filtered_by_date}")

        if self.error_breakdown:
            lines.append("\nError breakdown:")
            for tag, count in sorted(self.error_breakdown.items()):
                lines.append(f"  - {tag}: {count}")

        lines.append("=" * 60)
        return "\n".join(lines)
