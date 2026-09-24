from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_CHUNK_COLUMNS = {
    "Chunk ID",
    "Title",
    "Organisation",
    "Topic",
    "State/Region",
    "Year/Date",
    "Page/Section Reference",
    "Source URL",
    "Status",
    "Chunk Text (paraphrased)",
}

REQUIRED_REJECTED_COLUMNS = {
    "Chunk ID",
    "Title",
    "Organisation",
    "Reason unverified/rejected",
    "Source URL (if any)",
    "Notes",
}

REQUIRED_SOURCE_COLUMNS = {
    "Source Name",
    "Organisation",
    "URL",
    "Download Date",
    "Dataset Type",
    "Area/State",
    "Time Period",
    "Real/Synthetic",
    "Notes",
}


def _clean(value: Any) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _normalize_url(value: Any) -> str:
    url = _clean(value).lower().rstrip("/")
    return url


def _normalize_text(value: Any) -> str:
    text = _clean(value).casefold()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _source_requires_reverification(row: pd.Series) -> bool:
    dataset_type = _clean(row.get("Dataset Type")).casefold()
    notes = _clean(row.get("Notes")).casefold()

    warning_terms = (
        "secondary",
        "primary not directly fetched",
        "re-verify",
        "reverify",
        "not the imd.gov.in page",
        "not the mausam.imd.gov.in page",
    )

    combined = f"{dataset_type} {notes}"
    return any(term in combined for term in warning_terms)


