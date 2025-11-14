# Security Guidelines

This document outlines security best practices for the Email Processing Workflow.

## 🔒 Sensitive Data Protection

### What is Considered Sensitive

This project handles sensitive data that should **NEVER** be committed to version control:

1. **Personal Information:**
   - Your email address
   - Company name
   - Outlook folder names
   - Email content

2. **Credentials:**
   - API keys (OpenRouter, OpenAI)
   - Authentication tokens
   - Passwords

3. **Output Data:**
   - Extracted emails
   - Processed email data
   - Any Excel files containing business information

---

## 📁 Protected Files

The following files are automatically excluded from git via `.gitignore`:

### User Configuration
- `workflow_config.yaml` - Contains your email, folder names, and settings
- `.env` - Contains API keys and credentials
- `.env.local` - Local environment overrides

### Output Files
- `outputs/` - All extracted and processed email data
- `*.xlsx`, `*.xls` - Excel files with email content

### Other Sensitive Data
- `config_local.py` - Local configuration overrides
- `*_local.yaml` - Any local YAML configs
- `credentials.json` - Credential files

---

## ✅ Safe to Commit

These files are safe to share publicly:

- `workflow_config.yaml.template` - Template with placeholders
- `.env.example` - Example environment file (no real keys)
- All `.py` source files (no hardcoded credentials)
- Documentation files (`.md`)
- `.gitignore` - Defines what to exclude

---

## 🛡️ Security Best Practices

### 1. Never Hardcode Credentials

❌ **DON'T DO THIS:**
```python
API_KEY = "sk-or-abc123..."  # Hardcoded in source
EMAIL = "john@company.com"   # Hardcoded in source
```

✅ **DO THIS:**
```python
# Load from environment variables
API_KEY = os.getenv("OPENROUTER_API_KEY")
EMAIL = config.get('extraction', 'target_account_email')
```

### 2. Use Template Files

- Keep sensitive configs in files that are gitignored
- Provide `.template` versions with placeholder values
- Document what users need to change

### 3. Environment Variables

Store credentials in `.env` file:
```env
OPENROUTER_API_KEY=sk-or-your-key-here
```

Never in source code or committed configs.

### 4. Regular Security Audits

Before committing, check for sensitive data:
```bash
# Search for email addresses
git grep -i "@.*\.com"

# Search for API keys
git grep -i "sk-"

# Search for common sensitive patterns
git grep -i "password\|secret\|token\|key"
```

### 5. API Key Rotation

- Rotate API keys periodically (every 90 days)
- Revoke old keys after rotation
- Never reuse keys across projects

---

## 🚨 If You Accidentally Commit Sensitive Data

### Immediate Actions

1. **Revoke the exposed credential immediately**
   - OpenRouter: https://openrouter.ai/keys
   - OpenAI: https://platform.openai.com/api-keys

2. **Remove from git history**
   ```bash
   # Remove file from latest commit
   git reset HEAD~1
   git add .
   git commit -m "Remove sensitive data"

   # If already pushed, force push (DANGER!)
   git push --force-with-lease
   ```

3. **For public repos, consider the data compromised**
   - Change all credentials
   - Notify affected parties
   - Review access logs

### Prevention

- Use `git-secrets` to scan commits: https://github.com/awslabs/git-secrets
- Enable GitHub's secret scanning: Settings → Security → Secret scanning
- Use pre-commit hooks to check for sensitive data

---

## 📋 Setup Checklist

Before first use, verify:

- [ ] Created `.env` from `.env.example`
- [ ] Created `workflow_config.yaml` from `workflow_config.yaml.template`
- [ ] Added real credentials to `.env` (not `.env.example`)
- [ ] Added real email/folders to `workflow_config.yaml`
- [ ] Verified `.gitignore` excludes sensitive files
- [ ] Tested that git doesn't track sensitive files:
  ```bash
  git status  # Should not show .env or workflow_config.yaml
  ```

---

## 🔐 API Key Security

### Storage

- **Local Development:** Use `.env` file
- **Production:** Use environment variables or secrets manager
- **CI/CD:** Use encrypted secrets (GitHub Secrets, etc.)

### Permissions

- Use keys with minimum required permissions
- Create separate keys for dev/prod environments
- Monitor key usage for unusual activity

### Key Hygiene

- Never log API keys
- Don't include keys in error messages
- Redact keys from debug output
- Use key rotation policies

---

## 📱 Sharing Code

### When sharing this project:

1. **Fork/Clone without sensitive data:**
   ```bash
   git clone https://github.com/anciri/mail_processing_workflow
   cd mail_processing_workflow

   # Create your own config (don't copy from others)
   python setup_config.py
   ```

2. **Share only template files:**
   - Send `workflow_config.yaml.template`
   - Send `.env.example`
   - Never send `workflow_config.yaml` or `.env`

3. **For collaborators:**
   - Each person creates their own `.env`
   - Each person edits their own `workflow_config.yaml`
   - Share configuration structure, not values

---

## 🎓 Security Resources

- **Python Security:** https://python.readthedocs.io/en/stable/library/secrets.html
- **Git Security:** https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage
- **OWASP Guidelines:** https://owasp.org/www-project-top-ten/
- **GitHub Security:** https://docs.github.com/en/code-security

---

## 📞 Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT** create a public issue
2. Contact the repository maintainer privately
3. Provide details about the vulnerability
4. Allow time for a fix before public disclosure

---

## ⚖️ Compliance

### Data Protection

- This tool processes business emails
- Ensure compliance with your organization's data policies
- Consider GDPR, CCPA, and other data protection regulations
- Implement appropriate data retention policies

### Email Privacy

- Only process emails you have authorization to access
- Respect confidentiality of email content
- Secure storage of processed data
- Proper disposal of sensitive information

---

**Remember:** Security is not a one-time setup, it's an ongoing practice!

Last Updated: 2025-01-14
