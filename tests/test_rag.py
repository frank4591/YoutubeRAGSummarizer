from langchain_core.embeddings import Embeddings

from youtube_app.rag import TranscriptIndex


class FakeEmbeddings(Embeddings):
    def _vector(self, text: str) -> list[float]:
        return [float(len(text)), float(text.lower().count("python"))]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._vector(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._vector(text)


def test_transcript_index_returns_context():
    index = TranscriptIndex(
        "Python is useful.\n\nCooking is different.",
        FakeEmbeddings(),
        chunk_size=100,
        chunk_overlap=0,
    )
    assert "Python is useful." in index.context_for("python", k=1)
