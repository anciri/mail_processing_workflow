# Email Processing Workflow

Automated workflow for extracting emails from Outlook and processing them with AI analysis.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure settings
python setup_config.py
# Edit workflow_config.yaml and .env with your settings

# 3. Run workflow
python workflow.py
```

**That's it!** See [Getting Started Guide](docs/GETTING_STARTED.md) for detailed instructions.

---

## 📖 What It Does

1. **Extracts** emails from your Outlook folder
2. **Pauses** for you to review extracted data
3. **Processes** emails with AI to extract:
   - Company information
   - Equipment categories
   - Technical specifications
   - Contact details
4. **Saves** results to Excel files

---

## 📁 Project Structure

```
mail_processing_workflow/
├── workflow.py                  # ← Run this
├── extractor.py                 # Email extraction
├── email_processing.py          # AI processing
├── setup_config.py              # Initial setup
├── show_outlook_folders.py      # Folder explorer
│
├── workflow_config.yaml         # Your settings (create from template)
├── .env                         # Your API key (create from example)
├── workflow_config.yaml.template
├── .env.example
│
├── docs/                        # Documentation
│   ├── GETTING_STARTED.md      # Detailed setup guide
│   ├── CONFIGURATION.md        # All configuration options
│   ├── OPENROUTER.md           # AI models and pricing
│   └── SECURITY.md             # Security best practices
│
├── extractors/                  # Email extraction modules
├── outlook/                     # Outlook integration
├── utils/                       # Utility functions
└── outputs/                     # Output files (auto-created)
```

---

## 💡 Common Commands

```bash
# Basic workflow with checkpoint
python workflow.py

# With date filtering
python workflow.py --start-date 2024-01-01 --end-date 2024-12-31

# Extract only (no AI processing)
python workflow.py --extract-only

# Skip checkpoint (automatic mode)
python workflow.py --auto-process

# See your Outlook folder structure
python show_outlook_folders.py
```

---

## 📊 Output Files

| File | Description |
|------|-------------|
| `outputs/emails.xlsx` | Extracted emails |
| `outputs/emails_excluded.xlsx` | Non-RFQ emails |
| `outputs/emails_processed.xlsx` | ⭐ **Final output with AI analysis** |

---

## ⚙️ Configuration

### Outlook Settings

Edit `workflow_config.yaml`:
```yaml
extraction:
  target_account_email: "your.email@company.com"
  inbox_folder_name: "Inbox"
  target_folder_name: "YourFolder"
  target_subfolder_name: ""  # Optional
```

### API Key

Edit `.env`:
```env
OPENROUTER_API_KEY=sk-or-your-key-here
```

Get key from: https://openrouter.ai/keys

### AI Model

Edit `workflow_config.yaml`:
```yaml
processing:
  model: "openai/gpt-4o-mini"           # Fast and cheap
  # or: "google/gemini-flash-1.5"      # Cheaper
  # or: "anthropic/claude-3-haiku"     # Alternative
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Outlook is not running" | Open Outlook before running |
| "Folder not found" | Run `python show_outlook_folders.py` to see folder names |
| "API key not found" | Check `.env` file has your key |
| "No emails extracted" | Check date filters and folder settings |

See [Getting Started](docs/GETTING_STARTED.md#troubleshooting) for more solutions.

---

## 📚 Documentation

- **[Getting Started](docs/GETTING_STARTED.md)** - Step-by-step setup guide
- **[Configuration](docs/CONFIGURATION.md)** - All configuration options
- **[OpenRouter](docs/OPENROUTER.md)** - AI models, pricing, and setup
- **[Security](docs/SECURITY.md)** - Security best practices

---

## 💰 API Costs

Using OpenRouter:
- `gpt-4o-mini`: ~$0.06 per 100 emails
- `gemini-flash-1.5`: ~$0.03 per 100 emails
- Free options available

See [OpenRouter Guide](docs/OPENROUTER.md) for details.

---

## 🔐 Security

**Never commit these files:**
- `workflow_config.yaml` - Contains your personal settings
- `.env` - Contains your API keys
- `outputs/` - Contains your data

These are already in `.gitignore`. See [Security Guidelines](docs/SECURITY.md).

---

## 🎯 Features

- ✅ Outlook email extraction with date filtering
- ✅ Content analysis to identify RFQ emails
- ✅ Location extraction from email content
- ✅ AI-powered company and product analysis
- ✅ Manual checkpoint for review before processing
- ✅ Async processing for speed
- ✅ Retry logic with exponential backoff
- ✅ Multiple output formats (Excel)
- ✅ Detailed error logging
- ✅ OpenRouter support for multiple AI models

---

## 📋 Requirements

- **Python 3.8+**
- **Microsoft Outlook** (installed and running)
- **API Key** from OpenRouter or OpenAI
- See `requirements.txt` for Python packages

---

## 🆘 Getting Help

1. Check [Getting Started Guide](docs/GETTING_STARTED.md)
2. Check [Troubleshooting](docs/GETTING_STARTED.md#troubleshooting)
3. Check [Configuration Reference](docs/CONFIGURATION.md)
4. Review error messages in console

---

## 📜 License

Internal use only. Follow your organization's data handling policies.

---

**Quick Links:**
- [Setup Guide](docs/GETTING_STARTED.md) | [Configuration](docs/CONFIGURATION.md) | [OpenRouter](docs/OPENROUTER.md) | [Security](docs/SECURITY.md)
