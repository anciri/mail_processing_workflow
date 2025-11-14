# Getting Started - Email Processing Workflow

Complete step-by-step guide for setting up and running the email processing workflow.

## 📋 What You'll Need

- Windows computer
- Microsoft Outlook (installed and configured)
- Python 3.8+ installed
- OpenRouter or OpenAI API account
- 15-30 minutes for setup

---

## Part 1: One-Time Setup

### Step 1: Install Python

1. Go to https://www.python.org/downloads/
2. Click "Download Python"
3. Run the installer
4. **✅ IMPORTANT**: Check the box "Add Python to PATH"
5. Click "Install Now"
6. Test installation:
   ```bash
   # Open Command Prompt (Windows Key + R, type cmd, Enter)
   python --version
   # Should show: Python 3.11.x or similar
   ```

---

### Step 2: Get API Key

**Option A: OpenRouter (Recommended - Cheaper)**

1. Go to https://openrouter.ai/
2. Sign up or log in
3. Go to https://openrouter.ai/keys
4. Click "Create Key"
5. Copy key (starts with `sk-or-`)
6. Add $10-20 credits: https://openrouter.ai/credits

**Option B: Direct OpenAI**

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy key (starts with `sk-`)

**Save your key somewhere safe!**

---

### Step 3: Download and Extract Files

