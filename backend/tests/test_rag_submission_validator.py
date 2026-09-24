from pathlib import Path

import pandas as pd

from backend.data_pipeline.validators.rag_submission_validator import (
    validate_rag_submission,
)


def _write_submission(
    root: Path,
    source_dataset_type: str = "Official web page",
    source_notes: str = "Fetched directly from official source.",
    chunk_status: str = "VERIFIED",
    duplicate_text: bool = False,
) -> None:
    clean_dir = root / "CLEAN_VERIFIED"
    clean_dir.mkdir(parents=True, exist_ok=True)

    text_1 = "Official disaster guidance for testing."
    text_2 = (
        text_1
        if duplicate_text
        else "A second independent disaster guidance chunk."
    )

    chunks = pd.DataFrame(
        [
            {
                "Chunk ID": "TEST-001",
                "Title": "Test Guidance",
                "Organisation": "TESTORG",
                "Topic": "Flood",
                "State/Region": "India",
                "Year/Date": "2026",
                "Page/Section Reference": "Section 1",
                "Source URL": "https://example.gov.in/guidance",
                "Status": chunk_status,
                "Chunk Text (paraphrased)": text_1,
            },
            {
                "Chunk ID": "TEST-002",
                "Title": "Test Guidance Two",
                "Organisation": "TESTORG",
                "Topic": "Landslide",
                "State/Region": "India",
                "Year/Date": "2026",
                "Page/Section Reference": "Section 2",
                "Source URL": "https://example.gov.in/guidance",
                "Status": chunk_status,
                "Chunk Text (paraphrased)": text_2,
            },
        ]
    )

    rejected = pd.DataFrame(
        columns=[
            "Chunk ID",
            "Title",
            "Organisation",
            "Reason unverified/rejected",
            "Source URL (if any)",
            "Notes",
        ]
    )

    with pd.ExcelWriter(
        clean_dir / "clean_verified_chunks.xlsx",
        engine="openpyxl",
    ) as writer:
        chunks.to_excel(
            writer,
            sheet_name="Clean Verified Chunks",
            index=False,
        )
        rejected.to_excel(
            writer,
            sheet_name="Unverified Rejected",
            index=False,
        )

    sources = pd.DataFrame(
        [
            {
                "Source Name": "Test Official Source",
                "Organisation": "TESTORG",
                "URL": "https://example.gov.in/guidance",
                "Download Date": "2026-09-24",
                "Dataset Type": source_dataset_type,
                "Area/State": "India",
                "Time Period": "2026",
                "Real/Synthetic": "Real",
                "Notes": source_notes,
            }
        ]
    )

    with pd.ExcelWriter(
        root / "SOURCES.xlsx",
        engine="openpyxl",
    ) as writer:
        sources.to_excel(
            writer,
            sheet_name="Sources",
            index=False,
        )


def test_direct_official_submission_can_be_merge_ready(
    tmp_path: Path,
) -> None:
    root = tmp_path / "rag_submission"
    _write_submission(root)

    report = validate_rag_submission(root)

    assert report["status"] == "PASS"
    assert report["ready_for_merge"] is True
    assert report["chunk_count"] == 2
    assert report["verified_status_overclaims"] == []
    assert report["duplicate_chunk_ids"] == []
    assert report["duplicate_text_chunk_ids"] == []


def test_secondary_source_verified_overclaim_is_detected(
    tmp_path: Path,
) -> None:
    root = tmp_path / "rag_submission"

    _write_submission(
        root,
        source_dataset_type="Explainer citing official policy (secondary)",
        source_notes=(
            "Primary not directly fetched; re-verify against official "
            "source before production use."
        ),
    )

    report = validate_rag_submission(root)

    assert report["status"] == "PASS_WITH_WARNINGS"
    assert report["ready_for_merge"] is False
    assert len(report["chunks_requiring_reverification"]) == 2
    assert len(report["verified_status_overclaims"]) == 2


def test_duplicate_chunk_text_prevents_merge(
    tmp_path: Path,
) -> None:
    root = tmp_path / "rag_submission"

    _write_submission(
        root,
        duplicate_text=True,
    )

    report = validate_rag_submission(root)

    assert report["status"] == "PASS_WITH_WARNINGS"
    assert report["ready_for_merge"] is False
    assert set(report["duplicate_text_chunk_ids"]) == {
        "TEST-001",
        "TEST-002",
    }
