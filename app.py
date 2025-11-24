"""
Gradio Web Interface for Email Processing Workflow
Provides a user-friendly UI for extracting and processing emails.

UI INPUTS AND USAGE:
====================
1. START DATE / END DATE (from UI date inputs)
   → Passed to extractor.process_folder() to filter emails by date range
   → Parsed using utils.date_utils.parse_date()

2. OUTPUT FILENAME (from UI text input)
   → Used to customize output file names (emails.xlsx, emails_processed.xlsx, etc.)
   → Passed to EmailProcessor constructor as custom filenames
   → Also used in processing to name the final output file

3. PRODUCT CATEGORIZATION LIST (from UI large textbox)
   → User can edit the product list used in AI prompts
   → Injected into email_processing.PROMPT_TEMPLATE using regex replacement
   → Allows customization without editing code

4. SKIP CHECKPOINT (from UI checkbox)
   → Controls whether workflow pauses for review after extraction
   → If unchecked: stops after extraction for manual review
   → If checked: runs extraction and processing automatically

WINDOWS COM THREADING:
======================
- Gradio runs functions in thread pools
- Windows COM (Outlook automation) requires initialization in each thread
- pythoncom.CoInitialize() called at start of extraction
- pythoncom.CoUninitialize() called in finally block

All UI inputs are actively used and affect the workflow execution.
"""
import gradio as gr
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import re

# Import workflow components
from config_loader import get_config
from config import OUTPUT_DIR, OUTPUT_FILENAME
from extractor import EmailProcessor as EmailExtractor
from utils.date_utils import parse_date

# Default product list
DEFAULT_PRODUCT_LIST = """Agitadores, Aireadores, Almacenamiento, Arqueta, Asesoramiento, Biodigestor, Biodiscos, Bombas, Canal Parshall, Cavitador CAF, Clarificadores, Colector, Compresor, Compuerta, Compuertas, Contenedor, Cuadro electrico, Cucharas bivalva, Decantador centrífugo, Decantador lamelar, Decantador SBR, Desarenador, Desarenador cicloidal, Desarenador desengrasador, Desbaste, Deshidratación purín, Deshidratador centrifugo, Deshidratador filtro pensa, Desinfección por cloración, Desnatador, Difusores, Equipo para sistema de agua desalinizada, Equipos electromecánicos, Equipos pretratamiento y espesamiento, Estudios, Evaporadaror, Fabricación planta tratamiento, Filtración, Filtro carbon activado, Filtro prensa, Floculador, Floculante, Generador de microburbuja, Generador de Ozono, Instrumentación, Inyector, Mantenimiento, Membranas MBR, Mezclador, Osmosis inversa, Pasamuro, Planta de biogás, Planta de pretratamiento, Planta de pretratamiento compacta, Planta de tratamiento, Planta pilloto, Planta poli, Planta tratamiento compacta, PLC de control, Polipastos, Polymer feed pump, Pozo de bombeos, pressure booster pump, Reja de desbaste, Reja desbaste, Rental and, Repuestos Tornillo deshidratador de lodo, Sacor filtrantes, Separador de grasas, Separador de hidrocarburos, Separador solido liquido, Separadores de lodos ciclónicos, Silo decantador, Sinfin, Sistema CAF, Sistema coagulacion floculación, Sistema DAF, sistema de extracción de lodos, Sistema de medición continua, Sistema de neutralización de gas clorado, Sistema de ultrafiltración, Sistema desalinización, Sistema desodorización, Sistema electroquimico, Sistema FCM, Sistema llenado botellas, Sistema lodos activados, Sistema MBBR, Sistema MBR, Sistema SBR, Soplante, Tamiz compactador, Tamiz de aliviadero, Tamiz rotativo, Tanque de mazcla, Tanque de tormentas, Tolva, Tornillo deshidratador de lodo, Tratamiento biológico, Tratamiento reactores secuenciales, Tratamiento terciario, Tubos, Valvulas, Varios"""


