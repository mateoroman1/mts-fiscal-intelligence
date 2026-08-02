from pathlib import Path
from mts_fiscal_intelligence.models import AppModel, Field
from utils.document_extract import extract_pdf_pages, clean_extracted_text, ExtractedPage
import re
import fitz
import math
import json

DOCUMENTS_DIR = Path("documents")
VECTORSTORE_DIR = Path("vectorstore")
CHUNKS_PATH = VECTORSTORE_DIR / "chunks.json"

class DocumentChunk(AppModel):
    chunk_id: str = Field(min_length=1)
    document: str = Field(min_length=1)
    pages: list[int] = Field(min_length=1)
    text: str = Field(min_length=1)
    section: str | None = None

def pages_to_chunks(pages: list[ExtractedPage]) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []

    for index, page in enumerate(pages):
        chunks.append(
            DocumentChunk(
                chunk_id=(
                    f"{Path(page.document).stem}-{index:03d}"
                ),
                document=page.document,
                pages=[page.page],
                text=page.text
            )
        )
    return chunks

def build_chunks() -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []

    for path in sorted(
        DOCUMENTS_DIR.glob("*.pdf")
    ):
        pages = extract_pdf_pages(path)

        chunks.extend(pages_to_chunks(pages))

    return chunks

def main() -> None:
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    chunks = build_chunks()

    serialized = [chunk.model_dump() for chunk in chunks]

    CHUNKS_PATH.write_text(
        json.dumps(
            serialized,
            indent=2
        ),
        encoding="utf-8"
    )

    print(f"Wrote {len(chunks)} chunks to {CHUNKS_PATH}")

if __name__ == "__main__":
    main()