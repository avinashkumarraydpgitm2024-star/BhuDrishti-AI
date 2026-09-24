from pathlib import Path
import json

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENTS_FILE = (
    PROJECT_ROOT
    / "backend"
    / "rag"
    / "processed"
    / "risk_research_documents.jsonl"
)

VECTOR_DIR = (
    PROJECT_ROOT
    / "backend"
    / "rag"
    / "vector_store"
)

EMBEDDINGS_FILE = VECTOR_DIR / "risk_research_embeddings.npy"
METADATA_FILE = VECTOR_DIR / "risk_research_documents.json"

MODEL_NAME = "all-MiniLM-L6-v2"


def load_documents():
    documents = []

    with DOCUMENTS_FILE.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        for line in file:
            if line.strip():
                documents.append(json.loads(line))

    return documents


def main():
    documents = load_documents()

    if not documents:
        raise RuntimeError("No RAG documents found.")

    print("Documents:", len(documents))
    print("Loading embedding model:", MODEL_NAME)

    model = SentenceTransformer(MODEL_NAME)

    texts = [
        document["content"]
        for document in documents
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32,
    )

    VECTOR_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    np.save(
        EMBEDDINGS_FILE,
        embeddings,
    )

    with METADATA_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            {
                "model_name": MODEL_NAME,
                "embedding_dimension": int(
                    embeddings.shape[1]
                ),
                "document_count": len(documents),
                "documents": documents,
            },
            file,
            ensure_ascii=False,
            indent=2,
        )

    print("Embedding shape:", embeddings.shape)
    print("Saved embeddings:", EMBEDDINGS_FILE)
    print("Saved metadata:", METADATA_FILE)
    print("VECTOR STORE BUILD: PASS")


if __name__ == "__main__":
    main()
