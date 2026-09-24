from fastapi import APIRouter

from backend.app.schemas.rag import (
    RAGAnswerResponse,
    RAGQuestionRequest,
)
from backend.app.services.rag_answer_service import (
    answer_risk_question,
)


router = APIRouter(
    prefix="/rag",
    tags=["RAG Intelligence"],
)


@router.post(
    "/ask",
    response_model=RAGAnswerResponse,
)
def ask_risk_question(
    payload: RAGQuestionRequest,
) -> RAGAnswerResponse:
    result = answer_risk_question(
        payload.question,
        top_k=payload.top_k,
    )

    return RAGAnswerResponse(**result)
