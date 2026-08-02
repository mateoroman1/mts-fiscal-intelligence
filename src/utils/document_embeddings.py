import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

VECTORSTORE_DIR = Path("vectorstore")
CHUNKS_PATH = VECTORSTORE_DIR / "chunks.json"
EMBEDDINGS_PATH = VECTORSTORE_DIR / "embeddings.npy"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def main():
    chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))

    texts = [chunk["text"] for chunk in chunks]

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    np.save(EMBEDDINGS_PATH, embeddings)

    print(f"Saved {len(embeddings)} embeddings to {EMBEDDINGS_PATH}")

if __name__ == "__main__":
    main()