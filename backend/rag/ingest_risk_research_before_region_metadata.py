from pathlib import Path
import json

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILE = (
    PROJECT_ROOT
    / "backend"
    / "data"
    / "research"
    / "risk_research"
    / "official_risk_research.xlsx"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "backend"
    / "rag"
    / "processed"
    / "risk_research_documents.jsonl"
)


def clean_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()
    return value if value else None


def main():
    df = pd.read_excel(
        SOURCE_FILE,
        sheet_name="Risk Research",
    )

    documents = []

    for _, row in df.iterrows():
        case_id = clean_value(row.get("Case ID"))

        if not case_id:
            continue

        metadata = {
            "case_id": case_id,
            "location_name": clean_value(
                row.get("Location Name")
            ),
            "district": clean_value(
                row.get("District")
            ),
            "risk_type": clean_value(
                row.get("Risk Type")
            ),
            "risk_level": clean_value(
                row.get("Risk Level")
            ),
            "official_source_page": clean_value(
                row.get("Official Source Page")
            ),
            "official_document_section": clean_value(
                row.get(
                    "Official Document / Section to Check"
                )
            ),
            "verification_note": clean_value(
                row.get("Verification Note")
            ),
            "source_type": "official_risk_research",
        }

        sections = [
            (
                "Location",
                metadata["location_name"],
            ),
            (
                "District",
                metadata["district"],
            ),
            (
                "Risk Type",
                metadata["risk_type"],
            ),
            (
                "Risk Level",
                metadata["risk_level"],
            ),
            (
                "Risk Reason",
                clean_value(row.get("Risk Reason")),
            ),
            (
                "Warning Signs",
                clean_value(row.get("Warning Signs")),
            ),
            (
                "Safety Precautions",
                clean_value(
                    row.get("Safety Precautions")
                ),
            ),
            (
                "Approximate Risk Reduction",
                clean_value(
                    row.get(
                        "Approx. When Risk May Reduce"
                    )
                ),
            ),
            (
                "Alternative Safe Location or Route",
                clean_value(
                    row.get(
                        "Alternative Safe Location/Route"
                    )
                ),
            ),
        ]

        content = "\n".join(
            f"{title}: {value}"
            for title, value in sections
            if value
        )

        documents.append(
            {
                "document_id": case_id,
                "content": content,
                "metadata": metadata,
            }
        )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        for document in documents:
            file.write(
                json.dumps(
                    document,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print("Source rows:", len(df))
    print("RAG documents:", len(documents))
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
