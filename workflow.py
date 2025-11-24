#!/usr/bin/env python3
"""
Email Workflow Orchestrator
Coordinates the email extraction and processing pipeline with checkpoint reviews.
"""
import sys
import os
import argparse
import logging
from pathlib import Path

# Import core components directly
from extractor import EmailProcessor
from email_processing import AIProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class WorkflowOrchestrator:
    """Orchestrates the email extraction and processing workflow."""

    def __init__(self, auto_process=False):
        self.auto_process = auto_process
        self.extractor_output = "outputs/emails.xlsx"
        self.processor_output = "outputs/emails_processed.xlsx"

    def run_extractor(self, start_date=None, end_date=None):
        """
        Run the email extractor.

        Args:
            start_date: Optional start date for filtering (YYYY-MM-DD)
            end_date: Optional end date for filtering (YYYY-MM-DD)

        Returns:
            True if successful, False otherwise
        """
        logger.info("STEP 1/3: EXTRACTING EMAILS FROM OUTLOOK")

        try:
            # Initialize processor
            processor = EmailProcessor()
            
            # Convert string dates to datetime objects if needed
            # Note: EmailProcessor.process_folder expects datetime objects or None
            # We rely on utils.date_utils.parse_date which is used inside main() of extractor.py
            # but here we are calling process_folder directly.
            # Let's import parse_date to be safe
            from utils.date_utils import parse_date
            
            start_dt = parse_date(start_date) if start_date else None
            end_dt = parse_date(end_date) if end_date else None
            
            success, stats, output_path = processor.process_folder(start_dt, end_dt)
            
            if success:
                self.extractor_output = output_path
                logger.info("✅ Email extraction completed successfully!")
                return True
            else:
                logger.error("❌ Extractor failed")
                return False

        except Exception as e:
            logger.error(f"❌ Error running extractor: {e}")
            return False

    def check_extractor_output(self):
        """
        Check if extractor output exists and display information.

        Returns:
            True if output exists and is valid, False otherwise
        """
        if not os.path.exists(self.extractor_output):
            logger.error(f"❌ Extractor output file not found: {self.extractor_output}")
            return False

        try:
            import pandas as pd
            df = pd.read_excel(self.extractor_output)
            record_count = len(df)

            logger.info(f"Found extractor output: {self.extractor_output}")
            logger.info(f"Records extracted: {record_count}")

            if record_count == 0:
                logger.warning("⚠️  No records found in extractor output!")
                return False

            return True

        except Exception as e:
            logger.error(f"❌ Error reading extractor output: {e}")
            return False

    def checkpoint_review(self):
        """
        Pause workflow for user to review extractor results.

        Returns:
            True if user wants to continue, False otherwise
        """
        logger.info("STEP 2/3: CHECKPOINT - REVIEW EXTRACTED RESULTS")

        print(f"\nPlease review the extracted emails before processing:")
        print(f"  📄 File location: {self.extractor_output}")
        print(f"  💡 Open this file in Excel to review the extracted emails")
        print(f"  💡 Check for accuracy, completeness, and relevance")
        print()

        if self.auto_process:
            logger.info("ℹ️  Auto-process mode enabled - skipping checkpoint")
            return True

        while True:
            response = input(f"Continue to processing? (yes/no): ").strip().lower()

            if response in ['yes', 'y']:
                logger.info("✅ Proceeding to processing step...")
                return True
            elif response in ['no', 'n']:
                logger.warning("⚠️  Workflow stopped by user")
                return False
            else:
                print("Please answer 'yes' or 'no'")

    def run_processor(self):
        """
        Run the email processor.

        Returns:
            True if successful, False otherwise
        """
        logger.info("STEP 3/3: PROCESSING EMAILS WITH AI ANALYSIS")

        try:
            processor = AIProcessor()
            
            # We pass the extractor output as input to the processor
            success = processor.process_emails(
                input_file=self.extractor_output,
                output_file=self.processor_output
            )

            if success:
                logger.info("✅ Email processing completed successfully!")
                return True
            else:
                logger.error("❌ Processor failed")
                return False

        except Exception as e:
            logger.error(f"❌ Error running processor: {e}")
            return False

    def run_workflow(self, start_date=None, end_date=None, skip_extraction=False):
        """
        Run the complete workflow.

        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            skip_extraction: If True, skip extraction and start from existing output

        Returns:
            0 if successful, 1 if failed
        """
        print("\n" + "="*70)
        print("EMAIL EXTRACTION AND PROCESSING WORKFLOW".center(70))
        print("="*70 + "\n")

        # Step 1: Extract emails (unless skipped)
        if not skip_extraction:
            if not self.run_extractor(start_date, end_date):
                return 1
        else:
            logger.warning("⚠️  Skipping extraction step - using existing output")

        # Verify extractor output exists
        if not self.check_extractor_output():
            return 1

        # Step 2: Checkpoint for review
        if not self.checkpoint_review():
            return 1

        # Step 3: Process emails
        if not self.run_processor():
            return 1

        # Final summary
        print("\n" + "="*70)
        print("WORKFLOW COMPLETED SUCCESSFULLY".center(70))
        print("="*70)
        logger.info("All steps completed successfully!")
        print(f"\nOutput files:")
        print(f"  📄 Extracted emails: {self.extractor_output}")
        print(f"  📄 Processed emails: {self.processor_output}")
        print()

        return 0

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Email Extraction and Processing Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete workflow with checkpoint:
  python workflow.py

  # Run with date filtering:
  python workflow.py --start-date 2024-01-01 --end-date 2024-12-31

  # Skip extraction and process existing output:
  python workflow.py --skip-extraction

  # Auto-process without checkpoint (for automation):
  python workflow.py --auto-process

  # Run only extraction step:
  python workflow.py --extract-only
        """
    )

    parser.add_argument(
        '--start-date',
        type=str,
        help='Start date for email filtering (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--end-date',
        type=str,
        help='End date for email filtering (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--skip-extraction',
        action='store_true',
        help='Skip extraction and use existing output file'
    )

    parser.add_argument(
        '--extract-only',
        action='store_true',
        help='Run only the extraction step (no processing)'
    )

    parser.add_argument(
        '--auto-process',
        action='store_true',
        help='Automatically process without checkpoint confirmation'
    )

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = WorkflowOrchestrator(auto_process=args.auto_process)

    # Handle extract-only mode
    if args.extract_only:
        print("\n" + "="*70)
        print("EMAIL EXTRACTION ONLY".center(70))
        print("="*70 + "\n")
        if orchestrator.run_extractor(args.start_date, args.end_date):
            orchestrator.check_extractor_output()
            return 0
        return 1

    # Run complete workflow
    return orchestrator.run_workflow(
        start_date=args.start_date,
        end_date=args.end_date,
        skip_extraction=args.skip_extraction
    )

if __name__ == "__main__":
    sys.exit(main())
