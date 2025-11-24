import json
import logging
import asyncio
import pandas as pd
import re
import time
import os
from openai import AsyncOpenAI
from tenacity import retry, wait_exponential, stop_after_attempt
from config_loader import get_config
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# Configure logging
logger = logging.getLogger(__name__)

class AIProcessor:
    """
    Handles the AI processing of emails using OpenAI or OpenRouter.
    """
    def __init__(self):
        """Initialize the AI Processor with configuration."""
        self.config = get_config()
        self.processing_config = self.config.get_section('processing')
        
        # API Configuration
        self.use_openrouter = self.config.should_use_openrouter()
        self.model = self.processing_config.get('model', 'openai/gpt-4o-mini')
        
        # Processing settings
        self.max_tokens = self.processing_config.get('max_tokens', 1000)
        self.concurrency = self.processing_config.get('concurrency', 10)
        self.sleep_between_batches = self.processing_config.get('sleep_between_batches', 0)
        
        # Retry settings
        self.retry_attempts = self.processing_config.get('retry_attempts', 3)
        self.retry_min_wait = self.processing_config.get('retry_min_wait', 2)
        self.retry_max_wait = self.processing_config.get('retry_max_wait', 20)
        
        # Initialize client
        self._init_client()
        
        # Prompt Template
        self.prompt_template = USER_PROMPT_TEMPLATE

    def update_product_list(self, product_list_str):
        """Update the product list in the prompt template."""
        if not product_list_str or not product_list_str.strip():
            return

        import re
        # Use regex to find and replace the product categorization list in the prompt
        product_list_pattern = r'(When identifying equipment or products.*?:\n)(.*?)(\n\n\*\*Analysis Instructions)'
        
        replacement = r'\1' + product_list_str.strip() + r'.\3'
        
        self.prompt_template = re.sub(
            product_list_pattern,
            replacement,
            self.prompt_template,
            flags=re.DOTALL
        )
        logger.info("✅ Updated AI prompt with custom product list")

    def _init_client(self):
        """Initialize the AsyncOpenAI client."""
        try:
            api_key, key_type = self.config.get_api_key()
        except ValueError as e:
            logger.error(str(e))
            raise

        if self.use_openrouter:
            self.client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                default_headers={
                    "HTTP-Referer": "https://github.com/anciri/mail_processing_workflow",
                    "X-Title": "Email Processing Workflow"
                }
            )
            logger.info(f"🔄 Using OpenRouter with model: {self.model}")
        else:
            self.client = AsyncOpenAI(api_key=api_key)
            logger.info(f"🤖 Using OpenAI directly with model: {self.model}")

    def build_email_block(self, row, idx):
        """Build text block for a single email."""
        return (
            f"ID: {idx+1}\n"
            f"From Name: {row.get('From_Name','')}\n"
            f"From Email: {row.get('From_Email','')}\n"
            f"To: {row.get('To','')}\n"
            f"Date: {row.get('Date','')}\n"
            f"Subject: {row.get('Subject','')}\n"
            f"Body: {row.get('Body','')}"
        )

    async def analyze_email(self, idx, row):
        """Single async API call with retry expecting JSON response."""
        email_data = self.build_email_block(row, idx)
        prompt = self.prompt_template.format(EMAIL_DATA=email_data)

        # Create a retry-decorated function
        @retry(
            wait=wait_exponential(multiplier=1, min=self.retry_min_wait, max=self.retry_max_wait),
            stop=stop_after_attempt(self.retry_attempts)
        )
        async def _make_request():
            return await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0,
                response_format={"type": "json_object"}
            )

        try:
            response = await _make_request()
            content = response.choices[0].message.content

            # Validate response
            if not content:
                logger.warning(f"⚠️  Empty response for email {idx+1}")
                return json.dumps({"record_id": "error", "company_info": {"name": "Empty response"}})

            return content
        except Exception as e:
            logger.error(f"❌ Error on email {idx+1}: {e}")
            return json.dumps({"record_id": "error", "company_info": {"name": "API Error"}})

    def parse_json(self, json_text):
        """Parse JSON response from AI API."""
        # Handle empty or None responses
        if not json_text:
            return self._get_empty_parsed_result("Empty or None response")

        try:
            data = json.loads(json_text)
            
            # Ensure all fields exist with defaults
            company_info = data.get("company_info", {})
            
            return {
                "record_id": data.get("record_id", "Not found"),
                "company_name": company_info.get("name", "Not specified"),
                "company_website": company_info.get("website", "Not mentioned"),
                "company_country": company_info.get("country", "Not specified"),
                "email_category": data.get("email_category", "Not specified"),
                "product_category": data.get("product_category", "Not specified"),
                "equipment_requested": data.get("equipment_requested", "Not specified"),
                "technical_specifications": data.get("technical_specifications", "None specified"),
                "subject_body_correlation": data.get("subject_body_correlation", "Not specified")
            }
        except json.JSONDecodeError as e:
            logger.warning(f"⚠️  JSON parse error: {e}")
            return self._get_empty_parsed_result("JSON parse error")
        except Exception as e:
            logger.error(f"⚠️  Unexpected error parsing JSON: {e}")
            return self._get_empty_parsed_result("Unexpected error")

    def _get_empty_parsed_result(self, reason):
        """Return a dict with default values for failed parsing."""
        return {
            "record_id": reason,
            "company_name": "Error",
            "company_website": "Error",
            "company_country": "Error",
            "email_category": "Error",
            "product_category": "Error",
            "equipment_requested": "Error",
            "technical_specifications": "Error",
            "subject_body_correlation": "Error"
        }

    async def process_batch(self, batch_indices, df):
        """Process a batch of emails concurrently."""
        tasks = [self.analyze_email(idx, df.iloc[idx]) for idx in batch_indices]
        results = await asyncio.gather(*tasks)
        return results

    async def process_all_emails(self, df):
        """Process all emails in batches with concurrency control."""
        total = len(df)
        all_results = []

        logger.info(f"🚀 Processing {total} emails with concurrency={self.concurrency}...")

        for i in range(0, total, self.concurrency):
            batch_end = min(i + self.concurrency, total)
            batch_indices = list(range(i, batch_end))

            logger.info(f"📧 Processing batch {i+1}-{batch_end} of {total}...")
            batch_results = await self.process_batch(batch_indices, df)
            all_results.extend(batch_results)

            if self.sleep_between_batches > 0 and batch_end < total:
                await asyncio.sleep(self.sleep_between_batches)

        return all_results

    def process_emails(self, input_file=None, output_file=None):
        """
        Main entry point for processing emails.
        
        Args:
            input_file: Path to input Excel file (optional, defaults to config)
            output_file: Path to output Excel file (optional, defaults to config)
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Use config defaults if not provided
        input_path = input_file or self.processing_config.get('input_file', 'outputs/emails.xlsx')
        output_path = output_file or self.processing_config.get('output_file', 'outputs/emails_processed.xlsx')

        logger.info("=" * 60)
        logger.info("EMAIL PROCESSING WITH AI ANALYSIS")
        logger.info("=" * 60)

        # Check if input file exists
        if not os.path.exists(input_path):
            logger.error(f"❌ Error: Input file '{input_path}' not found!")
            logger.error(f"   Please run the extractor script first to generate the input file.")
            return False

        # Load input Excel
        logger.info(f"📂 Loading input file: {input_path}")
        try:
            df = pd.read_excel(input_path)
            logger.info(f"✅ Loaded {len(df)} email records")
        except Exception as e:
            logger.error(f"❌ Error loading Excel file: {e}")
            return False

        if len(df) == 0:
            logger.warning("⚠️  No emails to process!")
            return True

        # Process emails asynchronously
        start_time = time.time()
        xml_results = asyncio.run(self.process_all_emails(df))

        # Parse JSON results
        logger.info("\n📊 Parsing AI analysis results...")
        parsed_results = [self.parse_json(json_text) for json_text in xml_results]

        # Create output DataFrame
        df_parsed = pd.DataFrame(parsed_results)

        # Merge with original data
        df_final = pd.concat([df.reset_index(drop=True), df_parsed], axis=1)

        # Save output
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df_final.to_excel(output_path, index=False)
        except Exception as e:
            logger.error(f"❌ Error saving output file: {e}")
            return False

        elapsed_time = time.time() - start_time

        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("✅ PROCESSING COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"📊 Total emails processed: {len(df_final)}")
        logger.info(f"⏱️  Time elapsed: {elapsed_time:.2f} seconds")
        logger.info(f"💾 Output saved to: {output_path}")
        logger.info("=" * 60)

        return True

def main():
    """CLI entry point."""
    # Configure basic logging for CLI usage
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    
    try:
        processor = AIProcessor()
        success = processor.process_emails()
        return 0 if success else 1
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
