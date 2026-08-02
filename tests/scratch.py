from mts_fiscal_intelligence.tools.document_search import DocumentSearcher, DocumentSearchQuery
from pathlib import Path

searcher = DocumentSearcher(
    chunks_path=Path("vectorstore/chunks.json"),
    embeddings_path=Path("vectorstore/embeddings.npy"),
    model_name=("sentence-transformers/all-MiniLM-L6-v2")
)

queries = [
    "what did treasury say about inflation?",
    "how was consumer spending changing?",
    "what was happening in the labor market?",
    "why did economic growth slow?",
]

for text in queries:
    print(f"\nQUERY: {text}")

    matches = searcher.search(
        DocumentSearchQuery(
            query=text,
            top_k=3,
        )
    )

    for match in matches:
        print(
            f"\n{match.document}, "
            f"page {match.pages[0]}, "
            f"score={match.score:.3f}"
        )
        print(match.text[:700])