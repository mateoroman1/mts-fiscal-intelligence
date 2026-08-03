from pathlib import Path

from mts_fiscal_intelligence.agent import run_agent
from mts_fiscal_intelligence.config import settings
from mts_fiscal_intelligence.llm import LLMClient
from mts_fiscal_intelligence.orchestrator import Orchestrator
from mts_fiscal_intelligence.tools.document_search import DocumentSearcher

def build_document_searcher() -> DocumentSearcher:
    return DocumentSearcher(
        chunks_path=Path("vectorstore/chunks.json"),
        embeddings_path=Path("vectorstore/embeddings.npy"),
        model_name=("sentence-transformers/all-MiniLM-L6-v2")
    )

def main() -> None:
    document_searcher = build_document_searcher()

    orchestrator = Orchestrator(document_searcher=document_searcher)

    llm = LLMClient(api_key=settings.openai_api_key, model=settings.llm_model)

    question = input("Ask an MTS Question:\n> ").strip()

    if not question:
        print("No Input Recieved.")
        return

    result = run_agent(
        question=question,
        llm=llm,
        orchestrator=orchestrator
    )

    print("\nAnswer:\n")
    print(result.answer)

    if result.tool_calls:
        print("\nTool Trace:")

        for trace in result.tool_calls:
            status = ("OK" if trace.success else "Failed")

            print(f"- Step {trace.step}: {trace.tool_name} [{status}]")

            print(f" {trace.summary}")

    if result.sources:
        print("\nSources:")

        for source in result.sources:
            location_parts = []

            if source.document:
                location_parts.append(source.document)

            if source.page:
                location_parts.append(f"Page: {source.page}")

            location = ", ".join(location_parts)

            print(f"- {source.title}")
            print(f": {location if location else ""}")

if __name__ == "__main__":
    main()