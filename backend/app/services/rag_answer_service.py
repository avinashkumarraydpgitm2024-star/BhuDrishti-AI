from backend.app.services.rag_retrieval_service import (
    search_risk_knowledge,
)


def answer_risk_question(
    question: str,
    *,
    top_k: int = 3,
) -> dict:
    question = question.strip()

    if not question:
        return {
            "answer": "Please provide a risk-related question.",
            "primary_document_id": None,
            "primary_similarity_score": None,
            "sources": [],
            "grounded": False,
        }

    results = search_risk_knowledge(
        question,
        top_k=top_k,
        min_score=0.25,
    )

    if not results:
        return {
            "answer": (
                "No sufficiently relevant research record "
                "was found in the current BhuDrishti "
                "knowledge base."
            ),
            "primary_document_id": None,
            "primary_similarity_score": None,
            "sources": [],
            "grounded": False,
        }

    primary = results[0]
    metadata = primary["metadata"]

    source_entries = []

    for result in results:
        item_metadata = result["metadata"]

        source_location = (
            item_metadata.get("location_name")
            or item_metadata.get("region")
            or item_metadata.get("state")
        )

        source_entries.append(
            {
                "document_id": result["document_id"],
                "location": source_location,
                "risk_type": item_metadata.get(
                    "risk_type"
                ),
                "similarity_score": result["score"],
                "official_source": item_metadata.get(
                    "official_source_page"
                ),
                "verification_note": item_metadata.get(
                    "verification_note"
                ),
            }
        )

    location_name = metadata.get(
        "location_name"
    )

    context_name = (
        location_name
        or metadata.get("region")
        or metadata.get("state")
        or "General"
    )

    knowledge_scope = str(
        metadata.get("knowledge_scope") or ""
    ).strip().casefold()

    if location_name:
        context_label = "Most relevant research record"
    elif knowledge_scope == "national":
        context_label = "Most relevant national research context"
    elif knowledge_scope == "state":
        context_label = "Most relevant state research context"
    elif knowledge_scope == "regional":
        context_label = "Most relevant regional research context"
    else:
        context_label = "Most relevant research context"

    answer = (
        f"{context_label}: {context_name}.\n\n"
        f"{primary['content']}\n\n"
        f"This response is grounded in BhuDrishti's "
        f"retrieved research record "
        f"{primary['document_id']}. "
        f"It should not be treated as a live emergency alert."
    )

    return {
        "answer": answer,
        "primary_document_id": primary["document_id"],
        "primary_similarity_score": primary["score"],
        "sources": source_entries,
        "grounded": True,
    }


