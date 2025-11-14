# Security Migration Guide

## ⚠️ IMPORTANT: Before Pulling Latest Changes

Your current `workflow_config.yaml` contains your personal email and folder settings. Before pulling the latest security updates, **save your configuration**!

---

## 📋 Migration Steps

### Step 1: Save Your Current Configuration

**BEFORE** pulling changes from git, copy your settings:

```bash
# Navigate to your project folder
cd C:\Users\ancir\OneDrive\Desktop\Tevalcor\mail_processing_workflow

# View your current settings
notepad workflow_config.yaml

# Write down or copy these values:
# - target_account_email
# - inbox_folder_name
# - target_folder_name
# - target_subfolder_name
# - Any other custom settings you've changed
```

### Step 2: Pull Security Updates

```bash
git pull origin claude/email-extraction-workflow-011CV5yBhZ2qgZYcJLLyuJsK
```

**What happens:**
- `workflow_config.yaml` is now ignored by git (won't be tracked/committed)
- A new template file `workflow_config.yaml.template` is created
- `config.py` no longer has hardcoded personal data

### Step 3: Run Setup Script

```bash
python setup_config.py
```

This will:
- Create `workflow_config.yaml` from template (if it doesn't exist)
- Create `.env` from `.env.example` (if it doesn't exist)
- Give you instructions on what to edit

### Step 4: Restore Your Settings

Edit `workflow_config.yaml` and add back your settings:

```yaml
extraction:
  target_account_email: "a.ciricugno@tevalcor.com"  # Your email from Step 1
  inbox_folder_name: "Bandeja de entrada"           # Your inbox name
  target_folder_name: "TAGA"                        # Your folder from Step 1
  target_subfolder_name: "RFQ"                      # Your subfolder from Step 1
```

### Step 5: Set API Key in .env

Edit `.env` file:

```env
OPENROUTER_API_KEY=sk-or-your-actual-key-here
```

### Step 6: Verify Security

Check that sensitive files are NOT tracked by git:

```bash
git status
```

You should **NOT** see:
- `workflow_config.yaml`
- `.env`

If you do see them, they're being tracked (bad). Remove them:
```bash
git rm --cached workflow_config.yaml
git rm --cached .env
```

---

## ✅ What Changed (Security Improvements)

### Before (Insecure):
```
❌ workflow_config.yaml - tracked by git with your email
❌ config.py - hardcoded with your email and folders
❌ Anyone cloning repo sees your personal data
```

### After (Secure):
```
✅ workflow_config.yaml - NOT tracked by git
✅ workflow_config.yaml.template - tracked (with placeholders)
✅ config.py - loads from YAML, no hardcoded data
✅ Your personal data stays local
✅ Each user creates their own config
```

---

## 🔍 What's Now Protected

Files that are NO LONGER committed to git:
- `workflow_config.yaml` - Your personal email, folder names, settings
- `.env` - Your API keys
- `outputs/` - All extracted email data
- `*.xlsx` - All Excel files

---

## 🆘 Troubleshooting

### "Config file not found"

If you get an error about missing config:

```bash
# Create from template
python setup_config.py

# Or manually
copy workflow_config.yaml.template workflow_config.yaml
notepad workflow_config.yaml
```

### "API key not found"

```bash
# Create .env file
copy .env.example .env
notepad .env
# Add: OPENROUTER_API_KEY=your-key-here
```

### "My config still appears in git status"

```bash
# Remove from git tracking (keeps local file)
git rm --cached workflow_config.yaml
git commit -m "Remove sensitive config from tracking"
```

### "I already pushed sensitive data"

If you already pushed your email/config to GitHub:

1. **Change any exposed credentials immediately**
2. **Delete the remote branch** (if possible)
3. **Force push** after removing sensitive data:
   ```bash
   git rm --cached workflow_config.yaml
   git commit -m "Remove sensitive data"
   git push --force-with-lease
   ```
4. **Rotate all API keys**

---

## 📝 Quick Reference

**Setup new environment:**
```bash
python setup_config.py
notepad workflow_config.yaml  # Add your settings
notepad .env                   # Add your API key
python workflow.py             # Run workflow
```

**Check security:**
```bash
git status  # Should NOT show workflow_config.yaml or .env
```

**Share with team:**
```bash
# Only share template files, never your actual config
git add workflow_config.yaml.template
git add .env.example
# NEVER: git add workflow_config.yaml
# NEVER: git add .env
```

---

## 🎯 Summary

**What you need to do:**
1. Pull latest changes
2. Run `python setup_config.py`
3. Edit `workflow_config.yaml` with your settings
4. Edit `.env` with your API key
5. Verify git doesn't track these files

**What's automatically protected:**
- Your email address
- Your folder names
- Your API keys
- Your email data
- All output files

---

**Questions?** See `SECURITY.md` for detailed security guidelines.
