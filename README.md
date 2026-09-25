# YouTube Summarizer

A modular Gradio application that loads a YouTube transcript, summarizes it, and answers questions using retrieval-augmented generation.

## Architecture

- `youtube_app/config.py` loads and validates environment settings.
- `youtube_app/transcript.py` parses YouTube URLs and normalizes captions.
- `youtube_app/providers.py` contains OpenRouter LLM and embedding adapters.
- `youtube_app/rag.py` chunks transcripts and performs direct FAISS retrieval.
- `youtube_app/chains.py` owns prompts and LCEL chains.
- `youtube_app/service.py` coordinates the application use cases and caches indexes per video.
- `youtube_app/ui.py` contains only the Gradio presentation layer.
- `main.py` is the deployment entry point.

## Local setup

Use Python 3.11 or newer. From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
```

Set `OPENROUTER_API_KEY` in `.env`, then run:

```bash
python main.py
```

Open `http://127.0.0.1:7860` in a browser. The free router is the default chat model; set `OPENROUTER_MODEL` to another OpenRouter model when needed.

## Tests

```bash
pytest
```

The tests use fake embeddings and do not call YouTube or OpenRouter.

## Docker

```bash
docker build -t youtube-summarizer .
docker run --rm -p 7860:7860 --env-file .env youtube-summarizer
```

## GitHub safety

`.env` is ignored and must never be committed. If an API key has ever been shared or committed, revoke it and create a replacement before publishing the repository.
