# Quick Start Guide

This guide will get you up and running in 5 minutes.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Outlook Settings

Edit `workflow_config.yaml` and set your email and folder:

```yaml
extraction:
  target_account_email: "your_email@company.com"
  target_folder_name: "RFQ"
```

## Step 3: Set OpenAI API Key

```bash
# Windows Command Prompt
set OPENAI_API_KEY=sk-your-key-here

# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Linux/Mac
export OPENAI_API_KEY=sk-your-key-here
```

## Step 4: Run the Workflow

```bash
python workflow.py
```

## What Happens Next?

1. **Extraction Phase**
   - Script connects to Outlook
   - Extracts emails from your specified folder
   - Saves to `outputs/emails.xlsx`

2. **Checkpoint Phase**
   - Script pauses and asks you to review
   - Open `outputs/emails.xlsx` in Excel
   - Check the extracted emails
   - Return to terminal and type `yes` to continue

3. **Processing Phase**
   - Script analyzes emails with AI
   - Extracts company info and categorizes
   - Saves final results to `outputs/emails_processed.xlsx`

## Common Commands

```bash
# Extract only (no processing)
python workflow.py --extract-only

# Skip checkpoint (auto-process)
python workflow.py --auto-process

# Filter by date
python workflow.py --start-date 2024-01-01 --end-date 2024-12-31

# Process existing extraction
python workflow.py --skip-extraction
```

## Troubleshooting

**Problem**: "Outlook is not running"
**Solution**: Open Microsoft Outlook before running the script

**Problem**: "Folder not found"
**Solution**: Check that folder names in config match your Outlook folders exactly

**Problem**: "OpenAI API error"
**Solution**: Verify your API key is set correctly and you have credits

**Problem**: "No module named..."
**Solution**: Run `pip install -r requirements.txt`

## Output Files Location

All output files are saved in the `outputs/` directory:
- `emails.xlsx` - Extracted emails
- `emails_excluded.xlsx` - Excluded emails
- `emails_errors.xlsx` - Processing errors
- `emails_processed.xlsx` - Final output with AI analysis

## Need More Help?

See the full README.md for detailed documentation.