def load_config():
    """Load configuration and return key settings."""
    try:
        config = get_config()
        extraction_config = config.get_section('extraction')
        processing_config = config.get_section('processing')

        return {
            'email': extraction_config.get('target_account_email', 'Not configured'),
            'folder': extraction_config.get('target_folder_name', 'Not configured'),
            'subfolder': extraction_config.get('target_subfolder_name', ''),
            'model': processing_config.get('model', 'openai/gpt-4o-mini'),
            'output_dir': extraction_config.get('output_dir', 'outputs')
        }
    except Exception as e:
        return {'error': str(e)}


def run_extraction(start_date, end_date, output_name, progress=gr.Progress()):
    """
    Run email extraction phase.

    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        output_name: Custom name for output files
        progress: Gradio progress tracker

    Returns:
        Tuple of (status_message, extracted_file_path, statistics)
    """
    try:
        # Initialize COM for Windows threading (required for Outlook automation in Gradio threads)
        import sys
        if sys.platform == 'win32':
            import pythoncom
            pythoncom.CoInitialize()

        progress(0, desc="Starting extraction...")

        # UI INPUT 1: Parse start_date and end_date from UI date inputs
        start_dt = parse_date(start_date) if start_date else None
        end_dt = parse_date(end_date) if end_date else None

        # Validate dates
        if start_dt and end_dt and start_dt > end_dt:
            return "❌ Error: Start date must be before end date", None, None

        progress(0.2, desc="Connecting to Outlook...")

        # UI INPUT 2: Use custom output_name from UI to create filenames
        output_file = f"{output_name}.xlsx" if output_name else "emails.xlsx"
        excluded_file = f"{output_name}_excluded.xlsx" if output_name else "emails_excluded.xlsx"
        errors_file = f"{output_name}_errors.xlsx" if output_name else "emails_errors.xlsx"

        progress(0.3, desc="Extracting emails from Outlook...")

        # Import and create extractor with custom filenames
        from extractor import EmailProcessor
        import config

        # Initialize processor with custom filenames (if provided)
        if output_name:
            processor = EmailProcessor(
                output_filename=output_file,
                excluded_filename=excluded_file,
                errors_filename=errors_file
            )
        else:
            processor = EmailProcessor()

        # Pass date filters from UI to extractor
        processor.process_folder(start_dt, end_dt)

        progress(1.0, desc="Extraction complete!")

        # Get statistics from extracted file
        output_path = os.path.join(config.OUTPUT_DIR, output_file)
        if os.path.exists(output_path):
            df = pd.read_excel(output_path)
            stats = f"✅ Extracted {len(df)} emails\n📁 Saved to: {output_path}"
            return stats, output_path, len(df)
        else:
            return "⚠️ Extraction completed but no output file found", None, 0

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"❌ Error during extraction: {str(e)}\n\nDetails:\n{error_details}", None, None
    finally:
        # Uninitialize COM
        if sys.platform == 'win32':
            pythoncom.CoUninitialize()


def run_processing(extracted_file, output_name, product_list, progress=gr.Progress()):
    """
    Run AI processing phase with custom product list from UI.

    Args:
        extracted_file: Path to extracted emails file
        output_name: Custom name for output file
        product_list: Custom product categorization list from UI
        progress: Gradio progress tracker

    Returns:
        Tuple of (status_message, processed_file_path)
    """
    try:
        # Handle case where extracted_file is None (user skipped extraction)
        if not extracted_file:
            default_file = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
            if os.path.exists(default_file):
                extracted_file = default_file
                progress(0.1, desc=f"Using default file: {OUTPUT_FILENAME}")
            else:
                return "❌ Error: No extracted emails file found. Run extraction first.", None
        elif not os.path.exists(extracted_file):
             return "❌ Error: No extracted emails file found. Run extraction first.", None

        progress(0, desc="Loading extracted emails...")

        # Load emails
        df = pd.read_excel(extracted_file)
        total = len(df)

        if total == 0:
            return "⚠️ No emails to process", None

        progress(0.2, desc=f"Preparing AI analysis with custom product list...")

        # Import email processing module
        from email_processing import AIProcessor
        
        # Initialize processor
        processor = AIProcessor()

        # UI INPUT 3: Apply custom product_list from UI to AI prompt
        if product_list.strip():
            processor.update_product_list(product_list)

        progress(0.3, desc=f"Processing {total} emails with AI...")

        # Run async processing
        import asyncio
        results = asyncio.run(processor.process_all_emails(df))

        progress(0.8, desc="Parsing AI responses...")

        # Parse results
        parsed = [processor.parse_json(json_str) for json_str in results]
        df_parsed = pd.DataFrame(parsed)

        # Merge with original data
        df_final = pd.concat([df.reset_index(drop=True), df_parsed], axis=1)

        # UI INPUT 2: Use custom output_name from UI for processed file
        output_file = f"{output_name}_processed.xlsx" if output_name else "emails_processed.xlsx"
        output_path = os.path.join('outputs', output_file)

        os.makedirs('outputs', exist_ok=True)
        df_final.to_excel(output_path, index=False)

        progress(1.0, desc="Processing complete!")

        stats = f"✅ Processed {len(df_final)} emails\n📁 Saved to: {output_path}"
        return stats, output_path

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"❌ Error during processing: {str(e)}\n\nDetails:\n{error_details}", None


