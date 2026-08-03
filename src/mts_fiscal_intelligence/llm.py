from __future__ import annotations
from typing import Any
from openai import OpenAI

class LLMClient:
    def __init__(self, *, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)

        self.model = model

    def create_response(self, *, instructions: str, input_items: list[dict[str, Any]], tools: list[dict[str, Any]]) -> Any:
        return self.client.responses.create(
            model=self.model, 
            instructions=instructions, 
            input=input_items, 
            tools=tools)