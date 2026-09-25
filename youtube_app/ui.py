"""Gradio presentation layer."""

from __future__ import annotations

import gradio as gr

from .service import YouTubeQAService


def create_demo(service: YouTubeQAService) -> gr.Blocks:
    """Build the UI without starting a server or creating global clients."""

    def summarize(video_url: str) -> str:
        try:
            return service.summarize(video_url)
        except Exception as error:  # UI boundary: convert failures into user feedback.
            return f"Unable to summarize this video: {error}"

    def answer(video_url: str, question: str) -> str:
        try:
            return service.answer(video_url, question)
        except Exception as error:  # UI boundary: convert failures into user feedback.
            return f"Unable to answer the question: {error}"

    with gr.Blocks(title="YouTube Summarizer") as demo:
        gr.Markdown("# YouTube Summarizer\nSummarize a transcript or ask questions about its content.")
        video_url = gr.Textbox(label="YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        with gr.Row():
            summarize_button = gr.Button("Summarize", variant="primary")
            question_button = gr.Button("Ask question")
        summary_output = gr.Textbox(label="Summary", lines=6)
        question = gr.Textbox(label="Question", placeholder="What is the main idea?")
        answer_output = gr.Textbox(label="Answer", lines=6)

        summarize_button.click(summarize, inputs=video_url, outputs=summary_output)
        question_button.click(answer, inputs=[video_url, question], outputs=answer_output)

    return demo