def run_full_workflow(start_date, end_date, output_name, product_list,
                     skip_checkpoint, progress=gr.Progress()):
    """
    Run complete workflow: extraction + processing.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        output_name: Custom output filename
        product_list: Product categorization list
        skip_checkpoint: If True, auto-process without review
        progress: Gradio progress tracker

    Returns:
        Status message and file paths
    """
    # Step 1: Extraction
    progress(0, desc="Phase 1: Extracting emails...")
    extract_status, extracted_file, count = run_extraction(
        start_date, end_date, output_name, progress
    )

    if not extracted_file:
        return extract_status, None, None

    # UI INPUT 4: Check skip_checkpoint from UI checkbox
    if not skip_checkpoint:
        # User wants to review extraction before processing
        checkpoint_msg = f"\n\n⏸️ CHECKPOINT\nPlease review: {extracted_file}\n\nClick 'Process Emails' to continue with AI analysis."
        return extract_status + checkpoint_msg, extracted_file, None

    # Step 2: Processing (auto-process when skip_checkpoint is True)
    progress(0.5, desc="Phase 2: Processing with AI...")
    process_status, processed_file = run_processing(
        extracted_file, output_name, product_list, progress
    )

    final_status = f"{extract_status}\n\n{process_status}"
    return final_status, extracted_file, processed_file


