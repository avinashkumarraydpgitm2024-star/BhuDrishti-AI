from backend.data_pipeline.incident_pipeline import (
    normalize_incident
)


def normalize_incident_records(records):
    if not isinstance(records, list):
        raise ValueError(
            "Incident records must be provided as a list."
        )

    normalized = []

    for record in records:
        normalized.append(
            normalize_incident(record)
        )

    return normalized


import json

from backend.data_pipeline.incident_pipeline import (
    INCIDENT_DATA_PATH
)


def save_incident_records(records):
    normalized_records = normalize_incident_records(records)

    with open(
        INCIDENT_DATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            normalized_records,
            file,
            indent=2
        )

    return len(normalized_records)
