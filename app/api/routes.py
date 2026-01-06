from fastapi import APIRouter, HTTPException, Query
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
    return HealthResponse(
        status="ok",
        environment=settings.ENV,
        mcp_embedded=settings.MCP_EMBEDDED,
    )


@router.post("/classify", response_model=ClassificationResponse)
def classify(request: ClassificationRequest) -> ClassificationResponse:
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
        raise HTTPException(status_code=500, detail="Classification failed") from exc


@router.post("/context", response_model=ContextResponse)
def inspect_context(request: ClassificationRequest) -> ContextResponse:
    """
    Debug / inspection endpoint.

    Returns resolved MCP context *without* classification.
    """
    try:
        context = resolve_context(
            text=request.text,
            metadata=request.metadata,
        )
        return ContextResponse(
            context=context.to_dict(),
            sources=context.sources,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Context resolution failed") from exc


@router.get("/predict")
def predict(query: str = Query(..., description="Text to classify")):
    """
    Simple GET endpoint for HTML/JS frontend integration.
    Calls MCP and classification internally.
    """
    try:
        context = resolve_context(text=query, metadata={})
        decision = classify_document(text=query, context=context)
        return {
            "label": decision.label,
            "confidence": decision.confidence,
            "abstained": decision.abstained,
            "context_summary": context.summary(),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction failed") from exc
