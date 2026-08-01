from __future__ import annotations
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, model_validator

class AppModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True
    )

class ToolResult(AppModel):

    success: bool
    data: Any | None = None
    error: str | None = None
    sources: list[SourceReference] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_result_state(self) -> ToolResult:
        """Require success and error fields to describe a coherent state."""

        if self.success and self.error is not None:
            raise ValueError("a successful tool result cannot contain an error")

        if not self.success and not self.error:
            raise ValueError("a failed tool result must contain an error")

        return self


class SourceReference(AppModel):

    title: str = Field(
        min_length=1,
        description="Human-readable name for the source.",
    )
    url: str | None = Field(
        default=None,
        description="URL for an API request or published document.",
    )
    document: str | None = Field(
        default=None,
        description="Local or published document filename.",
    )
    page: int | None = Field(
        default=None,
        ge=1,
        description="One-indexed page number in a document.",
    )

class ToolTrace(AppModel):

    step: int = Field(ge=1)
    tool_name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)
    success: bool
    summary: str = Field(
        min_length=1,
        description="Concise description of the tool result.",
    )
    error: str | None = None
    sources: list[SourceReference] = Field(default_factory=list)

class AgentResult(AppModel):

    answer: str = Field(min_length=1)
    tool_calls: list[ToolTrace] = Field(default_factory=list)
    sources: list[SourceReference] = Field(default_factory=list)
    report_path: str | None = None