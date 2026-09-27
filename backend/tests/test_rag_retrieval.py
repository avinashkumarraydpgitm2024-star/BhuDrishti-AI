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


def test_location_specific_filter_stays_strict_for_sikkim():
    results = search_risk_knowledge(
        "Guwahati me landslide risk kya hai?",
        top_k=5,
        min_score=0.25,
    )

    for result in results:
        metadata = result["metadata"]

        if metadata.get("knowledge_scope") == "location_specific":
            assert metadata.get("state") != "Sikkim"


def test_existing_chungthang_primary_result_is_preserved():
    results = search_risk_knowledge(
        "Chungthang flood GLOF risk",
        top_k=5,
        min_score=0.25,
    )

    assert results
    assert results[0]["document_id"] == "RISK-001"


def test_national_rag_answer_uses_region_not_unknown_location():
    result = answer_risk_question(
        "India me CWC flood forecasting ka role kya hai?",
        top_k=3,
    )

    assert result["grounded"] is True
    assert result["primary_document_id"] == "CWC-F-001"
    assert (
        "Most relevant national research context: India."
        in result["answer"]
    )
    assert "Unknown location" not in result["answer"]
    assert "live emergency alert" in result["answer"]


def test_state_rag_answer_uses_state_context():
    result = answer_risk_question(
        "Sikkim me rainfall landslide ko kaise trigger karti hai?",
        top_k=3,
    )

    assert result["grounded"] is True
    assert result["primary_document_id"] == "SSDMA-SK-005"
    assert (
        "Most relevant state research context: Sikkim."
        in result["answer"]
    )
    assert "Unknown location" not in result["answer"]
