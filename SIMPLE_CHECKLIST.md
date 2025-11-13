# Simple Checklist - Email Workflow
## Print this page and check off each step as you go!

---

## ONE-TIME SETUP (First time only)

### ☐ 1. Install Python
- [ ] Go to https://www.python.org/downloads/
- [ ] Download and run installer
- [ ] **CHECK THE BOX:** "Add Python to PATH"
- [ ] Test: Open Command Prompt, type `python --version`

### ☐ 2. Get API Key (Choose One - OpenRouter Recommended)

**Option A: OpenRouter (RECOMMENDED - Cheaper & More Options)**
- [ ] Go to https://openrouter.ai/
- [ ] Sign up / Log in
- [ ] Go to https://openrouter.ai/keys
- [ ] Click "Create Key"
- [ ] Copy the key (starts with `sk-or-`)
- [ ] Add credits at https://openrouter.ai/credits ($10 = ~200-300 emails)
- [ ] Save key somewhere safe

**Option B: Direct OpenAI**
- [ ] Go to https://platform.openai.com/api-keys
- [ ] Create account / Sign in
- [ ] Click "Create new secret key"
- [ ] Copy the key (starts with `sk-`)
- [ ] Save it somewhere safe

### ☐ 3. Install Required Programs
- [ ] Open Command Prompt (`Windows Key + R`, type `cmd`)
- [ ] Go to your folder: `cd C:\EmailWorkflow` (change path if different)
- [ ] Type: `pip install -r requirements.txt`
- [ ] Wait for "Successfully installed" message

### ☐ 4. Set API Key (Choose Based on Step 2)

**If using OpenRouter (Method A - Set Each Time):**
- [ ] Write this down: `set OPENROUTER_API_KEY=your-key-here`
- [ ] You'll type this each time before running

**If using OpenRouter (Method B - Set Permanently - RECOMMENDED):**
- [ ] Press Windows Key, search "environment variables"
- [ ] Click "Edit the system environment variables"
- [ ] Click "Environment Variables" button
- [ ] Click "New" under User variables
- [ ] Name: `OPENROUTER_API_KEY`
- [ ] Value: (paste your API key)
- [ ] Click OK on everything

**If using Direct OpenAI:**
- [ ] Same steps but use `OPENAI_API_KEY` instead
- [ ] Edit `email_processing.py` line 20: Set `USE_OPENROUTER = False`

### ☐ 5. Edit Configuration File
- [ ] Open `workflow_config.yaml` in Notepad
- [ ] Change `target_account_email` to YOUR email
- [ ] Change `target_folder_name` to YOUR Outlook folder name
- [ ] Save and close

---

## RUNNING THE WORKFLOW (Every time you want to process emails)

### Before You Start:
- [ ] Microsoft Outlook is OPEN
- [ ] You can see your email folders in Outlook

### ☐ Step 1: Open Command Prompt
- [ ] Press `Windows Key + R`
- [ ] Type `cmd` and press Enter

### ☐ Step 2: Go to Your Folder
- [ ] Type: `cd C:\EmailWorkflow` (use your actual path)
- [ ] Press Enter

### ☐ Step 3: Set API Key (Only if you chose Method A above)
- [ ] Type: `set OPENAI_API_KEY=sk-your-key-here`
- [ ] Press Enter

### ☐ Step 4: Run the Script
- [ ] Type: `python workflow.py`
- [ ] Press Enter
- [ ] Wait for extraction to finish

### ☐ Step 5: Review Checkpoint
- [ ] When script pauses, open File Explorer
- [ ] Go to `outputs` folder
- [ ] Open `emails.xlsx` in Excel
- [ ] Review the emails
- [ ] Close Excel

### ☐ Step 6: Confirm Processing
- [ ] Go back to Command Prompt
- [ ] Type `yes` to continue (or `no` to stop)
- [ ] Press Enter
- [ ] Wait for processing to complete

### ☐ Step 7: Check Results
- [ ] Open `outputs` folder
- [ ] Open `emails_processed.xlsx` in Excel
- [ ] This is your final file with all the data! ✅

---

## QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "python is not recognized" | Reinstall Python, check "Add to PATH" |
| "Outlook is not running" | Open Outlook first |
| "Folder not found" | Check folder name in workflow_config.yaml |
| "API error" | Check API key is set correctly |
| "No module named..." | Run `pip install -r requirements.txt` again |

---

## USEFUL COMMANDS

### Extract emails from specific dates:
```
python workflow.py --start-date 2024-01-01 --end-date 2024-01-31
```

### Just extract (don't process):
```
python workflow.py --extract-only
```

### Skip extraction (process existing file):
```
python workflow.py --skip-extraction
```

### Auto-process (skip checkpoint):
```
python workflow.py --auto-process
```

---

## OUTPUT FILES (in the 'outputs' folder)

- **emails.xlsx** - Extracted emails from Outlook
- **emails_excluded.xlsx** - Emails that weren't RFQs
- **emails_errors.xlsx** - Any errors during extraction
- **emails_processed.xlsx** - ⭐ FINAL FILE with AI analysis

---

## NEED HELP?

1. Check error message in Command Prompt
2. Look at GUIDE_FOR_NON_CODERS.md (detailed explanations)
3. Look at README.md (technical details)
4. Ask someone who helped set this up for you

---

*Keep this checklist handy for each time you run the workflow!*
