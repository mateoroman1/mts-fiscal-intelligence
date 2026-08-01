import pytest
from pydantic import ValidationError

# Just testing the pydantic model, not a proper unit test

from mts_fiscal_intelligence.models import AgentResult, SourceReference, ToolResult, ToolTrace


def test_source_page_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        SourceReference(
            title="june mts",
            page=0,
        )


def test_source_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        SourceReference(
            title="june mts",
            pagge=4,
        )


def test_successful_tool_result() -> None:
    result = ToolResult(
        success=True,
        data={"records": []},
    )

    assert result.success is True
    assert result.error is None
    assert result.sources == []


def test_failed_tool_result_requires_error() -> None:
    with pytest.raises(ValidationError):
        ToolResult(success=False)


def test_successful_result_cannot_have_error() -> None:
    with pytest.raises(ValidationError):
        ToolResult(
            success=True,
            error="something broke",
        )


def test_agent_result_serializes() -> None:
    source = SourceReference(
        title="june 2026 mts",
        document="MonthlyTreasuryStatement_202606.pdf",
        page=7,
    )

    trace = ToolTrace(
        step=1,
        tool_name="search_documents",
        arguments={"query": "deficit increase"},
        success=True,
        summary="found three relevant report passages",
        sources=[source],
    )

    result = AgentResult(
        answer="the deficit increased because...",
        tool_calls=[trace],
        sources=[source],
    )

    dumped = result.model_dump()

    assert dumped["answer"] == "the deficit increased because..."
    assert dumped["tool_calls"][0]["tool_name"] == "search_documents"
    assert dumped["sources"][0]["page"] == 7