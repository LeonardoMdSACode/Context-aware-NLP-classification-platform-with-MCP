from typing import Dict, Optional, Any, List
from pydantic import BaseModel, Field


# -------------------------
# Requests
# -------------------------

class ClassificationRequest(BaseModel):
    """
    Input payload for classification and context inspection.
    """

    text: str = Field(
        ...,
        min_length=1,
        description="Raw document text to classify",
        example="Invoice for consulting services rendered in Q4",
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional structured metadata (source, language, department, etc.)",
        example={"source": "email", "language": "en"},
    )


# -------------------------
# Responses
# -------------------------

class ClassificationResponse(BaseModel):
    """
    Final classification result returned to the client.
    """

    label: Optional[str] = Field(
        None,
        description="Predicted document category (null if abstained)",
        example="finance.invoice",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence score",
        example=0.87,
    )

    abstained: bool = Field(
        ...,
        description="Whether the system abstained due to low confidence or rules",
        example=False,
    )

    context_used: Dict[str, Any] = Field(
        ...,
        description="Summary of structured context used during inference",
        example={
            "taxonomy": "v1.2",
            "policies_applied": ["finance_rules"],
            "historical_labels_considered": True,
        },
    )


class ContextResponse(BaseModel):
    """
    Context inspection response (no classification).
    """

    context: Dict[str, Any] = Field(
        ...,
        description="Resolved structured context from MCP servers",
    )

    sources: List[str] = Field(
        ...,
        description="List of MCP context sources consulted",
        example=["taxonomy_server", "policy_server"],
    )


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str = Field(example="ok")
    environment: str = Field(example="local")
    mcp_embedded: bool = Field(example=True)
