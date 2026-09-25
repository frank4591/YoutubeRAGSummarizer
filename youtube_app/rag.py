"""Transcript chunking and vector retrieval."""

from __future__ import annotations

import faiss
import numpy as np
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TranscriptIndex:
    """In-memory FAISS index for one transcript."""

    def __init__(self, text: str, embeddings: Embeddings, chunk_size: int, chunk_overlap: int) -> None:
        if not text.strip():
            raise ValueError("Cannot index an empty transcript")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self._documents = [Document(page_content=chunk) for chunk in splitter.split_text(text)]
        vectors = np.asarray(
            embeddings.embed_documents([document.page_content for document in self._documents]),
            dtype="float32",
        )
        if vectors.ndim != 2 or not len(vectors):
            raise ValueError("The embedding provider returned no usable vectors")
        self._embeddings = embeddings
        self._index = faiss.IndexFlatL2(vectors.shape[1])
        self._index.add(vectors)

    def search(self, query: str, k: int) -> list[Document]:
        """Return the most relevant transcript chunks."""
        if k <= 0:
            return []
        limit = min(k, len(self._documents))
        query_vector = np.asarray([self._embeddings.embed_query(query)], dtype="float32")
        _, indices = self._index.search(query_vector, limit)
        return [self._documents[index] for index in indices[0] if index >= 0]

    def context_for(self, query: str, k: int) -> str:
        """Return retrieved chunks formatted for an LLM prompt."""
        documents = self.search(query, k)
        return "\n\n".join(document.page_content for document in documents)