def validate_rag_submission(base_dir: str | Path) -> dict[str, Any]:
    base = Path(base_dir)

    chunk_file = base / "CLEAN_VERIFIED" / "clean_verified_chunks.xlsx"
    sources_file = base / "SOURCES.xlsx"

    errors: list[str] = []
    warnings: list[str] = []

    if not chunk_file.exists():
        return {
            "status": "FAIL",
            "errors": [f"Missing file: {chunk_file}"],
            "warnings": [],
            "ready_for_merge": False,
        }

    if not sources_file.exists():
        return {
            "status": "FAIL",
            "errors": [f"Missing file: {sources_file}"],
            "warnings": [],
            "ready_for_merge": False,
        }

    chunks = pd.read_excel(
        chunk_file,
        sheet_name="Clean Verified Chunks",
    )

    rejected = pd.read_excel(
        chunk_file,
        sheet_name="Unverified Rejected",
    )

    sources = pd.read_excel(
        sources_file,
        sheet_name="Sources",
    )

    missing_chunk_columns = sorted(
        REQUIRED_CHUNK_COLUMNS - set(chunks.columns)
    )
    missing_rejected_columns = sorted(
        REQUIRED_REJECTED_COLUMNS - set(rejected.columns)
    )
    missing_source_columns = sorted(
        REQUIRED_SOURCE_COLUMNS - set(sources.columns)
    )

    if missing_chunk_columns:
        errors.append(
            f"Missing Clean Verified Chunks columns: {missing_chunk_columns}"
        )

    if missing_rejected_columns:
        errors.append(
            f"Missing Unverified Rejected columns: {missing_rejected_columns}"
        )

    if missing_source_columns:
        errors.append(
            f"Missing Sources columns: {missing_source_columns}"
        )

    if errors:
        return {
            "status": "FAIL",
            "errors": errors,
            "warnings": warnings,
            "ready_for_merge": False,
        }

    chunk_ids = chunks["Chunk ID"].map(_clean)
    normalized_text = chunks["Chunk Text (paraphrased)"].map(
        _normalize_text
    )

    duplicate_chunk_ids = sorted(
        chunk_ids[
            chunk_ids.duplicated(keep=False) & chunk_ids.ne("")
        ].unique().tolist()
    )

    duplicate_text_rows = chunks.loc[
        normalized_text.duplicated(keep=False)
        & normalized_text.ne(""),
        "Chunk ID",
    ].map(_clean).tolist()

    missing_values: dict[str, int] = {}

    for column in REQUIRED_CHUNK_COLUMNS:
        count = int(chunks[column].map(_clean).eq("").sum())
        if count:
            missing_values[column] = count

    status_counts = {
        str(key): int(value)
        for key, value in Counter(
            chunks["Status"].map(_clean)
        ).items()
    }

    organisation_counts = {
        str(key): int(value)
        for key, value in Counter(
            chunks["Organisation"].map(_clean)
        ).items()
    }

    source_lookup: dict[str, dict[str, Any]] = {}

    for _, row in sources.iterrows():
        normalized_url = _normalize_url(row["URL"])

        if not normalized_url:
            continue

        source_lookup[normalized_url] = {
            "source_name": _clean(row["Source Name"]),
            "organisation": _clean(row["Organisation"]),
            "dataset_type": _clean(row["Dataset Type"]),
            "notes": _clean(row["Notes"]),
            "requires_reverification": _source_requires_reverification(
                row
            ),
        }

    unmatched_source_chunks: list[str] = []
    reverify_chunks: list[dict[str, str]] = []
    verified_status_overclaims: list[dict[str, str]] = []

    for _, row in chunks.iterrows():
        chunk_id = _clean(row["Chunk ID"])
        chunk_url = _normalize_url(row["Source URL"])
        status = _clean(row["Status"]).upper()

        source_info = source_lookup.get(chunk_url)

        if source_info is None:
            unmatched_source_chunks.append(chunk_id)
            continue

        if source_info["requires_reverification"]:
            item = {
                "chunk_id": chunk_id,
                "source_name": source_info["source_name"],
                "dataset_type": source_info["dataset_type"],
            }

            reverify_chunks.append(item)

            if status == "VERIFIED":
                verified_status_overclaims.append(item)

    source_reverification = []

    for _, row in sources.iterrows():
        if _source_requires_reverification(row):
            source_reverification.append(
                {
                    "source_name": _clean(row["Source Name"]),
                    "organisation": _clean(row["Organisation"]),
                    "dataset_type": _clean(row["Dataset Type"]),
                    "notes": _clean(row["Notes"]),
                }
            )

    if duplicate_chunk_ids:
        warnings.append(
            f"Duplicate Chunk IDs detected: {len(duplicate_chunk_ids)}"
        )

    if duplicate_text_rows:
        warnings.append(
            "Normalized duplicate chunk text detected."
        )

    if missing_values:
        warnings.append(
            "One or more clean chunk fields contain missing values."
        )

    if unmatched_source_chunks:
        warnings.append(
            f"{len(unmatched_source_chunks)} chunks do not exactly match "
            "a URL in SOURCES.xlsx."
        )

    if verified_status_overclaims:
        warnings.append(
            f"{len(verified_status_overclaims)} chunks are marked VERIFIED "
            "but their source metadata says primary-source re-verification "
            "is required."
        )

    if len(rejected) > 0:
        warnings.append(
            f"{len(rejected)} entries are stored in Unverified Rejected."
        )

    real_synthetic_counts = {
        str(key): int(value)
        for key, value in Counter(
            sources["Real/Synthetic"].map(_clean)
        ).items()
    }

    ready_for_merge = (
        not errors
        and not duplicate_chunk_ids
        and not duplicate_text_rows
        and not missing_values
        and not unmatched_source_chunks
        and not verified_status_overclaims
    )

    status = (
        "FAIL"
        if errors
        else "PASS_WITH_WARNINGS"
        if warnings
        else "PASS"
    )

    return {
        "classification": "rag_knowledge_submission",
        "chunk_count": int(len(chunks)),
        "unverified_rejected_count": int(len(rejected)),
        "source_count": int(len(sources)),
        "organisation_counts": organisation_counts,
        "status_counts": status_counts,
        "real_synthetic_counts": real_synthetic_counts,
        "duplicate_chunk_ids": duplicate_chunk_ids,
        "duplicate_text_chunk_ids": duplicate_text_rows,
        "missing_values": missing_values,
        "unmatched_source_chunks": unmatched_source_chunks,
        "sources_requiring_reverification": source_reverification,
        "chunks_requiring_reverification": reverify_chunks,
        "verified_status_overclaims": verified_status_overclaims,
        "errors": errors,
        "warnings": warnings,
        "ready_for_merge": ready_for_merge,
        "status": status,
    }
