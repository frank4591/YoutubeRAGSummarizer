"""YouTube URL parsing and transcript loading."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


_VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")


class TranscriptUnavailableError(RuntimeError):
    """Raised when a video has no usable transcript."""


@dataclass(frozen=True)
class Transcript:
    """Normalized transcript content and source metadata."""

    video_id: str
    text: str
    language_code: str


def extract_video_id(url: str) -> str:
    """Extract a YouTube video ID from watch, short, embed, shorts, or live URLs."""
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower().split(":", 1)[0]
    video_id = ""

    if host in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/", 1)[0]
    elif host.endswith("youtube.com"):
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        else:
            parts = parsed.path.strip("/").split("/")
            if len(parts) >= 2 and parts[0] in {"embed", "shorts", "live"}:
                video_id = parts[1]

    if not _VIDEO_ID_PATTERN.fullmatch(video_id):
        raise ValueError("Invalid YouTube URL or video ID")
    return video_id


class YouTubeTranscriptLoader:
    """Load the best available transcript, preferring manually created English."""

    def __init__(self, api: YouTubeTranscriptApi | None = None) -> None:
        self.api = api or YouTubeTranscriptApi()

    def load(self, url: str) -> Transcript:
        video_id = extract_video_id(url)
        available = list(self.api.list(video_id))
        english = [item for item in available if item.language_code == "en"]
        selected = next((item for item in english if not item.is_generated), None)
        selected = selected or next(iter(english), None) or next(iter(available), None)
        if selected is None:
            raise TranscriptUnavailableError("No transcript is available for this video")

        return Transcript(
            video_id=video_id,
            text=format_transcript(selected.fetch()),
            language_code=selected.language_code,
        )


def format_transcript(entries: object) -> str:
    """Normalize transcript snippets from current and older API response shapes."""
    lines: list[str] = []
    for entry in entries:  # type: ignore[union-attr]
        if isinstance(entry, dict):
            text = entry.get("text", "")
            start = entry.get("start", 0)
        else:
            text = getattr(entry, "text", "")
            start = getattr(entry, "start", 0)
        if text:
            lines.append(f"Text: {text} Start: {start}")
    return "\n".join(lines)
