# Configuration Guide

This guide explains how to configure the email processing workflow using the centralized configuration system.

## Overview

The workflow uses two configuration files:
1. **workflow_config.yaml** - All workflow settings (Outlook folders, models, processing options)
2. **.env** - Sensitive data (API keys, credentials)

This separation ensures:
- ✅ Configuration is centralized and easy to manage
- ✅ Sensitive data (API keys) never gets committed to git
- ✅ Settings can be changed without modifying code
- ✅ Professional, industry-standard approach

---

## Quick Start

### Step 1: Create .env File

```bash
# Copy the example file
cp .env.example .env

# Edit with your API key
notepad .env   # Windows
nano .env      # Linux/Mac
```

**Add your API key:**
```env
OPENROUTER_API_KEY=sk-or-your-actual-key-here
```

### Step 2: Configure workflow_config.yaml

Edit `workflow_config.yaml` to match your setup:

```yaml
extraction:
  target_account_email: "your.email@company.com"  # ← Change this
  inbox_folder_name: "Bandeja de entrada"         # ← Change if needed
  target_folder_name: "EX:::"                      # ← Change this
  target_subfolder_name: "ex:::"                    # ← Change if needed
```

### Step 3: Run the Workflow

```bash
python workflow.py
```

The scripts will automatically load settings from both files!

---

## Configuration Files Explained

### 1. workflow_config.yaml

**Purpose:** All non-sensitive workflow settings

**Location:** Project root directory

**Example Structure:**

```yaml
# Email extraction settings
extraction:
  target_account_email: "you@company.com"
  inbox_folder_name: "Inbox"
  target_folder_name: "RFQ"
  target_subfolder_name: ""
  output_dir: "outputs"
  output_filename: "emails.xlsx"
  progress_interval: 10

# AI processing settings
processing:
  input_file: "outputs/emails.xlsx"
  output_file: "outputs/emails_processed.xlsx"
  use_openrouter: true
  model: "openai/gpt-4o-mini"
  max_tokens: 700
  temperature: 0
  concurrency: 10
  retry_attempts: 3
```

**What You Should Change:**
- ✏️ `target_account_email` - Your Outlook email
- ✏️ `inbox_folder_name` - Usually "Inbox" or "Bandeja de entrada"
- ✏️ `target_folder_name` - Your folder name (e.g., "RFQ", "TAGA")
- ✏️ `target_subfolder_name` - Subfolder if any, or leave empty ""
- ✏️ `model` - AI model to use (optional, see models section)

**What You Can Leave Default:**
- ✅ `output_dir`, `output_filename` - Unless you want different output location
- ✅ `max_tokens`, `temperature` - These work well for most cases
- ✅ `concurrency`, `retry_attempts` - Optimized defaults

---

### 2. .env File

**Purpose:** Sensitive credentials (API keys)

**Location:** Project root directory

**Security:**
- ⚠️ **NEVER** commit to git (.gitignore excludes it)
- ⚠️ **NEVER** share publicly
- ✅ Each user should have their own .env file

**Example Content:**

```env
# OpenRouter API Key (recommended)
OPENROUTER_API_KEY=sk-or-v1-abc123xyz...

# OR Direct OpenAI API Key (alternative)
# OPENAI_API_KEY=sk-proj-abc123xyz...

# Optional: Override date filters
# START_DATE=2024-01-01
# END_DATE=2024-12-31
```

**Getting API Keys:**

**Option A: OpenRouter (Recommended)**
1. Go to https://openrouter.ai/keys
2. Create key
3. Add to .env as `OPENROUTER_API_KEY=...`

**Option B: Direct OpenAI**
1. Go to https://platform.openai.com/api-keys
2. Create key
3. Add to .env as `OPENAI_API_KEY=...`
4. Set `use_openrouter: false` in workflow_config.yaml

---

## Configuration Options Reference

### Extraction Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `target_account_email` | - | Your Outlook email address |
| `inbox_folder_name` | "Inbox" | Name of inbox folder |
| `target_folder_name` | "RFQ" | Folder containing emails to process |
| `target_subfolder_name` | "" | Optional subfolder name |
| `output_dir` | "outputs" | Where to save output files |
| `output_filename` | "emails.xlsx" | Name of extracted emails file |
| `excluded_filename` | "emails_excluded.xlsx" | Name of excluded emails file |
| `errors_filename` | "emails_errors.xlsx" | Name of errors file |
| `progress_interval` | 10 | Print progress every N emails |

### Processing Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `use_openrouter` | true | Use OpenRouter (true) or OpenAI (false) |
| `model` | "openai/gpt-4o-mini" | AI model to use |
| `max_tokens` | 700 | Max tokens per API call |
| `temperature` | 0 | AI creativity (0=deterministic, 1=creative) |
| `concurrency` | 10 | Number of parallel API calls |
| `sleep_between_batches` | 0 | Seconds to wait between batches |
| `retry_attempts` | 3 | Number of retries on failure |
| `retry_min_wait` | 2 | Min wait between retries (seconds) |
| `retry_max_wait` | 20 | Max wait between retries (seconds) |

---

## Changing AI Models

### OpenRouter Models (Recommended)

Edit `workflow_config.yaml`:

```yaml
processing:
  use_openrouter: true
  model: "google/gemini-flash-1.5"  # ← Change this
```

