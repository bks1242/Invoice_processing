from pathlib import Path
import pandas as pd

from pipeline_a import process_invoice as run_a
from pipeline_b import process_invoice as run_b

from compare import (
    compare_records,
    final_record
)

DATA_FOLDER = "data"
OUTPUT_FOLDER = "outputs"

output_rows = []
comparison_rows = []

# Recursively find all invoice images
image_files = []

for extension in ["*.jpg", "*.jpeg", "*.png"]:
    image_files.extend(
        Path(DATA_FOLDER).rglob(extension)
    )

print(f"Found {len(image_files)} images")

for image_file in sorted(image_files):

    print(
        f"Processing {image_file.name}"
    )

    try:

        result_a = run_a(
            str(image_file)
        )

        result_b = run_b(
            str(image_file)
        )

        # Final merged output
        final_result = final_record(
            result_a,
            result_b
        )

        final_result["file_name"] = (
            image_file.name
        )

        output_rows.append(
            final_result
        )

        comparison_rows.extend(

            compare_records(
                image_file.name,
                result_a,
                result_b
            )
        )

    except Exception as ex:

        print(
            f"Failed processing "
            f"{image_file.name}: {ex}"
        )

output_df = pd.DataFrame(
    output_rows
)

comparison_df = pd.DataFrame(
    comparison_rows
)

Path(OUTPUT_FOLDER).mkdir(
    exist_ok=True
)

output_df.to_csv(
    f"{OUTPUT_FOLDER}/output.csv",
    index=False
)

comparison_df.to_csv(
    f"{OUTPUT_FOLDER}/comparison_report.csv",
    index=False
)

print(
    f"Processed {len(output_rows)} invoices"
)

print(
    f"Output saved to "
    f"{OUTPUT_FOLDER}/output.csv"
)

print(
    f"Comparison saved to "
    f"{OUTPUT_FOLDER}/comparison_report.csv"
)