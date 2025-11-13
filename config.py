"""
Configuration settings for the email extractor.
Edit these values to match your Outlook setup.
"""

# === OUTLOOK SETTINGS ===
# Your Outlook email account
TARGET_ACCOUNT_EMAIL = "a.ciricugno@tevalcor.com"

# Folder navigation (adjust to match your Outlook folder structure)
INBOX_FOLDER_NAME = "Bandeja de entrada"
TARGET_FOLDER_NAME = "TAGA"
TARGET_SUBFOLDER_NAME = "RFQ"  # Leave empty "" if you want all TAGA emails

# === OUTPUT SETTINGS ===
OUTPUT_DIR = "outputs"
OUTPUT_FILENAME = "emails.xlsx"
EXCLUDED_FILENAME = "emails_excluded.xlsx"
ERRORS_FILENAME = "emails_errors.xlsx"

# === PROCESSING SETTINGS ===
PROGRESS_INTERVAL = 10  # Print progress every N items 