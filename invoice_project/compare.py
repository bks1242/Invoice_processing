def normalize(value):

    if value is None:
        return ""

    return str(value).strip().lower()


def compare_records(
    filename,
    pipeline_a,
    pipeline_b
):

    rows = []

    fields = [
        "seller_name",
        "seller_tax_id",
        "client_name",
        "client_tax_id",
        "invoice_number",
        "invoice_date",
        "net_worth",
        "vat",
        "gross_worth"
    ]

    for field in fields:

        rows.append({

            "file_name": filename,

            "field": field,

            "pipeline_a":
                pipeline_a.get(field, ""),

            "pipeline_b":
                pipeline_b.get(field, ""),

            "match":
                normalize(
                    pipeline_a.get(field)
                )
                ==
                normalize(
                    pipeline_b.get(field)
                )
        })

    return rows


def final_record(
    pipeline_a,
    pipeline_b
):
    """
    Prefer Invoice Model values.
    Fallback to LLM values.
    """

    fields = [
        "seller_name",
        "seller_tax_id",
        "client_name",
        "client_tax_id",
        "invoice_number",
        "invoice_date",
        "net_worth",
        "vat",
        "gross_worth"
    ]

    final = {}

    for field in fields:

        b_value = pipeline_b.get(field)

        if b_value not in [
            None,
            "",
            "None"
        ]:
            final[field] = b_value

        else:
            final[field] = pipeline_a.get(
                field,
                ""
            )

    return final