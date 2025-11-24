"""
Email Information Extractor - Main Entry Point
Extracts and analyzes emails from Outlook folders, identifying RFQ emails and contact information.

Refactored for modularity, maintainability, and extensibility.
"""
import argparse
import os
import pandas as pd
from datetime import datetime
from typing import Optional, List

# Import configuration
from config import (
    TARGET_ACCOUNT_EMAIL, TARGET_FOLDER_NAME, TARGET_SUBFOLDER_NAME,
    INBOX_FOLDER_NAME, OUTPUT_DIR, OUTPUT_FILENAME, EXCLUDED_FILENAME,
    ERRORS_FILENAME, PROGRESS_INTERVAL
)

# Import models
from models import EmailData, ExcludedEmail, ProcessingError, ProcessingStats, Location

# Import utilities
from utils.date_utils import parse_date, get_date_for_filtering
from utils.text_utils import clean_body_text

# Import extractors
from extractors.email_extractor import EmailExtractor
from extractors.content_analyzer import ContentAnalyzer
from extractors.location_extractor import LocationExtractor

# Import Outlook connector
from outlook.connector import OutlookConnector


class EmailProcessor:
    """Main email processing orchestrator"""

    def __init__(self, output_filename=None, excluded_filename=None, errors_filename=None):
        """
        Initialize EmailProcessor with optional custom output filenames.

        Args:
            output_filename: Custom filename for extracted emails (default: from config)
            excluded_filename: Custom filename for excluded emails (default: from config)
            errors_filename: Custom filename for error emails (default: from config)
        """
        self.email_extractor = EmailExtractor()
        self.content_analyzer = ContentAnalyzer()
        self.location_extractor = LocationExtractor()
        self.outlook_connector = OutlookConnector()

        # Use custom filenames if provided, otherwise use defaults from config
        self.output_filename = output_filename or OUTPUT_FILENAME
        self.excluded_filename = excluded_filename or EXCLUDED_FILENAME
        self.errors_filename = errors_filename or ERRORS_FILENAME

    def process_folder(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> tuple:
        """
        Main function to process emails from specified Outlook folder.

        Args:
            start_date: Optional start date for filtering emails (inclusive)
            end_date: Optional end date for filtering emails (inclusive)
            
        Returns:
            Tuple of (success: bool, stats: ProcessingStats, output_path: str)
        """
        try:
            # Connect to Outlook
            self.outlook_connector.connect()

            # Get target folder
            target_folder = self.outlook_connector.get_folder(
                TARGET_ACCOUNT_EMAIL,
                INBOX_FOLDER_NAME,
                TARGET_FOLDER_NAME,
                TARGET_SUBFOLDER_NAME
            )

            # Display date filter info if applicable
            self._print_date_filter_info(start_date, end_date)

            # Process all items in folder
            results, excluded, errors, stats = self._process_items(
                target_folder,
                start_date,
                end_date
            )

            # Calculate statistics
            self._calculate_stats(stats, results, excluded, errors)

            # Print statistics
            print(stats)

            # Save results to Excel files
            output_path = self._save_results(results, excluded, errors)
            
            return True, stats, output_path

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            print("Por favor, asegúrate de que Outlook esté abierto y las carpetas existan.")
            return False, None, None

    def _print_date_filter_info(
        self,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> None:
        """Print date filtering information"""
        if start_date or end_date:
            date_filter_msg = "Filtrando correos"
            if start_date and end_date:
                date_filter_msg += f" desde {start_date.strftime('%Y-%m-%d')} hasta {end_date.strftime('%Y-%m-%d')}"
            elif start_date:
                date_filter_msg += f" desde {start_date.strftime('%Y-%m-%d')}"
            elif end_date:
                date_filter_msg += f" hasta {end_date.strftime('%Y-%m-%d')}"
            print(date_filter_msg)

    def _process_items(
        self,
        target_folder,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> tuple:
        """
        Process all items in the target folder.

        Returns:
            Tuple of (results, excluded_emails, error_emails, stats)
        """
        results: List[EmailData] = []
        excluded_emails: List[ExcludedEmail] = []
        error_emails: List[ProcessingError] = []
        stats = ProcessingStats()

        print(f"Iniciando procesamiento... (sin filtro de Class, procesando todos los items)")

        for item in target_folder.Items:
            stats.total_items += 1

            # Progress indicator
            if stats.total_items % PROGRESS_INTERVAL == 0:
                print(f"  Procesando item {stats.total_items}... "
                      f"(Emails procesados: {len(results)}, Excluidos: {len(excluded_emails)})")

            # Step 1: Date filtering (only if date filters are active)
            if start_date or end_date:
                should_skip, skip_reason = self._check_date_filter(
                    item, start_date, end_date
                )

                if skip_reason == "error":
                    # Couldn't read date but date filtering is active
                    error_emails.append(ProcessingError(
                        error="Cannot read date (date filtering active)",
                        subject=getattr(item, 'Subject', 'Unknown'),
                        date=""
                    ))
                    continue

                if should_skip:
                    stats.filtered_by_date += 1
                    continue

            # Step 2: Content analysis for RFQ qualification
            try:
                subject = item.Subject or ""
                body = item.Body or ""

                qualifies, reason = self.content_analyzer.analyze(subject, body)

                if not qualifies:
                    # Collect excluded email info
                    excluded = self._create_excluded_email(item, subject, body, reason)
                    if excluded:
                        excluded_emails.append(excluded)
                    continue

            except Exception:
                # Can't analyze content, but still process the email
                # It will be marked with error tags
                qualifies = True

            # Step 3: Extract email data
            email_data = self.email_extractor.extract(item)
            results.append(email_data)

        print(f"\nProcesamiento completado!")
        print(f"  Total de items procesados: {stats.total_items}")

        return results, excluded_emails, error_emails, stats

    def _check_date_filter(
        self,
        email,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> tuple:
        """
        Check if email should be filtered by date.

        Returns:
            Tuple of (should_skip: bool, reason: str)
            reason can be: "ok", "skip", or "error"
        """
        received_date = get_date_for_filtering(email)

        if not received_date:
            # Couldn't read date from any source
            return True, "error"

        # Check if email is within date range
        if start_date and received_date < start_date:
            return True, "skip"

        if end_date and received_date > end_date:
            return True, "skip"

        return False, "ok"

    def _create_excluded_email(
        self,
        email,
        subject: str,
        body: str,
        reason: str
    ) -> Optional[ExcludedEmail]:
        """Create ExcludedEmail object from email"""
        try:
            sender_email_addr = ""
            if hasattr(email, 'SenderEmailAddress'):
                sender_email_addr = email.SenderEmailAddress

            location = self.location_extractor.extract(subject, body, sender_email_addr)

            excluded = ExcludedEmail(
                from_name=email.SenderName or "",
                from_email=sender_email_addr,
                date=email.ReceivedTime.strftime('%Y-%m-%d %H:%M:%S') if hasattr(email, 'ReceivedTime') else "",
                subject=subject,
                location=location,
                exclusion_reason=reason,
                body=clean_body_text(body)
            )

            return excluded

        except Exception:
            return None

    def _calculate_stats(
        self,
        stats: ProcessingStats,
        results: List[EmailData],
        excluded: List[ExcludedEmail],
        errors: List[ProcessingError]
    ) -> None:
        """Calculate processing statistics"""
        stats.excluded_count = len(excluded)
        stats.error_count = len(errors)
        stats.extracted_count = len(results)

        # Count emails with processing errors
        for email in results:
            if email.error_tags:
                stats.partial_error_count += 1
                for tag in email.error_tags:
                    stats.error_breakdown[tag] = stats.error_breakdown.get(tag, 0) + 1
            else:
                stats.complete_count += 1

    def _save_results(
        self,
        results: List[EmailData],
        excluded: List[ExcludedEmail],
        errors: List[ProcessingError]
    ) -> str:
        """
        Save results to Excel files using custom or default filenames.
        
        Returns:
            Path to the main output file
        """
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, self.output_filename)

        # Save valid RFQ emails
        if results:
            results_dicts = [email.to_dict() for email in results]
            df = pd.DataFrame(results_dicts)
            df.to_excel(output_path, index=False)
            print(f"\n¡Análisis completo! {len(results)} correos guardados en '{output_path}'")
        else:
            print("\nNo se encontraron correos en la carpeta.")
            # Create empty file if needed or handle as appropriate
            # For now, we still return the path where it would be

        # Save excluded emails
        if excluded:
            excluded_path = os.path.join(OUTPUT_DIR, self.excluded_filename)
            excluded_dicts = [email.to_dict() for email in excluded]
            df_excluded = pd.DataFrame(excluded_dicts)
            df_excluded.to_excel(excluded_path, index=False)
            print(f"Correos excluidos guardados en '{excluded_path}'")

        # Save error emails
        if errors:
            error_path = os.path.join(OUTPUT_DIR, self.errors_filename)
            error_dicts = [error.to_dict() for error in errors]
            df_errors = pd.DataFrame(error_dicts)
            df_errors.to_excel(error_path, index=False)
            print(f"Errores de procesamiento guardados en '{error_path}'")
            
        return output_path


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Extrae correos RFQ de Outlook con filtros opcionales por fecha.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Extraer todos los correos (sin filtro de fecha):
  python inf_extr.py

  # Extraer correos desde una fecha específica:
  python inf_extr.py --start-date 2024-01-01

  # Extraer correos hasta una fecha específica:
  python inf_extr.py --end-date 2024-12-31

  # Extraer correos en un rango de fechas:
  python inf_extr.py --start-date 2024-01-01 --end-date 2024-12-31

Formatos de fecha aceptados: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY
        """
    )

    parser.add_argument(
        '--start-date',
        type=str,
        help='Fecha de inicio para filtrar correos (formato: YYYY-MM-DD, DD/MM/YYYY, o DD-MM-YYYY)'
    )

    parser.add_argument(
        '--end-date',
        type=str,
        help='Fecha de fin para filtrar correos (formato: YYYY-MM-DD, DD/MM/YYYY, o DD-MM-YYYY)'
    )

    args = parser.parse_args()

    # Parse dates if provided
    start_date = None
    end_date = None

    if args.start_date:
        start_date = parse_date(args.start_date)
        if start_date is None:
            print("Error: Fecha de inicio inválida. Saliendo...")
            exit(1)

    if args.end_date:
        end_date = parse_date(args.end_date)
        if end_date is None:
            print("Error: Fecha de fin inválida. Saliendo...")
            exit(1)

    # Validate date range
    if start_date and end_date and start_date > end_date:
        print("Error: La fecha de inicio debe ser anterior a la fecha de fin.")
        exit(1)

    # Create processor and run
    processor = EmailProcessor()
    processor.process_folder(start_date, end_date)


if __name__ == "__main__":
    main()
