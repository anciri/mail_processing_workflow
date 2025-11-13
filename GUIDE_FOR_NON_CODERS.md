# Step-by-Step Guide for Non-Coders
# How to Run the Email Extraction and Processing Workflow

## What You Need Before Starting

1. A Windows computer
2. Microsoft Outlook installed and working
3. An OpenAI API account (I'll show you how to get one)
4. 15-30 minutes to set everything up

---

## PART 1: One-Time Setup (Do this once)

### Step 1: Check if Python is Installed

1. Press `Windows Key + R` on your keyboard
2. Type `cmd` and press Enter
3. A black window will open (this is called Command Prompt)
4. Type: `python --version` and press Enter

**What happens next:**
- If you see something like "Python 3.11.0" → Great! Skip to Step 2
- If you see "python is not recognized" → Continue below

#### Installing Python (if needed):

1. Go to: https://www.python.org/downloads/
2. Click the big yellow button "Download Python"
3. Run the downloaded file
4. **IMPORTANT**: Check the box that says "Add Python to PATH"
5. Click "Install Now"
6. Wait for installation to complete
7. Close and reopen Command Prompt
8. Test again by typing: `python --version`

---

### Step 2: Get Your OpenAI API Key

1. Go to: https://platform.openai.com/signup
2. Create an account (or sign in if you have one)
3. Go to: https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Give it a name like "Email Processing"
6. **COPY THE KEY** - it looks like: `sk-proj-abc123...`
7. Save it in a safe place (you'll need it in Step 5)

**Cost Note**: Processing 100 emails costs about $0.01-0.05

---

### Step 3: Download the Scripts

You should already have these files in a folder. If not:

1. Download all files from your repository
2. Put them in a folder like: `C:\EmailWorkflow\`

---

### Step 4: Install Required Programs

1. Open Command Prompt (Windows Key + R, type `cmd`, press Enter)
2. Navigate to your folder by typing:
   ```
   cd C:\EmailWorkflow
   ```
   (Replace with your actual folder path)

3. Type this command and press Enter:
   ```
   pip install -r requirements.txt
   ```

4. Wait 1-2 minutes while it installs everything
5. You should see "Successfully installed..." messages

---

### Step 5: Set Your OpenAI API Key

**Option A: Set it each time you run (easier)**

When you open Command Prompt, type this BEFORE running the workflow:
```
set OPENAI_API_KEY=sk-proj-your-key-here
```
(Replace `sk-proj-your-key-here` with your actual key from Step 2)

**Option B: Set it permanently (recommended)**

1. Press Windows Key
2. Type "environment variables"
3. Click "Edit the system environment variables"
4. Click "Environment Variables" button
5. Under "User variables", click "New"
6. Variable name: `OPENAI_API_KEY`
7. Variable value: Your API key (paste it here)
8. Click OK on all windows
9. Close and reopen Command Prompt

---

### Step 6: Configure Your Email Settings

1. Find the file called `workflow_config.yaml`
2. Right-click it → Open with → Notepad
3. Find this line:
   ```
   target_account_email: "your_email@company.com"
   ```
4. Replace `your_email@company.com` with YOUR actual Outlook email
5. Find this line:
   ```
   target_folder_name: "RFQ"
   ```
6. Replace `RFQ` with the name of YOUR Outlook folder
7. Save the file (File → Save)
8. Close Notepad

**How to find your folder name:**
- Open Outlook
- Look in the left sidebar for your folders
- Find the folder where your emails are stored
- Use that EXACT name (spelling matters!)

---

## PART 2: Running the Workflow (Do this each time)

### Step 1: Make Sure Outlook is Open

1. Open Microsoft Outlook
2. Make sure you can see your folders
3. Leave it open

---

### Step 2: Open Command Prompt

1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. Navigate to your folder:
   ```
   cd C:\EmailWorkflow
   ```
   (Replace with your actual folder path)

---

### Step 3: Set API Key (if you didn't do Option B above)

```
set OPENAI_API_KEY=sk-proj-your-key-here
```

---

### Step 4: Run the Workflow

Type this command and press Enter:
```
python workflow.py
```

**What happens now:**

#### Phase 1: Extraction (1-5 minutes)
- You'll see messages like "Processing item 10..."
- The script is reading emails from Outlook
- Wait until you see "✅ Email extraction completed successfully!"

#### Phase 2: Checkpoint (YOUR TURN!)
- You'll see: "Please review the extracted emails before processing"
- A file location: `outputs/emails.xlsx`
- **DO THIS NOW:**
  1. Open that folder in File Explorer
  2. Open `emails.xlsx` in Excel
  3. Review the extracted emails
  4. Check if everything looks correct
  5. Close Excel
  6. Go back to Command Prompt

#### Phase 3: Confirmation
- You'll see: "Continue to processing? (yes/no):"
- Type `yes` if everything looks good
- Type `no` if you want to stop
- Press Enter

#### Phase 4: Processing (2-10 minutes)
- If you said yes, the script will analyze emails with AI
- You'll see: "Processing batch 1-10 of 50..."
- Wait until you see "✅ PROCESSING COMPLETE!"

---

### Step 5: View Your Results

1. Open File Explorer
2. Go to your workflow folder
3. Open the `outputs` folder
4. You'll see these Excel files:

   - **emails.xlsx** - All extracted emails
   - **emails_excluded.xlsx** - Emails that weren't RFQs
   - **emails_processed.xlsx** - FINAL FILE with AI analysis ⭐

5. Open `emails_processed.xlsx` in Excel
6. You'll see all the extracted information plus AI analysis

---

## PART 3: Understanding the Results

### What's in emails_processed.xlsx:

**Original columns:**
- From_Name - Who sent it
- From_Email - Their email address
- Date - When it was sent
- Subject - Email subject line
- Body - Email content

**AI-added columns:**
- company_name - Name of the company
- company_website - Their website
- company_country - Which country they're from
- email_category - Type of request (Solution/Products)
- product_category - What type of equipment
- equipment_requested - Detailed description
- technical_specifications - Technical details mentioned

---

## Quick Reference Commands

### Run complete workflow:
```
python workflow.py
```

### Extract emails from last month only:
```
python workflow.py --start-date 2024-01-01 --end-date 2024-01-31
```

### Just extract, don't process:
```
python workflow.py --extract-only
```

### Skip extraction, just process existing file:
```
python workflow.py --skip-extraction
```

### Skip the checkpoint review (auto-process):
```
python workflow.py --auto-process
```

---

## Troubleshooting Common Problems

### "python is not recognized"
**Problem:** Python not installed or not in PATH
**Solution:**
1. Reinstall Python
2. Make sure to check "Add Python to PATH" during installation

---

### "Outlook is not running"
**Problem:** Outlook needs to be open
**Solution:** Open Microsoft Outlook before running the script

---

### "Folder not found"
**Problem:** Folder name in config doesn't match Outlook
**Solution:**
1. Check the exact folder name in Outlook
2. Update `workflow_config.yaml` with the correct name
3. Spelling and capitalization must match exactly

---

### "OpenAI API error" or "Invalid API key"
**Problem:** API key not set or incorrect
**Solution:**
1. Check you copied the complete API key
2. Make sure you set it with the `set OPENAI_API_KEY=...` command
3. The key should start with `sk-`

---

### "No module named 'pandas'" or similar
**Problem:** Dependencies not installed
**Solution:** Run this command again:
```
pip install -r requirements.txt
```

---

### "No emails extracted"
**Problem:** No emails found in the specified folder/date range
**Solution:**
1. Check the folder name is correct
2. Check if date filter is too restrictive
3. Make sure emails exist in that folder

---

## Tips for Success

1. **Start Small**: First time? Try extracting just one week of emails
   ```
   python workflow.py --start-date 2024-01-01 --end-date 2024-01-07
   ```

2. **Always Review**: Use the checkpoint to verify extraction before processing
   - This saves API costs if something went wrong

3. **Keep Outlook Open**: The script needs Outlook running to access emails

4. **Check Output Folder**: After each run, check the `outputs` folder for results

5. **Save Your API Key**: Keep your OpenAI API key in a safe place

6. **Close Excel First**: If you get an error opening files, close Excel and try again

---

## Getting Help

If something goes wrong:

1. **Read the error message** - it often tells you what's wrong
2. **Check this troubleshooting guide** above
3. **Look at the full README.md** for more details
4. **Copy the error message** and ask for help

---

## Example: Complete First Run

Here's what a complete first run looks like:

```
C:\> cd C:\EmailWorkflow
C:\EmailWorkflow> set OPENAI_API_KEY=sk-proj-abc123xyz...
C:\EmailWorkflow> python workflow.py

==================================================================
     EMAIL EXTRACTION AND PROCESSING WORKFLOW
==================================================================

[Step 1/3] EXTRACTING EMAILS FROM OUTLOOK
ℹ️  Running: python extractor.py
Iniciando procesamiento...
  Procesando item 10... (Emails procesados: 8, Excluidos: 2)
  Procesando item 20... (Emails procesados: 15, Excluidos: 5)
Procesamiento completado!
✅ Email extraction completed successfully!

[Step 2/3] CHECKPOINT - REVIEW EXTRACTED RESULTS

Please review the extracted emails before processing:
  📄 File location: outputs/emails.xlsx
  💡 Open this file in Excel to review the extracted emails
  💡 Check for accuracy, completeness, and relevance

Continue to processing? (yes/no): yes
✅ Proceeding to processing step...

[Step 3/3] PROCESSING EMAILS WITH AI ANALYSIS
ℹ️  Running: python email_processing.py
🚀 Processing 15 emails with concurrency=10...
📧 Processing batch 1-10 of 15...
📧 Processing batch 11-15 of 15...
✅ PROCESSING COMPLETE!

==================================================================
           WORKFLOW COMPLETED SUCCESSFULLY
==================================================================
✅ All steps completed successfully!

Output files:
  📄 Extracted emails: outputs/emails.xlsx
  📄 Processed emails: outputs/emails_processed.xlsx
```

---

## You're Done!

You should now have all your processed emails in `outputs/emails_processed.xlsx` ready to use! 🎉
