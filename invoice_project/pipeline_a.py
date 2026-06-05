import json

from azure.core.credentials import AzureKeyCredential

from azure.ai.formrecognizer import (
    DocumentAnalysisClient
)

from openai import AzureOpenAI

from config import (
    DOC_ENDPOINT,
    DOC_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_DEPLOYMENT
)

doc_client = DocumentAnalysisClient(
    endpoint=DOC_ENDPOINT,
    credential=AzureKeyCredential(DOC_KEY)
)

llm_client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2026-02-15-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)


def extract_text(image_path):

    with open(image_path, "rb") as f:

        poller = doc_client.begin_analyze_document(
            "prebuilt-read",
            document=f
        )

    result = poller.result()

    text = []

    for page in result.pages:
        for line in page.lines:
            text.append(line.content)

    return "\n".join(text)


def llm_extract(text):

    prompt = f"""
Extract invoice fields.

Return ONLY JSON.

{{
 "seller_name":"",
 "seller_tax_id":"",
 "client_name":"",
 "client_tax_id":"",
 "invoice_number":"",
 "invoice_date":"",
 "net_worth":"",
 "vat":"",
 "gross_worth":""
}}

Invoice Text:

{text}
"""

    response = llm_client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    return json.loads(content)


def process_invoice(image_path):

    text = extract_text(image_path)

    return llm_extract(text)