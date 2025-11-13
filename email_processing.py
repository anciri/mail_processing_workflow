"""
Email Processing Script - Analyzes extracted emails using AI API
Processes emails from the extractor output and enriches them with AI analysis.
Supports both OpenAI and OpenRouter.
"""
import asyncio
import pandas as pd
import re
import time
import os
from xml.etree import ElementTree as ET
from openai import AsyncOpenAI
from tenacity import retry, wait_exponential, stop_after_attempt
from config_loader import get_config

# === LOAD CONFIGURATION ===
config = get_config()
processing_config = config.get_section('processing')

# Input/Output files
INPUT_EXCEL = processing_config.get('input_file', 'outputs/emails.xlsx')
OUTPUT_EXCEL = processing_config.get('output_file', 'outputs/emails_processed.xlsx')

# API Configuration
USE_OPENROUTER = config.should_use_openrouter()
MODEL = processing_config.get('model', 'openai/gpt-4o-mini')

# Processing settings
MAX_TOKENS = processing_config.get('max_tokens', 700)
CONCURRENCY = processing_config.get('concurrency', 10)
SLEEP_BETWEEN_BATCHES = processing_config.get('sleep_between_batches', 0)

# Retry settings
RETRY_ATTEMPTS = processing_config.get('retry_attempts', 3)
RETRY_MIN_WAIT = processing_config.get('retry_min_wait', 2)
RETRY_MAX_WAIT = processing_config.get('retry_max_wait', 20)

# === PROMPT TEMPLATE ===
PROMPT_TEMPLATE = """You will be analyzing email data extracted from business correspondence related to water treatment equipment and solutions. The data contains fields such as ID, From_Name, Subject, Body, and other relevant information.

<email_data>
{EMAIL_DATA}
</email_data>

Your task is to analyze each email record and extract specific information primarily from the "Subject" and "Body" fields, focusing on emails that are requests for quotations of water treatment equipment or solutions.

**Product Categorization List:**
When identifying equipment or products, you should categorize them using items from this preferred list whenever possible:
Agitadores, Aireadores, Almacenamiento, Arqueta, Asesoramiento, Biodigestor, Biodiscos, Bombas, Canal Parshall, Cavitador CAF, Clarificadores, Colector, Compresor, Compuerta, Compuertas, Contenedor, Cuadro electrico, Cucharas bivalva, Decantador centrífugo, Decantador lamelar, Decantador SBR, Desarenador, Desarenador cicloidal, Desarenador desengrasador, Desbaste, Deshidratación purín, Deshidratador centrifugo, Deshidratador filtro pensa, Desinfección por cloración, Desnatador, Difusores, Equipo para sistema de agua desalinizada, Equipos electromecánicos, Equipos pretratamiento y espesamiento, Estudios, Evaporadaror, Fabricación planta tratamiento, Filtración, Filtro carbon activado, Filtro prensa, Floculador, Floculante, Generador de microburbuja, Generador de Ozono, Instrumentación, Inyector, Mantenimiento, Membranas MBR, Mezclador, Osmosis inversa, Pasamuro, Planta de biogás, Planta de pretratamiento, Planta de pretratamiento compacta, Planta de tratamiento, Planta pilloto, Planta poli, Planta tratamiento compacta, PLC de control, Polipastos, Polymer feed pump, Pozo de bombeos, pressure booster pump, Reja de desbaste, Reja desbaste, Rental and, Repuestos Tornillo deshidratador de lodo, Sacor filtrantes, Separador de grasas, Separador de hidrocarburos, Separador solido liquido, Separadores de lodos ciclónicos, Silo decantador, Sinfin, Sistema CAF, Sistema coagulacion floculación, Sistema DAF, sistema de extracción de lodos, Sistema de medición continua, Sistema de neutralización de gas clorado, Sistema de ultrafiltración, Sistema desalinización, Sistema desodorización, Sistema electroquimico, Sistema FCM, Sistema llenado botellas, Sistema lodos activados, Sistema MBBR, Sistema MBR, Sistema SBR, Soplante, Tamiz compactador, Tamiz de aliviadero, Tamiz rotativo, Tanque de mazcla, Tanque de tormentas, Tolva, Tornillo deshidratador de lodo, Tratamiento biológico, Tratamiento reactores secuenciales, Tratamiento terciario, Tubos, Valvulas, Varios.

**Information Extraction Requirements:**

For each email record, extract and categorize the following:

**Company Information (from Body field):**
- Company name
- Website (if mentioned)
- Country of the sending company

**Email Categorization:**
Classify each email into one of these categories:
- "Solución de tratamiento compleja" (Complex treatment solution)
- "Productos" (Products)

**Equipment Information:**
- Identify the type of equipment being requested, preferably selecting from the categorization list above
- Cross-reference information from both Subject and Body fields
- Note any specific technical requirements or specifications mentioned

**Analysis Process:**
1. First examine the Subject field for initial equipment type indicators
2. Then analyze the Body field for detailed equipment specifications and company information
3. Always cross-reference Subject and Body content to ensure accuracy
4. Look for keywords related to water treatment such as: filtration, purification, desalination, reverse osmosis, water treatment plants, pumps, filters, membranes, etc.
5. When categorizing products, match them to the provided categorization list whenever possible

**Output Format:**
For each email record, provide your analysis in the following structure:

<analysis>
<record_id>[ID from the data]</record_id>
<company_info>
<name>[Company name or "Not specified"]</name>
<website>[Website URL or "Not mentioned"]</website>
<country>[Country or "Not specified"]</country>
</company_info>
<email_category>[Solución de tratamiento compleja/Productos]</email_category>
<product_category>[Category from the provided list, or "Other" if not found in list]</product_category>
<equipment_requested>[Detailed description of equipment/solution requested]</equipment_requested>
<technical_specifications>[Any specific technical requirements mentioned or "None specified"]</technical_specifications>
<subject_body_correlation>[Brief note on how Subject and Body information align or differ]</subject_body_correlation>
</analysis>

**Important Guidelines:**
- If company information is not clearly stated in the Body field, mark as "Not specified"
- When equipment type is unclear, provide your best assessment based on available context
- Always prioritize information from the Body field over Subject when there are discrepancies
- Focus only on emails that appear to be genuine business inquiries for water treatment solutions
- When selecting product categories, prioritize exact matches from the provided list, then close matches, and only use "Other" when no reasonable match exists

Provide only the structured analysis for each email record as specified above, with no additional commentary or explanations outside the analysis tags.
"""

