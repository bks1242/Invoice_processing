# Invoice Field Extraction System

Extracts structured data from invoice images using **two independent approaches**, then cross-validates and merges the results.

---

## Folder Structure

invoice_project/

├── data/
│   ├── batch1-0331.jpg
│   ├── batch1-0332.jpg
│   └── ...
│
├── outputs/
│
├── pipeline_a.py
├── pipeline_b.py
├── compare.py
├── main.py
├── config.py
├── .env
└── requirements.txt

outputs/
├── output.csv
└── comparison_report.csv

# Design Considerations

The solution intentionally uses two fundamentally different extraction approaches:

## Pipeline A
    OCR-driven
    LLM-assisted extraction
    Semantic understanding

## Pipeline B
    Specialized document AI model
    Structured extraction
    Invoice-specific intelligence

This ensures true validation between two independent extraction systems rather than two variations of the same approach.

**Pipeline A: OCR + LLM Extraction**

Pipeline A combines OCR capabilities with a Large Language Model to perform intelligent field extraction.

Workflow
Invoice Image
      │
Azure Document Intelligence OCR
      │
Raw OCR Text
      │
Azure OpenAI GPT-4o
      │
Structured JSON Output
Description
Azure Document Intelligence OCR extracts text from the invoice image.
Extracted text is sent to Azure OpenAI GPT-4o.
GPT-4o identifies and extracts the required fields.
Results are returned in structured JSON format.
Advantages
Handles OCR noise effectively.
Flexible across different invoice layouts.
Uses semantic understanding to infer missing information.

**Pipeline B: Azure Prebuilt Invoice Model**
Pipeline B uses Azure Document Intelligence's specialized invoice extraction model.

Workflow
Invoice Image
      │
Azure Document Intelligence
Prebuilt Invoice Model
      │
Structured Invoice Fields

Description
Invoice image is submitted directly to Azure's prebuilt invoice model.
The model identifies invoice-specific entities.
Extracted fields are mapped to the required output schema.
Tax IDs are additionally extracted using OCR and pattern matching when not returned by the model.
Advantages
Specifically trained for invoice documents.
High extraction accuracy.
Structured outputs with confidence scores.

## Field Mapping
Required Field	Azure Invoice Field
Seller Name	    VendorName
Client Name	    CustomerName
Invoice Number	InvoiceId
Invoice Date	InvoiceDate
Net Worth	    SubTotal
VAT	            TotalTax
Gross Worth	    InvoiceTotal

Seller Tax ID and Client Tax ID are extracted using OCR text and regular expressions.

## Validation Strategy

After extraction, outputs from both pipelines are compared field-by-field.

Comparison logic:

normalize(value_a) == normalize(value_b)

Normalization includes:

Case normalization
Whitespace removal
Null handling

# Setup

## Install 
    pip install azure-ai-formrecognizer
    pip install azure-core
    pip install openai
    pip install pandas
    pip install python-dotenv

## enviornment variables (.env)
    AZURE_DOC_INTELLIGENCE_ENDPOINT=""
    AZURE_DOC_INTELLIGENCE_KEY=""
    AZURE_OPENAI_ENDPOINT=""
    AZURE_OPENAI_KEY=""
    AZURE_OPENAI_DEPLOYMENT=gpt-5.1

## Final Workflow
Invoice
   │
   ├──────────────► Pipeline A
   │               OCR + GPT-4o
   │
   └──────────────► Pipeline B
                   Azure Invoice Model
                   +
                   OCR Tax-ID Enrichment

                    │
                    ▼
            comparison_report.csv

                    │
                    ▼
             final_record()

                    │
                    ▼
                output.csv