**Popular Options:**
- `"openai/gpt-4o-mini"` - Fast, cheap ($0.15/$0.60 per 1M tokens)
- `"google/gemini-flash-1.5"` - Cheaper ($0.075/$0.30 per 1M tokens)
- `"anthropic/claude-3-haiku"` - Fast Claude model
- `"meta-llama/llama-3.1-8b-instruct:free"` - Free option

See full list: https://openrouter.ai/models

### Direct OpenAI Models

Edit `workflow_config.yaml`:

```yaml
processing:
  use_openrouter: false
  model: "gpt-4o"  # ← Change this
```

**Options:**
- `"gpt-4o-mini"` - Fast and cheap
- `"gpt-4o"` - More capable but expensive
- `"gpt-4-turbo"` - Previous generation

---

## Advanced Configuration

### Adjusting Concurrency

If you get rate limit errors, reduce concurrency:

```yaml
processing:
  concurrency: 5  # ← Reduced from 10
  sleep_between_batches: 1  # ← Add delay between batches
```

### Changing Output Location

```yaml
extraction:
  output_dir: "C:/MyResults"  # ← Custom directory
  output_filename: "my_emails.xlsx"  # ← Custom filename
```

### Using Multiple Configurations

You can maintain multiple config files for different scenarios:

```bash
# Development config
python workflow.py --config workflow_config_dev.yaml

# Production config
python workflow.py --config workflow_config_prod.yaml
```

*(Note: This requires updating workflow.py to support --config argument)*

---

## Environment Variables

### Loading Priority

The system loads environment variables in this order:
1. .env file in project directory
2. System environment variables
3. Default values from config

### Setting Without .env File

You can also set environment variables directly:

**Windows:**
```cmd
set OPENROUTER_API_KEY=your-key-here
python workflow.py
```

**Linux/Mac:**
```bash
export OPENROUTER_API_KEY=your-key-here
python workflow.py
```

**Permanent (Windows):**
1. Windows Key → "environment variables"
2. Edit system environment variables
3. Environment Variables → New
4. Name: `OPENROUTER_API_KEY`
5. Value: Your key

---

## Troubleshooting

### "No API key found in environment variables"

**Problem:** .env file not created or API key not set

**Solution:**
1. Copy .env.example to .env
2. Add your API key to .env
3. Verify file is in project root directory

### "Configuration file not found: workflow_config.yaml"

**Problem:** Running script from wrong directory

**Solution:**
```bash
cd /path/to/mail_processing_workflow
python workflow.py
```

### "FileNotFoundError: workflow_config.yaml"

**Problem:** Config file missing

**Solution:**
Download latest files from repository or recreate config file

### Changes Not Taking Effect

**Problem:** Python caching old configuration

**Solution:**
```bash
# Delete Python cache
rm -rf __pycache__

# Or restart Python/Terminal
```

### Invalid YAML Syntax

**Problem:** Syntax error in workflow_config.yaml

**Solution:**
- Check indentation (use spaces, not tabs)
- Verify quotes are balanced
- Use YAML validator: https://www.yamllint.com/

---

## Security Best Practices

### ✅ DO:
- Keep .env file in project root
- Add .env to .gitignore (already done)
- Use different API keys for dev/prod
- Rotate API keys periodically
- Limit API key permissions

### ❌ DON'T:
- Commit .env to version control
- Share .env file publicly
- Hard-code API keys in scripts
- Use production keys for testing
- Share API keys via email/chat

---

## Migration from Old System

If you're updating from the old configuration system:

### Before (Old System):
```python
# config.py
TARGET_FOLDER_NAME = "RFQ"
MODEL = "gpt-4o-mini"
```

### After (New System):
```yaml
# workflow_config.yaml
extraction:
  target_folder_name: "RFQ"
processing:
  model: "openai/gpt-4o-mini"
```

**Benefits:**
- No need to edit Python files
- Centralized configuration
- Better organization
- Industry standard

---

## Getting Help

**Configuration Issues:**
1. Check this guide
2. Verify YAML syntax
3. Check file locations
4. Review error messages

**API Key Issues:**
1. Verify key is correct
2. Check API credits/balance
3. Ensure key has proper permissions

**Model Issues:**
1. Check model name spelling
2. Verify model is available
3. Check API provider status

---

## Example Configurations

### Minimal Configuration

```yaml
extraction:
  target_account_email: "you@company.com"
  target_folder_name: "RFQ"

processing:
  model: "openai/gpt-4o-mini"
```

### Full Configuration

```yaml
extraction:
  target_account_email: "you@company.com"
  inbox_folder_name: "Bandeja de entrada"
  target_folder_name: "TAGA"
  target_subfolder_name: "RFQ"
  output_dir: "outputs"
  output_filename: "emails.xlsx"
  excluded_filename: "emails_excluded.xlsx"
  errors_filename: "emails_errors.xlsx"
  progress_interval: 10

processing:
  input_file: "outputs/emails.xlsx"
  output_file: "outputs/emails_processed.xlsx"
  use_openrouter: true
  model: "google/gemini-flash-1.5"
  max_tokens: 700
  temperature: 0
  concurrency: 10
  sleep_between_batches: 0
  retry_attempts: 3
  retry_min_wait: 2
  retry_max_wait: 20

workflow:
  require_checkpoint_confirmation: true
  auto_process: false
```

---

**That's it! Your workflow is now configured using industry-standard practices.** 🎉
