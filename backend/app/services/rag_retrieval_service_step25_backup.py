from functools import lru_cache
from pathlib import Path
import json

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[3]

VECTOR_DIR = (
    PROJECT_ROOT
    / "backend"
    / "rag"
    / "vector_store"
)

EMBEDDINGS_FILE = (
    VECTOR_DIR
    / "risk_research_embeddings.npy"
)

METADATA_FILE = (
    VECTOR_DIR
    / "risk_research_documents.json"
)


@lru_cache(maxsize=1)
def _load_store():
    if not EMBEDDINGS_FILE.exists():
        raise RuntimeError(
            "RAG embeddings file not found."
        )

    if not METADATA_FILE.exists():
        raise RuntimeError(
            "RAG metadata file not found."
        )

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

    model = SentenceTransformer(
        model_name
    )

    return model, embeddings, documents


def search_risk_knowledge(
    query: str,
    *,
    top_k: int = 5,
    min_score: float = 0.20,
) -> list[dict]:
    query = query.strip()

    if not query:
        return []

    model, embeddings, documents = (
        _load_store()
    )

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0].astype(np.float32)

    # Both stored vectors and query vector are
    # normalized, so dot product = cosine similarity.
    scores = embeddings @ query_embedding

    top_k = max(
        1,
        min(top_k, len(documents)),
    )

    indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in indices:
        score = float(scores[index])

        if score < min_score:
            continue

        document = documents[index]

        results.append(
            {
                "document_id": document[
                    "document_id"
                ],
                "score": round(score, 4),
                "content": document["content"],
                "metadata": document["metadata"],
            }
        )

    return results