# === BUILD EMAIL XML BLOCK ===
def build_email_block(row, idx):
    """Build XML block for a single email."""
    return (
        f"<ID>{idx+1}</ID>\n"
        f"<From_Name>{row.get('From_Name','')}</From_Name>\n"
        f"<From_Email>{row.get('From_Email','')}</From_Email>\n"
        f"<To>{row.get('To','')}</To>\n"
        f"<Date>{row.get('Date','')}</Date>\n"
        f"<Subject>{row.get('Subject','')}</Subject>\n"
        f"<Body>{row.get('Body','')}</Body>"
    )

# === CLIENT INIT (async) ===
# Get API key from environment (loaded via config_loader)
try:
    api_key, key_type = config.get_api_key()
except ValueError as e:
    print(str(e))
    exit(1)

# Initialize client based on configuration
if USE_OPENROUTER:
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://github.com/anciri/mail_processing_workflow",
            "X-Title": "Email Processing Workflow"
        }
    )
    print(f"🔄 Using OpenRouter with model: {MODEL}")
else:
    client = AsyncOpenAI(api_key=api_key)
    print(f"🤖 Using OpenAI directly with model: {MODEL}")

# === RETRY DECORATOR ===
@retry(
    wait=wait_exponential(multiplier=1, min=RETRY_MIN_WAIT, max=RETRY_MAX_WAIT),
    stop=stop_after_attempt(RETRY_ATTEMPTS)
)
async def analyze_email(idx, row):
    """Single async API call with retry."""
    email_data = build_email_block(row, idx)
    prompt = PROMPT_TEMPLATE.format(EMAIL_DATA=email_data)

    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS,
            temperature=0
        )
        content = response.choices[0].message.content

        # Validate response
        if not content:
            print(f"⚠️  Empty response for email {idx+1}")
            return "<analysis><record_id>error</record_id><company_info><name>Empty response</name></company_info></analysis>"

        content = content.strip()

        # Check if response contains XML
        if not content.startswith("<analysis>"):
            print(f"⚠️  Invalid format for email {idx+1} - response doesn't start with <analysis>")
            print(f"   First 100 chars: {content[:100]}")
            # Try to extract XML if it's embedded in text
            if "<analysis>" in content:
                start_idx = content.find("<analysis>")
                end_idx = content.find("</analysis>") + len("</analysis>")
                if end_idx > start_idx:
                    content = content[start_idx:end_idx]
            else:
                return "<analysis><record_id>error</record_id><company_info><name>Invalid XML format</name></company_info></analysis>"

        return content
    except Exception as e:
        print(f"❌ Error on email {idx+1}: {e}")
        return "<analysis><record_id>error</record_id><company_info><name>API Error</name></company_info></analysis>"

