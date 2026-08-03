from __future__ import annotations
from mts_fiscal_intelligence.models import AgentResult, ToolTrace, SourceReference, ToolResult
from mts_fiscal_intelligence.orchestrator import Orchestrator
from mts_fiscal_intelligence.prompts import SYSTEM_PROMPT
from mts_fiscal_intelligence.llm import LLMClient

import json
from typing import Any

MAX_STEPS = 8

def summarize_tool_result(result: ToolResult) -> str:
    if not result.success:
        return result.error or "Tool execution failed."

    if not isinstance(result.data, dict):
        return "Tool executed successfully"

    if "record_count" in result.data:
        return f"Retrieved {result.data['record_count']} rows."

    if "match_count" in result.data:
        return f"Found {result.data['match_count']} matching sections."

    return "Tool executed successfully"

def execute_function_call(*, function_call: Any, orchestrator: Orchestrator) -> ToolResult:

    try:
        arguments = json.loads(function_call.arguments)

    except (json.JSONDecodeError, ValueError) as e:
        return ToolResult(
            success=False,
            error=(f"the model returned invalid json arguments: {e}")
        )

    return orchestrator.execute(tool_name=function_call.name, arguments=arguments)

def deduplicate_sources(sources: list[SourceReference]) -> list[SourceReference]:
    unique: list[SourceReference] = []
    seen: set[tuple[
            str,
            str | None,
            str | None,
            int | None
        ]
    ] = set()

    for source in sources:
        key = (
            source.title,
            source.url,
            source.document,
            source.page
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(source)

    return unique

def run_agent(*, question: str, llm: LLMClient, orchestrator: Orchestrator) -> AgentResult:
    input_items = [
        {
            "role": "user",
            "content": question
        }
    ]

    traces = []
    collected_sources = []

    for step in range(1, MAX_STEPS + 1):
        response = llm.create_response(
            instructions=SYSTEM_PROMPT,
            input_items=input_items,
            tools=orchestrator.tool_definition
        )

        function_calls = [item for item in response.output if item.type == "function_call"]

        if not function_calls:
            answer = response.output_text.strip()

            if not answer:
                raise RuntimeError("Model returned nothing.")

            return AgentResult(
                answer=response.output_text,
                tool_calls=traces,
                sources=deduplicate_sources(collected_sources)
            )
        
        input_items.extend(response.output)

        for function_call in function_calls:
            result = execute_function_call(function_call=function_call, orchestrator=orchestrator)

            traces.append(
                ToolTrace(
                    step=step,
                    tool_name=function_call.name,
                    arguments=json.loads(function_call.arguments),
                    success=result.success,
                    summary=summarize_tool_result(result),
                    error=result.error,
                    sources=result.sources
                )
            )

        input_items.append({
            "type": "function_call_output",
            "call_id": function_call.call_id,
            "output": result.model_dump_json()
        })

    raise RuntimeError("Agent exceeeded max steps")