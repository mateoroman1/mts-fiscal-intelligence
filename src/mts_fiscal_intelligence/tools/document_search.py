from mts_fiscal_intelligence.models import AppModel, Field, ToolResult, SourceReference
from utils.document_chunk import DocumentChunk
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

class DocumentSearchQuery(AppModel):
    query: str = Field(min_length=1)
    documents: list[str] = Field(default_factory=list)
    top_k: int = Field(default=5, ge=1, le=20)

class DocumentMatch(AppModel):
    chunk_id: str
    document: str
    pages: list[int]
    text: str
    score: float
    section: str | None = None

class DocumentSearcher:
    def __init__(self, *, chunks_path: Path, embeddings_path: Path, model_name: str) -> None:

        raw_chunks = json.loads(chunks_path.read_text(encoding="utf-8"))

        # validate chunks i guess
        self.chunks = [DocumentChunk.model_validate(chunk) for chunk in raw_chunks]

        self.embeddings = np.load(embeddings_path)

        if len(self.chunks) != len(self.embeddings):
            raise ValueError("Chunk count mismatch with embeddings count.")

        self.model = SentenceTransformer(model_name)

    def search(self, query: DocumentSearchQuery) -> list[DocumentMatch]:
        query_embedding = self.model.encode([query.query], normalize_embeddings=True)[0]

        candidate_indicies = [
            index for index, chunk in enumerate(self.chunks) 
            if (not query.documents or chunk.document in query.documents)
            ] # why am i out of breath???

        if not candidate_indicies:
            return []

        candidate_embeddings = self.embeddings[candidate_indicies]

        scores = candidate_embeddings @ query_embedding

        # explain this one
        ranked_positions = np.argsort(scores)[::-1][:query.top_k]

        matches: list[DocumentMatch] = []

        for position in ranked_positions:
            chunk_index = candidate_indicies[int(position)]

            chunk = self.chunks[chunk_index]

            matches.append(
                DocumentMatch(
                    chunk_id=chunk.chunk_id,
                    document=chunk.document,
                    pages=chunk.pages,
                    text=chunk.text,
                    score=float(scores[position]),
                    section=chunk.section
                )
            )

        return matches

def search_documents(query: DocumentSearchQuery, *, searcher: DocumentSearcher) -> ToolResult:
    try:
        matches = searcher.search(query)
    except Exception as e:
        return ToolResult(
            success=False,
            error=(f"Document Search failed: {e}")
        )

    sources = [SourceReference(
        title=match.document,
        document=match.document,
        page=match.pages[0]
    )
     for match in matches
    ]

    return ToolResult(
        success=True,
        data={
            "query": query.query,
            "match_count": len(matches),
            "matches": [match.model_dump() for match in matches]
        },
        sources=sources
    )