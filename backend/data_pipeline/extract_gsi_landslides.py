import pymupdf
import csv
import os

PDF_PATH = "backend/data/india_sources/gsi_landslide_report.pdf"
OUTPUT_PATH = "backend/data/india_historical_incidents.csv"

print("Opening GSI PDF...")

doc = pymupdf.open(PDF_PATH)

records = []

for page_number, page in enumerate(doc, start=1):
    tables = page.find_tables().tables

    if not tables:
        continue

    for row in tables[0].extract():
        if not row:
            continue

        first = (row[0] or "").strip()

        if first.isdigit() and len(row) >= 11:
            records.append(row[:11])

    if page_number % 100 == 0:
        print(f"Processed {page_number}/{len(doc)} pages")

headers = [
    "serial_no",
    "slide_no",
    "state",
    "district",
    "slide_name",
    "nh_sh_location",
    "latitude",
    "longitude",
    "material_involved",
    "movement_type",
    "history"
]

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(records)

print("Extraction complete.")
print("Total records:", len(records))
print("Saved to:", OUTPUT_PATH)
