"""Application service coordinating transcript, retrieval, and generation."""

from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings

from .chains import create_qa_chain, create_summary_chain
from .config import Settings
from .providers import create_embeddings, create_llm
from .rag import TranscriptIndex
from .transcript import Transcript, YouTubeTranscriptLoader


class YouTubeQAService:
    """Use case layer for summarizing videos and answering transcript questions."""

    def __init__(
        self,
        settings: Settings,
        transcript_loader: YouTubeTranscriptLoader,
        embeddings: Embeddings,
        llm: BaseChatModel,
    ) -> None:
        self.settings = settings
        self.transcript_loader = transcript_loader
        self.embeddings = embeddings
        self.llm = llm
        self._transcripts: dict[str, Transcript] = {}
        self._indexes: dict[str, TranscriptIndex] = {}

    @classmethod
    def from_settings(cls, settings: Settings) -> "YouTubeQAService":
        return cls(
            settings=settings,
            transcript_loader=YouTubeTranscriptLoader(),
            embeddings=create_embeddings(settings),
            llm=create_llm(settings),
        )

    def _transcript(self, video_url: str) -> Transcript:
        transcript = self.transcript_loader.load(video_url)
        self._transcripts[transcript.video_id] = transcript
        return transcript

    def summarize(self, video_url: str) -> str:
        """Fetch a transcript and generate its summary."""
        transcript = self._transcript(video_url)
        return create_summary_chain(self.llm).invoke({"transcript": transcript.text})

    def answer(self, video_url: str, question: str) -> str:
        """Retrieve relevant transcript context and answer a question."""
        question = question.strip()
        if not question:
            raise ValueError("Please enter a question")

        transcript = self._transcript(video_url)
        index = self._indexes.get(transcript.video_id)
        if index is None:
            index = TranscriptIndex(
                transcript.text,
                self.embeddings,
                self.settings.chunk_size,
                self.settings.chunk_overlap,
            )
            self._indexes[transcript.video_id] = index

        context = index.context_for(question, self.settings.retrieval_k)
        return create_qa_chain(self.llm).invoke({"context": context, "question": question})
