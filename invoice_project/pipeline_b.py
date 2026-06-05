from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

import re

from config import (
    DOC_ENDPOINT,
    DOC_KEY
)

client = DocumentAnalysisClient(
    endpoint=DOC_ENDPOINT,
    credential=AzureKeyCredential(DOC_KEY)
)


def get_field(document, field_name):

    field = document.fields.get(field_name)

    if field:
        return field.value

    return ""


def extract_text(image_path):

    with open(image_path, "rb") as f:

        poller = client.begin_analyze_document(
            "prebuilt-read",
            document=f
        )

    result = poller.result()

    text = []

    for page in result.pages:
        for line in page.lines:
            text.append(line.content)

    return "\n".join(text)


def extract_tax_ids(full_text):

    tax_ids = re.findall(
        r'\d{3}-\d{2}-\d{4}',
        full_text
    )

    seller_tax = ""
    client_tax = ""

    if len(tax_ids) > 0:
        seller_tax = tax_ids[0]

    if len(tax_ids) > 1:
        client_tax = tax_ids[1]

    return seller_tax, client_tax


def process_invoice(image_path):

    with open(image_path, "rb") as f:

        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            document=f
        )

    result = poller.result()

    if len(result.documents) == 0:
        return {}

    invoice = result.documents[0]

    output = {}

    output["seller_name"] = get_field(
        invoice,
        "VendorName"
    )

    output["client_name"] = get_field(
        invoice,
        "CustomerName"
    )

    output["invoice_number"] = get_field(
        invoice,
        "InvoiceId"
    )

    output["invoice_date"] = str(
        get_field(invoice, "InvoiceDate")
    )

    output["net_worth"] = get_field(
        invoice,
        "SubTotal"
    )

    output["vat"] = get_field(
        invoice,
        "TotalTax"
    )

    output["gross_worth"] = get_field(
        invoice,
        "InvoiceTotal"
    )

    # OCR enrichment
    ocr_text = extract_text(image_path)

    seller_tax, client_tax = extract_tax_ids(
        ocr_text
    )

    output["seller_tax_id"] = seller_tax
    output["client_tax_id"] = client_tax

    return output