from mts_fiscal_intelligence.models import AgentResult, ToolTrace

MAX_STEPS = 8

def run_agent(*, question: str, llm: LLMClient, orchestrator: Orchestrator) -> AgentResult:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    traces: list[ToolTrace] = []

    for step in range(1, MAX_STEPS + 1):
        response = llm.respond(messages=messages, tools=orchestrator.tool_definitions())

        if not response.tool_calls:
            if not response.text:
                raise RuntimeError("Model returned neither text nor tool call")

            return AgentResult(
                answer=response.text,
                tool_calls=traces,
                sources=[
                    source for trace in traces 
                    for source in trace.sources
                    ]
            )
        messages.append(llm.assistant_message(response))

        for tool_call in response.tool_calls:
            result = orchestrator.execute_tool(
                name = tool_call.name,
                arguments = tool_call.arguments
            )

            traces.append(
                ToolTrace(
                    step=step,
                    tool_name=tool_call.name,
                    arguments=tool_call.arguments,
                    success=result.success,
                    summary=summarize_tool_result(result),
                    error=result.error,
                    sources=result.sources
                )
            )

        messages.append(llm.tool_result_message(call_id=tool_call.call_id, result=result))

raise RuntimeError("Agent exceeeded max steps")