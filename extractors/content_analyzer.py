"""
Content analyzer - determines if an email qualifies as an RFQ.
"""
import re


class ContentAnalyzer:
    """Analyzes email content to determine if it's an RFQ."""

    # Keywords that suggest RFQ/inquiry
    RFQ_KEYWORDS = [
        'rfq', 'request for quotation', 'request for quote', 'cotización', 'cotizacion',
        'presupuesto', 'quote', 'quotation', 'precio', 'price', 'coste', 'cost',
        'oferta', 'offer', 'propuesta', 'proposal', 'inquiry', 'consulta',
        'información', 'informacion', 'information', 'interesado', 'interested',
        'necesito', 'need', 'require', 'requerimos', 'solicitud', 'request'
    ]

    # Keywords that suggest exclusion (auto-replies, notifications, etc.)
    EXCLUSION_KEYWORDS = [
        'out of office', 'fuera de la oficina', 'automatic reply', 'respuesta automática',
        'unsubscribe', 'darse de baja', 'newsletter', 'boletín',
        'do not reply', 'no responder', 'noreply', 'no-reply'
    ]

    def __init__(self):
        pass

    def analyze(self, subject: str, body: str) -> tuple:
        """
        Analyze email content to determine if it qualifies as RFQ.

        Args:
            subject: Email subject line
            body: Email body text

        Returns:
            Tuple of (qualifies: bool, reason: str)
        """
        if not subject and not body:
            return False, "Empty email"

        subject_lower = (subject or "").lower()
        body_lower = (body or "").lower()
        combined = f"{subject_lower} {body_lower}"

        # Check for exclusion keywords first
        for keyword in self.EXCLUSION_KEYWORDS:
            if keyword in combined:
                return False, f"Auto-reply or notification (keyword: {keyword})"

        # Check for RFQ keywords
        for keyword in self.RFQ_KEYWORDS:
            if keyword in combined:
                return True, "RFQ keyword found"

        # Check if email contains question marks (suggests inquiry)
        if '?' in subject or body.count('?') >= 2:
            return True, "Contains questions"

        # Default: exclude if no RFQ indicators found
        return False, "No RFQ keywords or indicators found"
