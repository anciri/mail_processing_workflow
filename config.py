"""
Configuration settings for the email extractor.
Loads settings from workflow_config.yaml.

NOTE: This file loads configuration from workflow_config.yaml
Edit workflow_config.yaml (copy from workflow_config.yaml.template) to customize settings.
"""
from config_loader import get_config

# Load configuration
_config = get_config()
_extraction_config = _config.get_section('extraction')

# === OUTLOOK SETTINGS ===
TARGET_ACCOUNT_EMAIL = _extraction_config.get('target_account_email', 'your_email@company.com')
INBOX_FOLDER_NAME = _extraction_config.get('inbox_folder_name', 'Inbox')
TARGET_FOLDER_NAME = _extraction_config.get('target_folder_name', 'YourFolder')
TARGET_SUBFOLDER_NAME = _extraction_config.get('target_subfolder_name', '')

# === OUTPUT SETTINGS ===
OUTPUT_DIR = _extraction_config.get('output_dir', 'outputs')
OUTPUT_FILENAME = _extraction_config.get('output_filename', 'emails.xlsx')
EXCLUDED_FILENAME = _extraction_config.get('excluded_filename', 'emails_excluded.xlsx')
ERRORS_FILENAME = _extraction_config.get('errors_filename', 'emails_errors.xlsx')

# === PROCESSING SETTINGS ===
PROGRESS_INTERVAL = _extraction_config.get('progress_interval', 10)
