# Email Extraction and Processing Workflow

A complete workflow for extracting emails from Outlook and processing them with AI-powered analysis using OpenAI's API.

## Overview

This workflow consists of three main components:

1. **Extractor** (`extractor.py`) - Extracts emails from Outlook folders and saves to Excel
2. **Checkpoint Review** - Manual review step where you can verify extraction results
3. **Processor** (`email_processing.py`) - Analyzes extracted emails using OpenAI API

## Features

- 🔄 **Sequential Execution** - Runs extraction and processing in order with checkpoint
- ✋ **Manual Checkpoint** - Review extracted emails before processing
- 📅 **Date Filtering** - Filter emails by date range
- 🚀 **Async Processing** - Fast parallel API calls with configurable concurrency
- 🔄 **Retry Logic** - Automatic retries with exponential backoff
- 📊 **Detailed Output** - Multiple Excel files for different email categories
- ⚙️ **Flexible Configuration** - YAML config file and command-line options

## Prerequisites

### Required Software
- Python 3.8+
- Microsoft Outlook (must be installed and configured)
- OpenAI API key

### Required Python Packages

```bash
pip install pandas openpyxl pywin32 python-dateutil openai tenacity pyyaml
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Configure Settings

Edit `workflow_config.yaml` to set your Outlook account and folder names:

```yaml
extraction:
  target_account_email: "your_email@company.com"
  target_folder_name: "RFQ"
```

### 2. Set OpenAI API Key

Set your OpenAI API key as an environment variable:

```bash
# Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"

# Linux/Mac
export OPENAI_API_KEY=your-api-key-here
```

Or create a `.env` file in the project directory:

```
OPENAI_API_KEY=your-api-key-here
```

### 3. Run the Workflow

Run the complete workflow with checkpoint:

```bash
python workflow.py
```

The workflow will:
1. Extract emails from Outlook
2. Pause for you to review the extracted emails
3. Wait for your confirmation to continue
4. Process emails with AI analysis

## Usage Examples

### Basic Usage

```bash
# Run complete workflow with checkpoint
python workflow.py

# Skip checkpoint and auto-process (for automation)
python workflow.py --auto-process

# Extract only (no processing)
python workflow.py --extract-only

# Process existing extraction (skip extraction step)
python workflow.py --skip-extraction
```

### Date Filtering

```bash
# Extract emails from a specific date range
python workflow.py --start-date 2024-01-01 --end-date 2024-12-31

# Extract emails after a specific date
python workflow.py --start-date 2024-01-01

# Extract emails before a specific date
python workflow.py --end-date 2024-12-31
```

### Running Scripts Individually

You can also run each script separately:

```bash
# 1. Extract emails
python extractor.py --start-date 2024-01-01

# 2. Review the output file: outputs/emails.xlsx

# 3. Process emails
python email_processing.py
```

## Output Files

The workflow creates several output files in the `outputs/` directory:

| File | Description |
|------|-------------|
| `emails.xlsx` | Extracted RFQ emails with all fields |
| `emails_excluded.xlsx` | Emails that didn't qualify as RFQs |
| `emails_errors.xlsx` | Emails with processing errors |
| `emails_processed.xlsx` | Final output with AI analysis |

### Output File Structure

**emails.xlsx** contains:
- From_Name, From_Email
- Date, Subject, Body
- To, CC, Attachments
- Location information
- Error tags (if any)

**emails_processed.xlsx** contains all above fields plus:
- company_name
- company_website
- company_country
- email_category (Solution/Products)
- product_category
- equipment_requested
- technical_specifications
- subject_body_correlation

## Workflow Steps Explained

### Step 1: Email Extraction

The extractor:
1. Connects to Outlook
2. Navigates to specified folder
3. Filters emails by date (if specified)
4. Analyzes content to identify RFQ emails
5. Extracts contact information and location
6. Saves results to Excel files

**What to review:**
- Check if all relevant emails were extracted
- Verify email classification (RFQ vs excluded)
- Look for any processing errors
- Ensure contact information was extracted correctly

### Step 2: Checkpoint Review

After extraction completes, you can:
- Open `outputs/emails.xlsx` in Excel
- Review the extracted emails
- Check data quality and completeness
- Decide whether to continue to processing

**Decision point:**
- Type `yes` to continue to processing
- Type `no` to stop the workflow

### Step 3: AI Processing

The processor:
1. Loads extracted emails
2. Sends each email to OpenAI API
3. Extracts company information
4. Categorizes equipment type
5. Identifies technical specifications
6. Saves enriched data to final output

## Configuration

### Workflow Configuration (`workflow_config.yaml`)

The YAML config file contains all settings:

```yaml
extraction:
  target_account_email: "your_email@company.com"
  target_folder_name: "RFQ"
  output_dir: "outputs"

