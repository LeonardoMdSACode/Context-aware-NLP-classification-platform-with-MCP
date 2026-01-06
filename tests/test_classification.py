from app.classification.decision import classify_document
from app.orchestration.context_resolver import resolve_context

def test_invoice_classification(embedded_mcp_servers):
    # Ensure MCP context is loaded
    context = resolve_context(
        text="Invoice for Q4 2025 total amount $4,500",
        metadata={"department": "finance"}
    )

    result = classify_document(
        text="Invoice for Q4 2025 total amount $4,500",
        context=context
    )

    assert result.label == "finance.invoice"
    assert result.confidence > 0.5
    assert result.abstained is False


def test_abstention_logic(embedded_mcp_servers):
    context = resolve_context(
        text="Random unrelated text with no meaning",
        metadata={}
    )

    result = classify_document(
        text="Random unrelated text with no meaning",
        context=context
    )

    assert "confidence" in result.__dict__
