from pathlib import Path
from mts_fiscal_intelligence.models import AppModel, Field
import re
import fitz
import math

# DOCUMENTS_DIR = Path("documents")

class ExtractedPage(AppModel):
    document: str = Field(min_length=1)
    page: int = Field(ge=1)
    text: str

def extract_pdf_pages(path: Path) -> list[ExtractedPage]:
    pages: list[ExtractedPage] = []

    with fitz.open(path) as document:
        for page_index, page in enumerate(document):
            pages.append(
                ExtractedPage(
                    document=path.name,
                    page=page_index + 1,
                    text=clean_extracted_text(page.get_text("text"))
                )
            )

    return pages

def narrative_score(text: str) -> float:

    words = text.split()

    if not words:
        return 0.0

    word_count = len(words)

    sentence_markers = sum(
        text.count(marker) for marker in ".!?"
        )

    alphabetical_words = sum(
        word.strip(".,;:()[]").isalpha() for word in words
    )

    alphabetical_ratio = alphabetical_words / len(words)
    sentence_ratio = sentence_markers / len(words)

    word_score = alphabetical_ratio + sentence_ratio

    length_weight = 1- math.exp(-word_count / 100)

    return word_score * length_weight

def clean_extracted_text(text: str) -> str:

    text = text.replace("\u00a0", " ")

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r" *\n *",
        "\n",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


# if __name__ == "__main__":
#     pages = extract_pdf_pages(path=(
#         DOCUMENTS_DIR
#         / "Treasury_Bulletin_2026_06.pdf"))
#     ranked_pages = sorted(pages, key=lambda page: narrative_score(page.text))

#     for page in ranked_pages[:10]:
#         print(f"Page: {page.page}") 
#         print(f"Score: {narrative_score(page.text)}") 
#         print(page.text[:900])
#         print()