1. Download repository as ZIP from GitHub
2. Extract to a folder (e.g., `C:\EmailWorkflow\`)
3. Remember this location!

---

### Step 4: Install Dependencies

1. Open Command Prompt (`Windows Key + R`, type `cmd`, press Enter)
2. Navigate to your folder:
   ```bash
   cd C:\EmailWorkflow
   ```
   (Replace with your actual path)

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Wait 1-2 minutes for installation to complete

---

### Step 5: Run Setup Script

```bash
python setup_config.py
```

This creates two files:
- `workflow_config.yaml` - Your Outlook settings
- `.env` - Your API key

---

### Step 6: Configure Your Settings

**Edit workflow_config.yaml:**

1. Open in Notepad:
   ```bash
   notepad workflow_config.yaml
   ```

2. Change these values:
   ```yaml
   extraction:
     target_account_email: "your.email@company.com"  # ← Your email
     inbox_folder_name: "Inbox"                      # ← Usually "Inbox" or "Bandeja de entrada"
     target_folder_name: "YourFolder"                # ← Your folder name
     target_subfolder_name: ""                       # ← Optional subfolder
   ```

3. Save and close

**How to find your folder name:**
```bash
python show_outlook_folders.py
```
This shows your exact folder structure.

---

**Edit .env file:**

1. Open in Notepad:
   ```bash
   notepad .env
   ```

2. Add your API key:
   ```env
   # If using OpenRouter:
   OPENROUTER_API_KEY=sk-or-your-key-here

   # If using OpenAI:
   OPENAI_API_KEY=sk-your-key-here
   ```

3. Save and close

---

## Part 2: Running the Workflow

### Before Each Run

✅ Make sure Microsoft Outlook is **open**

---

### Basic Workflow

1. **Open Command Prompt**
   ```bash
   cd C:\EmailWorkflow
   ```

2. **Run the workflow**
   ```bash
   python workflow.py
   ```

3. **What happens:**

   **Phase 1: Extraction (1-5 minutes)**
   - Script connects to Outlook
   - Extracts emails from your folder
   - Shows progress: "Processing item 10..."
   - Completes: "✅ Email extraction completed successfully!"

   **Phase 2: Checkpoint (Your turn!)**
   - Script pauses
   - Shows file location: `outputs/emails.xlsx`
   - **You do this:**
     1. Open `outputs/emails.xlsx` in Excel
     2. Review the extracted emails
     3. Check if everything looks correct
     4. Close Excel
     5. Go back to Command Prompt

   **Phase 3: Confirmation**
   - Script asks: "Continue to processing? (yes/no):"
   - Type `yes` to continue
   - Type `no` to stop
   - Press Enter

   **Phase 4: AI Processing (2-10 minutes)**
   - Script analyzes emails with AI
   - Shows progress: "Processing batch 1-10 of 50..."
   - Completes: "✅ PROCESSING COMPLETE!"

4. **View Results**
   - Open `outputs/emails_processed.xlsx`
   - This is your final file with all analysis! ⭐

---

### With Date Filtering

```bash
# Extract emails from January 2024
python workflow.py --start-date 2024-01-01 --end-date 2024-01-31

# From specific date onwards
python workflow.py --start-date 2024-01-01

# Up to specific date
python workflow.py --end-date 2024-12-31
```

---

### Other Options

```bash
# Extract only (no AI processing)
python workflow.py --extract-only

# Skip extraction (process existing file)
python workflow.py --skip-extraction

# Skip checkpoint (automatic)
python workflow.py --auto-process
```

---

## 📊 Understanding Output Files

In the `outputs/` folder:

| File | What It Contains |
|------|------------------|
| `emails.xlsx` | All extracted emails |
| `emails_excluded.xlsx` | Emails that weren't RFQs |
| `emails_errors.xlsx` | Any processing errors |
| `emails_processed.xlsx` | **FINAL FILE** ⭐ with AI analysis |

### emails_processed.xlsx Columns

**Original Data:**
- From_Name, From_Email
- Date, Subject, Body
- Attachments, Location

**AI-Added Data:**
- company_name
- company_website
- company_country
- email_category (Solution/Products)
- product_category
- equipment_requested
- technical_specifications

---

## 🔧 Troubleshooting

### "python is not recognized"
**Problem:** Python not installed or not in PATH
**Solution:**
1. Reinstall Python
2. Check "Add Python to PATH" during installation
3. Restart Command Prompt

---

### "Outlook is not running"
**Problem:** Outlook not open
**Solution:** Open Microsoft Outlook before running script

---

### "Folder not found"
**Problem:** Folder name doesn't match
**Solution:**
1. Run `python show_outlook_folders.py`
2. Find exact folder name (spelling, capitals matter!)
3. Update `workflow_config.yaml` with exact name

---

### "API key not found"
**Problem:** API key not set correctly
**Solution:**
1. Check `.env` file exists
2. Verify key is on correct line
3. Key should start with `sk-or-` or `sk-`
4. No quotes needed around key

---

### "No emails extracted"
**Problem:** No emails found
**Solution:**
1. Check date filters aren't too restrictive
2. Verify folder name is correct
3. Check emails exist in that folder in Outlook

---

### "Module not found"
**Problem:** Dependencies not installed
**Solution:**
```bash
pip install -r requirements.txt
```

---

## 💡 Tips for Success

### First Time
- Start with a small date range (1 week)
- Verify extraction looks good before processing
- Use the checkpoint to review

### Regular Use
- Process emails weekly rather than all at once
- Keep Outlook open during extraction
- Check API balance periodically

### Performance
- For large batches (>500 emails):
  - Reduce concurrency in config
  - Add sleep between batches
  - Consider splitting into smaller date ranges

---

## 🎯 Complete Example Run

```
C:\> cd C:\EmailWorkflow

C:\EmailWorkflow> python workflow.py --start-date 2024-01-01 --end-date 2024-01-31

==================================================================
     EMAIL EXTRACTION AND PROCESSING WORKFLOW
==================================================================

[Step 1/3] EXTRACTING EMAILS FROM OUTLOOK
✅ Conectado a Outlook exitosamente
📂 Accediendo a carpeta: Bandeja de entrada
📂 Accediendo a carpeta: TAGA
📂 Accediendo a subcarpeta: RFQ
📧 Encontrados 1263 items en la carpeta
Filtrando correos desde 2024-01-01 hasta 2024-01-31
  Procesando item 10... (Emails procesados: 8, Excluidos: 2)
  Procesando item 20... (Emails procesados: 15, Excluidos: 5)
✅ Email extraction completed successfully!

[Step 2/3] CHECKPOINT - REVIEW EXTRACTED RESULTS

Please review the extracted emails before processing:
  📄 File location: outputs/emails.xlsx

Continue to processing? (yes/no): yes

[Step 3/3] PROCESSING EMAILS WITH AI ANALYSIS
🔄 Using OpenRouter with model: openai/gpt-4o-mini
🚀 Processing 15 emails with concurrency=10...
📧 Processing batch 1-10 of 15...
📧 Processing batch 11-15 of 15...

==================================================================
           WORKFLOW COMPLETED SUCCESSFULLY
==================================================================
✅ All steps completed successfully!

Output files:
  📄 Extracted emails: outputs/emails.xlsx
  📄 Processed emails: outputs/emails_processed.xlsx
```

---

## 📚 Next Steps

- **Configuration**: See `docs/CONFIGURATION.md` for all options
- **Models**: See `docs/OPENROUTER.md` for AI model choices
- **Security**: See `docs/SECURITY.md` for best practices

---

## ✅ Quick Checklist

Print this and check off as you go:

**Setup (Do Once):**
- [ ] Python installed with PATH
- [ ] API key obtained
- [ ] Files downloaded and extracted
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Setup script run (`python setup_config.py`)
- [ ] `workflow_config.yaml` edited with your settings
- [ ] `.env` edited with API key
- [ ] Folder structure verified (`python show_outlook_folders.py`)

**Each Run:**
- [ ] Outlook is open
- [ ] Command Prompt opened to project folder
- [ ] Run: `python workflow.py`
- [ ] Review extracted emails during checkpoint
- [ ] Confirm to continue processing
- [ ] Open `outputs/emails_processed.xlsx` for results

---

**You're all set!** 🎉
