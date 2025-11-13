#!/usr/bin/env python3
"""
Email Workflow Orchestrator
Coordinates the email extraction and processing pipeline with checkpoint reviews.
"""
import sys
import os
import subprocess
import argparse
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class WorkflowOrchestrator:
    """Orchestrates the email extraction and processing workflow."""

    def __init__(self, auto_process=False):
        self.auto_process = auto_process
        self.extractor_output = "outputs/emails.xlsx"
        self.processor_output = "outputs/emails_processed.xlsx"

    def print_header(self, text):
        """Print a formatted header."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")

    def print_step(self, step_num, total_steps, description):
        """Print a step indicator."""
        print(f"{Colors.BOLD}{Colors.CYAN}[Step {step_num}/{total_steps}] {description}{Colors.END}")

    def print_success(self, message):
        """Print a success message."""
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")

    def print_error(self, message):
        """Print an error message."""
        print(f"{Colors.RED}❌ {message}{Colors.END}")

    def print_warning(self, message):
        """Print a warning message."""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

    def print_info(self, message):
        """Print an info message."""
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}")

    def run_extractor(self, start_date=None, end_date=None):
        """
        Run the email extractor script.

        Args:
            start_date: Optional start date for filtering (YYYY-MM-DD)
            end_date: Optional end date for filtering (YYYY-MM-DD)

        Returns:
            True if successful, False otherwise
        """
        self.print_step(1, 3, "EXTRACTING EMAILS FROM OUTLOOK")

        cmd = [sys.executable, "extractor.py"]

        if start_date:
            cmd.extend(["--start-date", start_date])
        if end_date:
            cmd.extend(["--end-date", end_date])

        self.print_info(f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, check=True, text=True)

            if result.returncode == 0:
                self.print_success("Email extraction completed successfully!")
                return True
            else:
                self.print_error(f"Extractor failed with return code {result.returncode}")
                return False

        except subprocess.CalledProcessError as e:
            self.print_error(f"Error running extractor: {e}")
            return False
        except FileNotFoundError:
            self.print_error("extractor.py not found in current directory")
            return False

    def check_extractor_output(self):
        """
        Check if extractor output exists and display information.

        Returns:
            True if output exists and is valid, False otherwise
        """
        if not os.path.exists(self.extractor_output):
            self.print_error(f"Extractor output file not found: {self.extractor_output}")
            return False

        try:
            import pandas as pd
            df = pd.read_excel(self.extractor_output)
            record_count = len(df)

            self.print_success(f"Found extractor output: {self.extractor_output}")
            self.print_info(f"Records extracted: {record_count}")

            if record_count == 0:
                self.print_warning("No records found in extractor output!")
                return False

            return True

        except Exception as e:
            self.print_error(f"Error reading extractor output: {e}")
            return False

    def checkpoint_review(self):
        """
        Pause workflow for user to review extractor results.

        Returns:
            True if user wants to continue, False otherwise
        """
        self.print_step(2, 3, "CHECKPOINT - REVIEW EXTRACTED RESULTS")

        print(f"\n{Colors.BOLD}Please review the extracted emails before processing:{Colors.END}")
        print(f"  📄 File location: {Colors.CYAN}{self.extractor_output}{Colors.END}")
        print(f"  💡 Open this file in Excel to review the extracted emails")
        print(f"  💡 Check for accuracy, completeness, and relevance")
        print()

        if self.auto_process:
            self.print_info("Auto-process mode enabled - skipping checkpoint")
            return True

        while True:
            response = input(f"{Colors.BOLD}{Colors.YELLOW}Continue to processing? (yes/no): {Colors.END}").strip().lower()

            if response in ['yes', 'y']:
                self.print_success("Proceeding to processing step...")
                return True
            elif response in ['no', 'n']:
                self.print_warning("Workflow stopped by user")
                return False
            else:
                print("Please answer 'yes' or 'no'")

    def run_processor(self):
        """
        Run the email processor script.

        Returns:
            True if successful, False otherwise
        """
        self.print_step(3, 3, "PROCESSING EMAILS WITH AI ANALYSIS")

        cmd = [sys.executable, "email_processing.py"]

        self.print_info(f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, check=True, text=True)

            if result.returncode == 0:
                self.print_success("Email processing completed successfully!")
                return True
            else:
                self.print_error(f"Processor failed with return code {result.returncode}")
                return False

        except subprocess.CalledProcessError as e:
            self.print_error(f"Error running processor: {e}")
            return False
        except FileNotFoundError:
            self.print_error("email_processing.py not found in current directory")
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
        self.print_header("EMAIL EXTRACTION AND PROCESSING WORKFLOW")

        # Step 1: Extract emails (unless skipped)
        if not skip_extraction:
            if not self.run_extractor(start_date, end_date):
                return 1
        else:
            self.print_warning("Skipping extraction step - using existing output")

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
        self.print_header("WORKFLOW COMPLETED SUCCESSFULLY")
        print(f"{Colors.GREEN}All steps completed successfully!{Colors.END}")
        print(f"\n{Colors.BOLD}Output files:{Colors.END}")
        print(f"  📄 Extracted emails: {Colors.CYAN}{self.extractor_output}{Colors.END}")
        print(f"  📄 Processed emails: {Colors.CYAN}{self.processor_output}{Colors.END}")
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
        orchestrator.print_header("EMAIL EXTRACTION ONLY")
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
