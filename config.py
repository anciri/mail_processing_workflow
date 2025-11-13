"""
Configuration settings for the email extractor.
Loads settings from workflow_config.yaml.
"""
from config_loader import get_config

# === OUTLOOK SETTINGS ===
# Your Outlook email account
TARGET_ACCOUNT_EMAIL = "a.ciricugno@tevalcor.com"

# Folder navigation (adjust to match your Outlook folder structure)
INBOX_FOLDER_NAME = "Bandeja de entrada"
TARGET_FOLDER_NAME = "TAGA"
TARGET_SUBFOLDER_NAME = "RFQ"  # Leave empty "" if you want all TAGA emails

# === OUTPUT SETTINGS ===
OUTPUT_DIR = _extraction_config.get('output_dir', 'outputs')
OUTPUT_FILENAME = _extraction_config.get('output_filename', 'emails.xlsx')
EXCLUDED_FILENAME = _extraction_config.get('excluded_filename', 'emails_excluded.xlsx')
ERRORS_FILENAME = _extraction_config.get('errors_filename', 'emails_errors.xlsx')

# === PROCESSING SETTINGS ===
PROGRESS_INTERVAL = 10  # Print progress every N items 