# === PARSE XML RESPONSE ===
def parse_xml(xml_text):
    """Parse XML response from AI API."""
    # Handle empty or None responses
    if not xml_text:
        print(f"⚠️  XML parse error: Empty or None response")
        return {
            "record_id": "Empty response",
            "company_name": "N/A",
            "company_website": "N/A",
            "company_country": "N/A",
            "email_category": "N/A",
            "product_category": "N/A",
            "equipment_requested": "N/A",
            "technical_specifications": "N/A",
            "subject_body_correlation": "N/A"
        }

    try:
        # Remove control characters
        xml_clean = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", xml_text)

        # Check if cleaned text is empty
        if not xml_clean.strip():
            print(f"⚠️  XML parse error: Empty after cleaning")
            return {
                "record_id": "Empty after cleaning",
                "company_name": "N/A",
                "company_website": "N/A",
                "company_country": "N/A",
                "email_category": "N/A",
                "product_category": "N/A",
                "equipment_requested": "N/A",
                "technical_specifications": "N/A",
                "subject_body_correlation": "N/A"
            }

        root = ET.fromstring(xml_clean)
        return {
            "record_id": root.findtext("record_id", "Not found"),
            "company_name": root.findtext("company_info/name", "Not specified"),
            "company_website": root.findtext("company_info/website", "Not mentioned"),
            "company_country": root.findtext("company_info/country", "Not specified"),
            "email_category": root.findtext("email_category", "Not specified"),
            "product_category": root.findtext("product_category", "Not specified"),
            "equipment_requested": root.findtext("equipment_requested", "Not specified"),
            "technical_specifications": root.findtext("technical_specifications", "None specified"),
            "subject_body_correlation": root.findtext("subject_body_correlation", "Not specified")
        }
    except ET.ParseError as e:
        print(f"⚠️  XML parse error: {e}")
        print(f"   XML preview (first 200 chars): {xml_text[:200]}")
        return {
            "record_id": "XML parse error",
            "company_name": "Parse error",
            "company_website": "Parse error",
            "company_country": "Parse error",
            "email_category": "Parse error",
            "product_category": "Parse error",
            "equipment_requested": "Parse error",
            "technical_specifications": "Parse error",
            "subject_body_correlation": "Parse error"
        }
    except Exception as e:
        print(f"⚠️  Unexpected error parsing XML: {e}")
        return {
            "record_id": "Unexpected error",
            "company_name": "Error",
            "company_website": "Error",
            "company_country": "Error",
            "email_category": "Error",
            "product_category": "Error",
            "equipment_requested": "Error",
            "technical_specifications": "Error",
            "subject_body_correlation": "Error"
        }

# === ASYNC BATCH PROCESSING ===
async def process_batch(batch_indices, df):
    """Process a batch of emails concurrently."""
    tasks = [analyze_email(idx, df.iloc[idx]) for idx in batch_indices]
    results = await asyncio.gather(*tasks)
    return results

async def process_all_emails(df):
    """Process all emails in batches with concurrency control."""
    total = len(df)
    all_results = []

    print(f"🚀 Processing {total} emails with concurrency={CONCURRENCY}...")

    for i in range(0, total, CONCURRENCY):
        batch_end = min(i + CONCURRENCY, total)
        batch_indices = list(range(i, batch_end))

        print(f"📧 Processing batch {i+1}-{batch_end} of {total}...")
        batch_results = await process_batch(batch_indices, df)
        all_results.extend(batch_results)

        if SLEEP_BETWEEN_BATCHES > 0 and batch_end < total:
            await asyncio.sleep(SLEEP_BETWEEN_BATCHES)

    return all_results

# === MAIN FUNCTION ===
def main():
    """Main entry point for email processing."""
    print("=" * 60)
    print("EMAIL PROCESSING WITH AI ANALYSIS")
    print("=" * 60)

    # Check if input file exists
    if not os.path.exists(INPUT_EXCEL):
        print(f"❌ Error: Input file '{INPUT_EXCEL}' not found!")
        print(f"   Please run the extractor script first to generate the input file.")
        return 1

    # Load input Excel
    print(f"📂 Loading input file: {INPUT_EXCEL}")
    try:
        df = pd.read_excel(INPUT_EXCEL)
        print(f"✅ Loaded {len(df)} email records")
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        return 1

    if len(df) == 0:
        print("⚠️  No emails to process!")
        return 0

    # Process emails asynchronously
    start_time = time.time()
    xml_results = asyncio.run(process_all_emails(df))

    # Parse XML results
    print("\n📊 Parsing AI analysis results...")
    parsed_results = [parse_xml(xml_text) for xml_text in xml_results]

    # Create output DataFrame
    df_parsed = pd.DataFrame(parsed_results)

    # Merge with original data
    df_final = pd.concat([df.reset_index(drop=True), df_parsed], axis=1)

    # Save output
    os.makedirs(os.path.dirname(OUTPUT_EXCEL), exist_ok=True)
    df_final.to_excel(OUTPUT_EXCEL, index=False)

    elapsed_time = time.time() - start_time

    # Print summary
    print("\n" + "=" * 60)
    print("✅ PROCESSING COMPLETE!")
    print("=" * 60)
    print(f"📊 Total emails processed: {len(df_final)}")
    print(f"⏱️  Time elapsed: {elapsed_time:.2f} seconds")
    print(f"💾 Output saved to: {OUTPUT_EXCEL}")
    print("=" * 60)

    return 0

if __name__ == "__main__":
    exit(main())