processing:
  model: "gpt-4o-mini"
  concurrency: 10
  max_tokens: 700
```

### Extractor Configuration

Edit settings in `config.py` or environment variables:

- `TARGET_ACCOUNT_EMAIL` - Your Outlook account
- `TARGET_FOLDER_NAME` - Folder to extract from
- `OUTPUT_DIR` - Output directory path

### Processor Configuration

Edit settings at the top of `email_processing.py`:

- `MODEL` - OpenAI model (default: gpt-4o-mini)
- `CONCURRENCY` - Parallel requests (default: 10)
- `MAX_TOKENS` - Max tokens per request (default: 700)

## Troubleshooting

### Common Issues

**1. "Outlook is not running"**
- Solution: Open Outlook before running the script

**2. "Folder not found"**
- Solution: Check folder names in config match your Outlook folders

**3. "OpenAI API error"**
- Solution: Verify your API key is set correctly
- Check you have API credits available

**4. "No emails extracted"**
- Solution: Check date filters and folder settings
- Verify emails exist in the target folder

**5. "Module not found"**
- Solution: Install required packages with pip

### Debug Mode

To see more detailed output, you can modify the scripts:

```python
# In extractor.py, increase progress interval
PROGRESS_INTERVAL = 1  # Show progress for every email

# In email_processing.py, add debug prints
print(f"Processing email: {row.get('Subject')}")
```

## Advanced Usage

### Custom AI Prompts

Edit the `PROMPT_TEMPLATE` in `email_processing.py` to customize the AI analysis:

```python
PROMPT_TEMPLATE = """
Your custom instructions here...
"""
```

### Batch Processing

Process large batches efficiently:

```bash
# Increase concurrency for faster processing
# Edit email_processing.py: CONCURRENCY = 20

# Add sleep between batches to avoid rate limits
# Edit email_processing.py: SLEEP_BETWEEN_BATCHES = 1
```

### Automation

For automated workflows without manual checkpoints:

```bash
# Create a scheduled task/cron job
python workflow.py --auto-process --start-date 2024-01-01
```

## Project Structure

```
mail_processing_workflow/
├── extractor.py              # Email extraction from Outlook
├── email_processing.py       # AI-powered email analysis
├── workflow.py               # Workflow orchestrator
├── workflow_config.yaml      # Configuration file
├── config.py                 # Extractor configuration
├── models.py                 # Data models
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── outputs/                  # Output directory
│   ├── emails.xlsx          # Extracted emails
│   ├── emails_excluded.xlsx # Excluded emails
│   ├── emails_errors.xlsx   # Processing errors
│   └── emails_processed.xlsx # Final output
├── extractors/              # Extraction modules
│   ├── email_extractor.py
│   ├── content_analyzer.py
│   └── location_extractor.py
├── outlook/                 # Outlook integration
│   └── connector.py
└── utils/                   # Utility functions
    ├── date_utils.py
    └── text_utils.py
```

## API Costs

The processing step uses OpenAI's API, which has associated costs:

- **gpt-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- Approximate cost: $0.01-0.05 per 100 emails (depends on email length)

Monitor your usage at: https://platform.openai.com/usage

## Best Practices

1. **Start Small** - Test with a small date range first
2. **Review Carefully** - Always review extraction results at checkpoint
3. **Monitor Costs** - Keep track of OpenAI API usage
4. **Backup Data** - Keep copies of original Outlook data
5. **Regular Runs** - Process emails in batches regularly rather than all at once

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the configuration files
3. Check log output for error messages
4. Verify all prerequisites are met

## License

This project is for internal use. Ensure compliance with your organization's data handling policies.

## Changelog

### Version 1.0.0 (2025-11-13)
- Initial release
- Email extraction from Outlook
- AI-powered processing with OpenAI
- Checkpoint review workflow
- Sequential execution with manual approval
