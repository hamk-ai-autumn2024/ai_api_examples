"""FAISS-based RAG example using the latest OpenAI Python SDK."""

from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Iterable, List, Sequence, Tuple

import faiss
import numpy as np
from openai import OpenAI

SAMPLE_DOCUMENTS = (
    "FAISS is a vector search library for efficient similarity search.",
    "OpenAI offers powerful language models accessible via API.",
    "RAG systems enhance LLMs by augmenting retrieval with generative completion.",
    "SQLite is a lightweight, disk-based database that doesn't require a separate server process.",
    "Python is a versatile programming language popular for data science and web development.",
    "NumPy is a fundamental package for scientific computing with Python.",
    "FAISS supports various indexing methods for different performance needs.",
    "Embeddings convert text into numerical vectors for machine learning tasks.",
    "FAISS can handle large-scale datasets efficiently.",
    "FAISS is developed by Facebook AI Research (FAIR).",
    "RAG stands for Retrieval-Augmented Generation.",
    "Limits of RAG include potential inaccuracies in retrieved documents and reliance on the quality of the underlying data.",
    "Easter eggs are hidden features or messages in software, games, or media.",
    "Easter egg for FAISS: The name 'FAISS' is pronounced like 'face' and stands for Facebook AI Similarity Search.",
)

CLIENT = OpenAI()  # Reads credentials from OPENAI_API_KEY.
EMBEDDING_MODEL = "text-embedding-3-small"
RESPONSE_MODEL = "gpt-5-nano"
DB_PATH = Path("rag_data2.db")


def ensure_documents(conn: sqlite3.Connection, documents: Iterable[str]) -> None:
    """Create the documents table (if needed), reset its contents, and seed sample rows."""
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_documents_id ON documents(id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_documents_content ON documents(content)")
        conn.execute("DELETE FROM documents")
        conn.executemany(
            "INSERT INTO documents (content) VALUES (?)",
            ((doc,) for doc in documents),
        )


def fetch_documents(conn: sqlite3.Connection) -> Sequence[Tuple[int, str]]:
    return conn.execute("SELECT id, content FROM documents ORDER BY id").fetchall()


def get_embedding(text: str) -> List[float]:
    response = CLIENT.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[text],
    )
    return response.data[0].embedding


def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index


def rag_query(
    query: str,
    index: faiss.IndexFlatL2,
    doc_ids: Sequence[int],
    conn: sqlite3.Connection,
    top_k: int = 3,
) -> Tuple[str, List[str]]:
    query_embedding = np.array(get_embedding(query), dtype="float32").reshape(1, -1)
    _, positions = index.search(query_embedding, top_k)

    retrieved_docs: List[str] = []
    for pos in positions[0]:
        if pos >= len(doc_ids):
            continue
        doc_id = doc_ids[pos]
        row = conn.execute("SELECT content FROM documents WHERE id = ?", (doc_id,)).fetchone()
        if row:
            retrieved_docs.append(row[0])

    context = "\n".join(retrieved_docs)

    response = CLIENT.responses.create(
        model=RESPONSE_MODEL,
        input=[
            {
                "role": "system",
                "content": "You are a concise assistant that only uses the supplied context.",
            },
            {
                "role": "user",
                "content": (
                    "Answer the question using only the context.\n\n"
                    f"Context:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
                ),
            },
        ],
        #temperature=0.3,
        max_output_tokens=400,
    )

    return response.output_text.strip(), retrieved_docs


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        ensure_documents(conn, SAMPLE_DOCUMENTS)
        rows = fetch_documents(conn)

        if not rows:
            raise RuntimeError("No documents available to build the FAISS index.")

        doc_ids, contents = zip(*rows)
        embeddings = np.array([get_embedding(text) for text in contents], dtype="float32")
        index = build_faiss_index(embeddings)
        print("Example query: What is FAISS?")
        while True:
            query_text = input("Enter your question (press Enter to exit): ").strip()
            if not query_text:
                break

            answer, sources = rag_query(query_text, index, doc_ids, conn)

            print("Answer:", answer)
            print("Sources:")
            for i, src in enumerate(sources, start=1):
                print(f"  {i}. {src}")
            print()

    print("Goodbye!")


if __name__ == "__main__":
    main()
