from functools import lru_cache
from pathlib import Path
import json
import re

import numpy as np
from sentence_transformers import SentenceTransformer


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
    risk_type = str(
        metadata.get("risk_type") or ""
    ).casefold()

    for detected in detected_types:
        if detected == "glof":
            if (
                "glof" in risk_type
                or "glacial" in risk_type
                or "flood" in risk_type
            ):
                return True

        elif detected == "flood":
            if (
                "flood" in risk_type
                or "glof" in risk_type
            ):
                return True

        elif detected == "landslide":
            if (
                "landslide" in risk_type
                or "slide" in risk_type
            ):
                return True

    return False



def _normalize_location_text(value: str) -> str:
    value = value.casefold()
    value = re.sub(r"[^\w\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _document_location_match(
    query: str,
    document: dict,
) -> bool:
    query_normalized = _normalize_location_text(query)

    metadata = document.get("metadata", {})

    location = _normalize_location_text(
        str(metadata.get("location_name") or "")
    )

    if not location:
        return False

    # Match meaningful location phrases from the document.
    candidates = [
        part.strip()
        for part in re.split(
            r"[/,–—()-]+",
            location,
        )
        if len(part.strip()) >= 4
    ]

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
    has_known_location = _query_has_known_location(
        query,
        documents,
    )

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
            has_known_location
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

