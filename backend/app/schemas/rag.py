from pydantic import BaseModel, Field


class RAGQuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
    )


class RAGSourceResponse(BaseModel):
    document_id: str
    location: str | None = None
    risk_type: str | None = None
    similarity_score: float
    official_source: str | None = None
    verification_note: str | None = None


class RAGAnswerResponse(BaseModel):
    answer: str
    grounded: bool
    primary_document_id: str | None = None
    primary_similarity_score: float | None = None
    sources: list[RAGSourceResponse]
