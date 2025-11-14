# Using OpenRouter for Email Processing

## What is OpenRouter?

OpenRouter is a service that provides unified access to multiple AI models from different providers (OpenAI, Anthropic, Google, Meta, etc.) through a single API. Benefits include:

- **Better Pricing**: Often cheaper than using OpenAI directly
- **More Models**: Access to Claude, Gemini, Llama, and many others
- **Fallback Options**: Can switch models if one is down
- **Pay-as-you-go**: No monthly subscriptions

## Quick Setup

### Step 1: Get OpenRouter API Key

1. Go to: https://openrouter.ai/
2. Sign up or log in
3. Go to: https://openrouter.ai/keys
4. Click "Create Key"
5. Copy your API key (starts with `sk-or-...`)

### Step 2: Add Credits

1. Go to: https://openrouter.ai/credits
2. Add credits (start with $5-10)
3. You only pay for what you use

### Step 3: Set API Key

**Windows Command Prompt:**
```bash
set OPENROUTER_API_KEY=sk-or-your-key-here
```

**Windows PowerShell:**
```powershell
$env:OPENROUTER_API_KEY="sk-or-your-key-here"
```

**Linux/Mac:**
```bash
export OPENROUTER_API_KEY=sk-or-your-key-here
```

**Or set permanently** (recommended):
1. Windows Key → Search "environment variables"
2. Click "Edit the system environment variables"
3. Click "Environment Variables"
4. Click "New" under User variables
5. Name: `OPENROUTER_API_KEY`
6. Value: Your API key
7. Click OK

### Step 4: Configure Model (Optional)

Edit `email_processing.py` to choose your model:

```python
# Around line 30
if USE_OPENROUTER:
    MODEL = "openai/gpt-4o-mini"  # Change this to your preferred model
```

### Step 5: Run Workflow

```bash
python workflow.py
```

That's it! The script will now use OpenRouter instead of OpenAI directly.

---

## Available Models

Here are popular models you can use (as of 2024):

### Fast & Cheap (Good for this workflow)
- `openai/gpt-4o-mini` - $0.15/$0.60 per 1M tokens (in/out)
- `anthropic/claude-3-haiku` - $0.25/$1.25 per 1M tokens
- `google/gemini-flash-1.5` - $0.075/$0.30 per 1M tokens
- `meta-llama/llama-3.1-8b-instruct` - $0.05/$0.05 per 1M tokens (free tier available)

### High Quality (More expensive)
- `openai/gpt-4o` - $2.50/$10 per 1M tokens
- `anthropic/claude-3.5-sonnet` - $3/$15 per 1M tokens
- `google/gemini-pro-1.5` - $1.25/$5 per 1M tokens

### Free Tier Models
- `meta-llama/llama-3.1-8b-instruct:free`
- `google/gemini-flash-1.5:free` (with limits)
- Many other free options at: https://openrouter.ai/models?order=newest&supported_parameters=tools&max_price=0

**Recommended for this workflow:** `openai/gpt-4o-mini` or `google/gemini-flash-1.5`

Check latest models and pricing: https://openrouter.ai/models

---

## Cost Comparison

**Example: Processing 100 emails with gpt-4o-mini**

Via OpenRouter:
- Input: ~150,000 tokens × $0.15 = $0.02
- Output: ~70,000 tokens × $0.60 = $0.04
- **Total: ~$0.06 per 100 emails**

Via Direct OpenAI:
- Similar pricing, but OpenRouter may have promotions

**Using Gemini Flash 1.5:**
- Input: ~150,000 tokens × $0.075 = $0.01
- Output: ~70,000 tokens × $0.30 = $0.02
- **Total: ~$0.03 per 100 emails** (50% cheaper!)

---

## Switching Between OpenAI and OpenRouter

Edit `email_processing.py` around line 20:

**Use OpenRouter:**
```python
USE_OPENROUTER = True
```

**Use OpenAI directly:**
```python
USE_OPENROUTER = False
```

When using OpenAI directly, set `OPENAI_API_KEY` instead of `OPENROUTER_API_KEY`.

---

## Troubleshooting

### "OPENROUTER_API_KEY not set"
- Make sure you set the environment variable
- Close and reopen Command Prompt after setting it
- Check spelling: `OPENROUTER_API_KEY` (not `OPENAI_API_KEY`)

### "Insufficient credits"
- Add credits at: https://openrouter.ai/credits
- Check your balance at: https://openrouter.ai/activity

### "Model not found"
- Check model name at: https://openrouter.ai/models
- Make sure to use the full model path (e.g., `openai/gpt-4o-mini`)
- Model names are case-sensitive

### "Rate limit exceeded"
- Reduce `CONCURRENCY` in `email_processing.py` (try 5 instead of 10)
- Add `SLEEP_BETWEEN_BATCHES = 1` to slow down requests

---

## Advanced: Trying Different Models

You can easily experiment with different models:

1. Edit `email_processing.py`
2. Change the `MODEL` variable (line ~30)
3. Run a small test with a few emails
4. Compare quality and cost

Example:
```python
# Try Claude Haiku (Anthropic's fast model)
MODEL = "anthropic/claude-3-haiku"

# Try Gemini Flash (Google's fast model)
MODEL = "google/gemini-flash-1.5"

# Try Llama (Meta's open source model, often free)
MODEL = "meta-llama/llama-3.1-8b-instruct"
```

---

## Monitoring Usage

Track your spending:
1. Go to: https://openrouter.ai/activity
2. See detailed usage by model
3. Download usage reports

---

## Benefits of OpenRouter for This Workflow

✅ **Cost Savings**: Gemini Flash is ~50% cheaper than GPT-4o-mini
✅ **Flexibility**: Switch models without changing code
✅ **Reliability**: Automatic fallback if a model is down
✅ **Simple Billing**: One account for all AI models
✅ **No Subscriptions**: Pay only for what you use

---

## Getting Help

- OpenRouter Docs: https://openrouter.ai/docs
- Model Comparisons: https://openrouter.ai/models
- Discord Community: https://discord.gg/openrouter
- Pricing Calculator: https://openrouter.ai/models (filter by price)

---

**Recommended Setup:**
- Use OpenRouter (it's enabled by default)
- Start with `openai/gpt-4o-mini` (familiar, reliable)
- Try `google/gemini-flash-1.5` to save 50%
- Add $10 in credits to start (processes ~200-300 emails)