def create_interface():
    """Create and configure Gradio interface."""

    # Load current config
    config_info = load_config()

    # Define interface
    with gr.Blocks(title="Email Processing Workflow", theme=gr.themes.Soft()) as interface:

        gr.Markdown("# 📧 Email Processing Workflow")
        gr.Markdown("Extract and process emails from Outlook with AI analysis")

        # Configuration display
        with gr.Accordion("📋 Current Configuration", open=False):
            gr.Markdown(f"""
            - **Email Account:** `{config_info.get('email', 'Not configured')}`
            - **Target Folder:** `{config_info.get('folder', 'Not configured')}`
            - **Subfolder:** `{config_info.get('subfolder', 'None')}`
            - **AI Model:** `{config_info.get('model', 'Not configured')}`

            *To change these settings, edit `workflow_config.yaml`*
            """)

        # Main controls
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ Settings")

                # Date selection
                today = datetime.now()
                week_ago = today - timedelta(days=7)

                start_date = gr.Textbox(
                    label="Start Date (YYYY-MM-DD)",
                    value=week_ago.strftime("%Y-%m-%d"),
                    placeholder="2024-01-01"
                )

                end_date = gr.Textbox(
                    label="End Date (YYYY-MM-DD)",
                    value=today.strftime("%Y-%m-%d"),
                    placeholder="2024-12-31"
                )

                # Output filename
                output_name = gr.Textbox(
                    label="Output Filename (without extension)",
                    value="",
                    placeholder="emails (leave empty for default)"
                )

                # Checkpoint option
                skip_checkpoint = gr.Checkbox(
                    label="Skip checkpoint (auto-process)",
                    value=False,
                    info="If unchecked, workflow pauses for review"
                )

            with gr.Column(scale=2):
                gr.Markdown("### 📝 Product Categorization List")
                gr.Markdown("*Edit this list to customize AI product categorization*")

                product_list = gr.Textbox(
                    label="Products (comma-separated)",
                    value=DEFAULT_PRODUCT_LIST,
                    lines=10,
                    max_lines=15,
                    info="Add or remove products from this list"
                )

        # Action buttons
        gr.Markdown("---")
        with gr.Row():
            extract_btn = gr.Button("📥 Extract Emails", variant="primary", scale=1)
            process_btn = gr.Button("🤖 Process Emails", variant="secondary", scale=1)
            full_btn = gr.Button("▶️ Run Full Workflow", variant="primary", scale=2)

        # Status and results
        gr.Markdown("### 📊 Results")

        status_output = gr.Textbox(
            label="Status",
            lines=8,
            max_lines=15,
            interactive=False
        )

        with gr.Row():
            extracted_file = gr.File(label="📄 Extracted Emails", interactive=False)
            processed_file = gr.File(label="⭐ Processed Emails (Final)", interactive=False)

        # Button actions
        extract_btn.click(
            fn=run_extraction,
            inputs=[start_date, end_date, output_name],
            outputs=[status_output, extracted_file, gr.State()]
        )

        process_btn.click(
            fn=run_processing,
            inputs=[extracted_file, output_name, product_list],
            outputs=[status_output, processed_file]
        )

        full_btn.click(
            fn=run_full_workflow,
            inputs=[start_date, end_date, output_name, product_list, skip_checkpoint],
            outputs=[status_output, extracted_file, processed_file]
        )

        # Help section
        with gr.Accordion("❓ Help", open=False):
            gr.Markdown("""
            ### How to Use

            1. **Set Date Range**: Choose start and end dates for email extraction
            2. **Customize Output**: (Optional) Set a custom filename
            3. **Edit Product List**: (Optional) Modify the product categories
            4. **Run Workflow**:
               - **Extract Emails**: Only extract from Outlook
               - **Process Emails**: Process already extracted emails
               - **Run Full Workflow**: Do both (with optional checkpoint)

            ### Workflow Phases

            **Phase 1: Extraction**
            - Connects to Outlook
            - Extracts emails from configured folder
            - Filters by date range
            - Saves to Excel

            **Phase 2: Processing** (if not skipped)
            - Analyzes emails with AI
            - Extracts company information
            - Categorizes products
            - Adds technical specifications

            ### Checkpoint

            If "Skip checkpoint" is unchecked:
            - Workflow pauses after extraction
            - Review the extracted file
            - Click "Process Emails" to continue

            If checked:
            - Runs extraction and processing automatically
            - No manual review step

            ### Output Files

            - **Extracted Emails**: Raw extracted data
            - **Processed Emails**: Final output with AI analysis ⭐

            Both files can be downloaded from this interface.

            ### Troubleshooting

            - **"Outlook not running"**: Open Outlook before extracting
            - **"Folder not found"**: Check `workflow_config.yaml` settings
            - **"API error"**: Check `.env` file has valid API key

            See `docs/GETTING_STARTED.md` for detailed help.
            """)

    return interface


def main():
    """Launch Gradio interface."""
    # Check dependencies
    try:
        import gradio
    except ImportError:
        print("❌ Gradio not installed. Install with: pip install gradio")
        sys.exit(1)

    # Check configuration
    if not os.path.exists('workflow_config.yaml'):
        print("⚠️ Warning: workflow_config.yaml not found")
        print("   Run: python setup_config.py")
        print()

    if not os.path.exists('.env'):
        print("⚠️ Warning: .env file not found")
        print("   Run: python setup_config.py")
        print()

    # Create and launch interface
    print("🚀 Starting Email Processing Workflow UI...")
    print("📍 Access at: http://localhost:7860")
    print()

    interface = create_interface()
    interface.queue()  # Enable queuing for long-running tasks
    interface.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=False,  # Set to True for public sharing
        show_error=True
    )


if __name__ == "__main__":
    main()
