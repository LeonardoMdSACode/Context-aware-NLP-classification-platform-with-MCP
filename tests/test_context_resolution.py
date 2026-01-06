from app.orchestration.context_resolver import resolve_context

def test_context_resolution_embedded():
    context = resolve_context(
        text="Invoice for Q4 2025",
        metadata={"department": "finance"}
    )

    ctx = context.to_dict()

    assert "taxonomy" in ctx
    assert "policies" in ctx
    assert "history" in ctx
    assert isinstance(context.sources, list)
