from functools import lru_cache
from pathlib import Path
import json
import re

import numpy as np
from sentence_transformers import SentenceTransformer

from backend.app.services.geographic_lookup_service import (
    find_location_records,
)

from backend.app.services.geographic_lookup_service import (
    find_location_records,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

VECTOR_DIR = (
    PROJECT_ROOT
    / "backend"
    / "rag"
    / "vector_store"
)

EMBEDDINGS_FILE = VECTOR_DIR / "risk_research_embeddings.npy"
METADATA_FILE = VECTOR_DIR / "risk_research_documents.json"


RISK_KEYWORDS = {
    "flood": (
        "flood",
        "flooding",
        "inundation",
    ),
    "glof": (
        "glof",
        "glacial lake",
        "glacial lake outburst",
    ),
    "landslide": (
        "landslide",
        "land slide",
        "slide",
        "slope failure",
    ),
    "rainfall": (
        "rainfall",
        "rain",
        "precipitation",
        "cloudburst",
    ),
    "earthquake": (
        "earthquake",
        "seismic",
        "tremor",
    ),
    "weather": (
        "weather",
        "weather warning",
        "storm",
        "wind warning",
    ),
}


@lru_cache(maxsize=1)
def _load_store():
    if not EMBEDDINGS_FILE.exists():
        raise RuntimeError("RAG embeddings file not found.")

    if not METADATA_FILE.exists():
        raise RuntimeError("RAG metadata file not found.")

    embeddings = np.load(
        EMBEDDINGS_FILE
    ).astype(np.float32)

    with METADATA_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        store = json.load(file)

    documents = store["documents"]
    model_name = store["model_name"]

    if len(documents) != len(embeddings):
        raise RuntimeError(
            "RAG document/vector count mismatch."
        )

    model = SentenceTransformer(model_name)

    return model, embeddings, documents


def _detect_query_risk_types(query: str) -> set[str]:
    normalized = re.sub(
        r"\s+",
        " ",
        query.casefold(),
    )

    detected = set()

    for risk_type, keywords in RISK_KEYWORDS.items():
        if any(
            keyword in normalized
            for keyword in keywords
        ):
            detected.add(risk_type)

    return detected


def _document_matches_risk_type(
    document: dict,
    detected_types: set[str],
) -> bool:
    if not detected_types:
        return True

    metadata = document.get("metadata", {})

    searchable_type = " ".join(
        [
            str(metadata.get("risk_type") or ""),
            str(metadata.get("topic") or ""),
        ]
    ).casefold()

    for detected in detected_types:
        if detected == "glof":
            if any(
                term in searchable_type
                for term in ("glof", "glacial", "flood")
            ):
                return True

        elif detected == "flood":
            if any(
                term in searchable_type
                for term in ("flood", "glof", "inundation")
            ):
                return True

        elif detected == "landslide":
            if any(
                term in searchable_type
                for term in ("landslide", "slide", "slope")
            ):
                return True

        elif detected == "rainfall":
            if any(
                term in searchable_type
                for term in (
                    "rain",
                    "precipitation",
                    "cloudburst",
                )
            ):
                return True

        elif detected == "earthquake":
            if any(
                term in searchable_type
                for term in ("earthquake", "seismic", "tremor")
            ):
                return True

        elif detected == "weather":
            if any(
                term in searchable_type
                for term in ("weather", "storm", "warning")
            ):
                return True

    return False



def _normalize_location_text(value: str) -> str:
    value = value.casefold()
    value = re.sub(r"[^\w\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _location_candidates(value: str) -> list[str]:
    raw_parts = re.split(r"[/,–—()-]+", value)

    return [
        _normalize_location_text(part)
        for part in raw_parts
        if len(_normalize_location_text(part)) >= 4
    ]


def _document_location_match(
    query: str,
    document: dict,
) -> bool:
    query_normalized = _normalize_location_text(query)
    metadata = document.get("metadata", {})

    location = str(metadata.get("location_name") or "")
    district = str(metadata.get("district") or "")

    candidates = (
        _location_candidates(location)
        + _location_candidates(district)
    )

    return any(
        candidate in query_normalized
        for candidate in candidates
    )


def _query_has_known_location(
    query: str,
    documents: list[dict],
) -> bool:
    return any(
        _document_location_match(query, document)
        for document in documents
    )

def _resolve_query_geography(query: str) -> dict | None:
    query_normalized = _normalize_location_text(query)

    risk_words = {
        "landslide",
        "landslides",
        "flood",
        "flooding",
        "glof",
        "risk",
        "risks",
        "safety",
        "precautions",
        "warning",
        "warnings",
    }

    words = [
        word
        for word in query_normalized.split()
        if len(word) >= 4
        and word not in risk_words
    ]

    for size in (3, 2, 1):
        for index in range(len(words) - size + 1):
            candidate = " ".join(
                words[index:index + size]
            )

            matches = find_location_records(
                candidate,
                limit=20,
            )

            if not matches:
                continue

            states = {
                str(item["state"]).strip()
                for item in matches
                if item.get("state")
            }

            if len(states) == 1:
                return {
                    "query_location": candidate,
                    "state": next(iter(states)),
                    "matches": matches,
                }

    return None

def _document_matches_state(
    document: dict,
    state: str,
) -> bool:
    metadata = document.get("metadata", {})

    document_state = _normalize_location_text(
        str(metadata.get("state") or "")
    )
    query_state = _normalize_location_text(state)

    return bool(
        document_state
        and document_state == query_state
    )

def _document_matches_state(
    document: dict,
    state: str,
) -> bool:
    metadata = document.get("metadata", {})

    document_state = _normalize_location_text(
        str(metadata.get("state") or "")
    )
    query_state = _normalize_location_text(state)

    return bool(
        document_state
        and document_state == query_state
    )

def _document_knowledge_scope(
    document: dict,
) -> str:
    metadata = document.get("metadata", {})

    scope = _normalize_location_text(
        str(metadata.get("knowledge_scope") or "")
    )

    return scope or "location specific"


def _document_applicable_states(
    document: dict,
) -> set[str]:
    metadata = document.get("metadata", {})
    states: set[str] = set()

    raw_states = metadata.get("applicable_states")

    if isinstance(raw_states, (list, tuple, set)):
        values = raw_states
    elif raw_states:
        values = re.split(
            r"[,;/|]+",
            str(raw_states),
        )
    else:
        values = []

    for value in values:
        normalized = _normalize_location_text(
            str(value)
        )

        if normalized:
            states.add(normalized)

    state = _normalize_location_text(
        str(metadata.get("state") or "")
    )

    if state and state != "india":
        states.add(state)

    return states


def _document_applies_to_state(
    document: dict,
    state: str,
) -> bool:
    scope = _document_knowledge_scope(document)

    if scope in {
        "national",
        "general",
        "india wide",
        "indiawide",
    }:
        return True

    query_state = _normalize_location_text(state)

    if not query_state:
        return True

    return (
        query_state
        in _document_applicable_states(document)
    )


def _known_location_states(
    query: str,
    documents: list[dict],
) -> set[str]:
    states: set[str] = set()

    for document in documents:
        if not _document_location_match(
            query,
            document,
        ):
            continue

        metadata = document.get("metadata", {})

        state = _normalize_location_text(
            str(metadata.get("state") or "")
        )

        if state:
            states.add(state)

    return states


def search_risk_knowledge(
    query: str,
    *,
    top_k: int = 5,
    min_score: float = 0.20,
) -> list[dict]:
    query = query.strip()

    if not query:
        return []

    model, embeddings, documents = _load_store()

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0].astype(np.float32)

    scores = embeddings @ query_embedding

    detected_types = _detect_query_risk_types(query)

    known_location_states = _known_location_states(
        query,
        documents,
    )

    has_known_location = bool(
        known_location_states
    )

    resolved_geography = (
        None
        if has_known_location
        else _resolve_query_geography(query)
    )

    query_state = None

    if len(known_location_states) == 1:
        query_state = next(
            iter(known_location_states)
        )

    elif resolved_geography:
        query_state = resolved_geography["state"]

    ranked_indices = np.argsort(scores)[::-1]

    results = []

    for index in ranked_indices:
        score = float(scores[index])

        if score < min_score:
            continue

        document = documents[index]

        if not _document_matches_risk_type(
            document,
            detected_types,
        ):
            continue

        if (
            query_state
            and not _document_applies_to_state(
                document,
                query_state,
            )
        ):
            continue

        scope = _document_knowledge_scope(
            document
        )

        if (
            has_known_location
            and scope == "location specific"
            and not _document_location_match(
                query,
                document,
            )
        ):
            continue

        results.append(
            {
                "document_id": document["document_id"],
                "score": round(score, 4),
                "content": document["content"],
                "metadata": document["metadata"],
            }
        )

        if len(results) >= top_k:
            break

    return results











