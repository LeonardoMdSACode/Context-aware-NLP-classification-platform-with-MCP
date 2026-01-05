from fastapi import APIRouter, Depends, HTTPException

from app.config import get_settings
from app.api.schemas import (
    ClassificationRequest,
    ClassificationResponse,
    HealthResponse,
    ContextResponse,
)

from app.orchestration.context_resolver import resolve_context
from app.classification.decision import classify_document


router = APIRouter()
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """
    Liveness / readiness probe.
    """
    return HealthResponse(
        status="ok",
        environment=settings.ENV,
        mcp_embedded=settings.MCP_EMBEDDED,
    )


@router.post("/classify", response_model=ClassificationResponse)
def classify(request: ClassificationRequest) -> ClassificationResponse:
    """
    Main inference endpoint.

    Flow:
    1. Resolve structured context via MCP
    2. Perform classification
    3. Apply confidence / abstention logic
    """

    try:
        context = resolve_context(
            text=request.text,
            metadata=request.metadata,
        )

        decision = classify_document(
            text=request.text,
            context=context,
        )

        return ClassificationResponse(
            label=decision.label,
            confidence=decision.confidence,
            abstained=decision.abstained,
            context_used=context.summary(),
        )

    except Exception as exc:
        # Intentionally generic: internal details go to logs
        raise HTTPException(
            status_code=500,
            detail="Classification failed",
        ) from exc


@router.post("/context", response_model=ContextResponse)
def inspect_context(request: ClassificationRequest) -> ContextResponse:
    """
    Debug / inspection endpoint.

    Returns resolved MCP context *without* classification.
    Useful for:
    - Testing
    - Auditing
    - Demonstrations
    """

    context = resolve_context(
        text=request.text,
        metadata=request.metadata,
    )

    return ContextResponse(
        context=context.to_dict(),
        sources=context.sources,
    )
