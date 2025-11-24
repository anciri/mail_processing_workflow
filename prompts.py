"""
Prompts and schemas for AI email processing.
"""

SYSTEM_PROMPT = """You are an expert AI analyst specializing in processing business emails related to water treatment equipment and solutions.
Your task is to analyze email content and extract structured data in JSON format.
"""

USER_PROMPT_TEMPLATE = """You will be analyzing email data extracted from business correspondence.

<email_data>
{EMAIL_DATA}
</email_data>

**Product Categorization List:**
When identifying equipment or products, categorize them using items from this preferred list whenever possible:
Agitadores, Aireadores, Almacenamiento, Arqueta, Asesoramiento, Biodigestor, Biodiscos, Bombas, Canal Parshall, Cavitador CAF, Clarificadores, Colector, Compresor, Compuerta, Compuertas, Contenedor, Cuadro electrico, Cucharas bivalva, Decantador centrífugo, Decantador lamelar, Decantador SBR, Desarenador, Desarenador cicloidal, Desarenador desengrasador, Desbaste, Deshidratación purín, Deshidratador centrifugo, Deshidratador filtro pensa, Desinfección por cloración, Desnatador, Difusores, Equipo para sistema de agua desalinizada, Equipos electromecánicos, Equipos pretratamiento y espesamiento, Estudios, Evaporadaror, Fabricación planta tratamiento, Filtración, Filtro carbon activado, Filtro prensa, Floculador, Floculante, Generador de microburbuja, Generador de Ozono, Instrumentación, Inyector, Mantenimiento, Membranas MBR, Mezclador, Osmosis inversa, Pasamuro, Planta de biogás, Planta de pretratamiento, Planta de pretratamiento compacta, Planta de tratamiento, Planta pilloto, Planta poli, Planta tratamiento compacta, PLC de control, Polipastos, Polymer feed pump, Pozo de bombeos, pressure booster pump, Reja de desbaste, Reja desbaste, Rental and, Repuestos Tornillo deshidratador de lodo, Sacor filtrantes, Separador de grasas, Separador de hidrocarburos, Separador solido liquido, Separadores de lodos ciclónicos, Silo decantador, Sinfin, Sistema CAF, Sistema coagulacion floculación, Sistema DAF, sistema de extracción de lodos, Sistema de medición continua, Sistema de neutralización de gas clorado, Sistema de ultrafiltración, Sistema desalinización, Sistema desodorización, Sistema electroquimico, Sistema FCM, Sistema llenado botellas, Sistema lodos activados, Sistema MBBR, Sistema MBR, Sistema SBR, Soplante, Tamiz compactador, Tamiz de aliviadero, Tamiz rotativo, Tanque de mazcla, Tanque de tormentas, Tolva, Tornillo deshidratador de lodo, Tratamiento biológico, Tratamiento reactores secuenciales, Tratamiento terciario, Tubos, Valvulas, Varios.

**Analysis Instructions:**
1. Analyze the "Subject" and "Body" to identify if this is a Request for Quotation (RFQ) or product inquiry.
2. Extract company information from the body.
3. Identify the specific equipment or solution requested.
4. Cross-reference Subject and Body for accuracy.

**Output Format:**
You must respond with a valid JSON object following this schema:

```json
{{
  "record_id": "ID from the data",
  "company_info": {{
    "name": "Company name or 'Not specified'",
    "website": "Website URL or 'Not mentioned'",
    "country": "Country or 'Not specified'"
  }},
  "email_category": "One of: 'Solución de tratamiento compleja', 'Productos'",
  "product_category": "Category from the provided list, or 'Other'",
  "equipment_requested": "Detailed description of equipment/solution requested",
  "technical_specifications": "Any specific technical requirements or 'None specified'",
  "subject_body_correlation": "Brief note on how Subject and Body information align or differ"
}}
```
"""
