from __future__ import annotations
from typing import Any
from pydantic import ValidationError

from mts_fiscal_intelligence.models import ToolResult
from mts_fiscal_intelligence.tools.document_search import DocumentSearchQuery, DocumentSearcher, search_documents
from mts_fiscal_intelligence.tools.fiscaldata import FiscalDataQuery, query_fiscaldata

# tool schema
def build_function_tool(*, name: str, description: str, parameters: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": parameters,
        "strict": False
    }

TOOL_DEFINITIONS = [
    build_function_tool(
        name="query_fiscaldata",
        description=(
            "Query direct structured Monthly Treasury Statement "
            "data from Fiscaldata.Treasury.gov API. Currently supports: "
            "Summary of Receipts, Outlays, and the Deficit/Surplus of the U.S. Government and "
            "Summary of Budget and Off-Budget Results and Financing of the U.S. Government. "
            "Do not use it for narrative economic commentary."
        ),
        parameters=FiscalDataQuery.model_json_schema(),
    ),
    build_function_tool(
        name="search_documents",
        description=(
            "Currently only includes June 2026 report."
            "Search Treasury Bulletin documents for narrative "
            "economic context, including inflation, consumer "
            "spending, labor-market conditions, economic "
            "growth, and related treasury commentary. do not "
            "use it as the source for monthly treasury "
            "statement amounts."
        ),
        parameters=DocumentSearchQuery.model_json_schema(),
    ),
]

class Orchestrator:
    def __init__(self, *, document_searcher: DocumentSearcher) -> None:
        self.document_searcher = document_searcher

    @property
    def tool_definition(self) -> list[dict[str,Any]]:
        return TOOL_DEFINITIONS

    def execute(self, *, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        try:
            # Only have two tools so we're rolling with this for now
            if tool_name == "query_fiscaldata":
                query = FiscalDataQuery.model_validate(arguments)

                return query_fiscaldata(query)

            elif tool_name == "search_documents":
                query = DocumentSearchQuery.model_validate(arguments)

                return search_documents(query, searcher=self.document_searcher)

            return ToolResult(
                success=False,
                error=f"Unknown tool: {tool_name}"
            )

        except ValidationError as e:
            return ToolResult(
                success=False,
                error=(f"Invalid arguments for {tool_name}"),
                data={"validation_errors": e.errors(include_url=False)}
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=(f"Unexpected error in tool execution, {tool_name}: {e}")
            )