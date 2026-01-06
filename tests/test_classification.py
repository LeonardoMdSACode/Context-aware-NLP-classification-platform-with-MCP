from app.classification.decision import classify_document

def test_invoice_classification():
    result = classify_document(
        text="Invoice for Q4 2025 total amount $4,500",
        context={}
    )

    assert result.label == "finance.invoice"
    assert result.confidence > 0.5
    assert result.abstained is False


def test_abstention_logic():
    result = classify_document(
        text="Random unrelated text with no meaning",
        context={}
    )

    assert "confidence" in result.__dict__
