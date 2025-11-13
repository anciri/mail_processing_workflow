"""
Configuration settings for the email extractor.
Edit these values to match your Outlook setup.
"""

# === OUTLOOK SETTINGS ===
# Your Outlook email account
TARGET_ACCOUNT_EMAIL = "your_email@company.com"  # CHANGE THIS to your email

# Folder navigation (adjust to match your Outlook folder structure)
INBOX_FOLDER_NAME = "Inbox"
TARGET_FOLDER_NAME = "RFQ"  # CHANGE THIS to your folder name
TARGET_SUBFOLDER_NAME = ""  # Leave empty if no subfolder, or set subfolder name

# === OUTPUT SETTINGS ===
OUTPUT_DIR = "outputs"
OUTPUT_FILENAME = "emails.xlsx"
EXCLUDED_FILENAME = "emails_excluded.xlsx"
ERRORS_FILENAME = "emails_errors.xlsx"

# === PROCESSING SETTINGS ===
PROGRESS_INTERVAL = 10  # Print progress every N items
