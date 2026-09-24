from backend.app.services.rag_retrieval_service import search_risk_knowledge


def test_chungthang_flood_retrieval():
    results = search_risk_knowledge(
        "Chungthang me flood ya GLOF risk ke bare me batao",
        top_k=3,
        min_score=0.25,
    )

    assert results, "Chungthang query should return at least one RAG result."

    primary = results[0]

    assert primary["document_id"] == "RISK-001"
    assert primary["metadata"]["location_name"] == "Chungthang"
    assert primary["metadata"]["state"] == "Sikkim"
    assert "Flood" in primary["metadata"]["risk_type"]


def test_guwahati_does_not_return_sikkim_research():
    results = search_risk_knowledge(
        "Guwahati me landslide risk kya hai?",
        top_k=3,
        min_score=0.25,
    )

    assert results == [], (
        "Guwahati query must not return unrelated Sikkim research records."
    )


def test_mangan_landslide_retrieval():
    results = search_risk_knowledge(
        "Mangan district me landslide risk kya hai?",
        top_k=3,
        min_score=0.25,
    )

    assert results, "Mangan query should return a relevant RAG result."

    primary = results[0]

    assert primary["document_id"] == "RISK-002"
    assert primary["metadata"]["location_name"] == "Mangan Town"
    assert primary["metadata"]["state"] == "Sikkim"
    assert primary["metadata"]["risk_type"] == "Landslide"

from backend.app.services.rag_answer_service import answer_risk_question


def test_guwahati_answer_is_not_falsely_grounded():
    result = answer_risk_question(
        "Guwahati me landslide risk kya hai?",
        top_k=3,
    )

    assert result["grounded"] is False
    assert result["primary_document_id"] is None
    assert result["primary_similarity_score"] is None
    assert result["sources"] == []


def test_rag_source_and_content_integrity():
    results = search_risk_knowledge(
        "Mangan district me landslide risk kya hai?",
        top_k=3,
        min_score=0.25,
    )

    assert results

    primary = results[0]

    assert primary["document_id"] == "RISK-002"
    assert primary["metadata"]["official_source_page"] == "https://ssdma.nic.in/activities.html"
    assert "use only routes" in primary["content"]
    assert "use onlyroutes" not in primary["content"]
    assert "completed, but" in primary["content"]
