"""Prompt and LCEL chain construction."""

from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


SUMMARY_PROMPT = """Summarize the following YouTube transcript in one concise paragraph.
Ignore timestamps and focus on the spoken content.

Transcript:
{transcript}
"""

QA_PROMPT = """Answer the question using only the supplied video context.
If the context does not contain the answer, say that clearly.

Video context:
{context}

Question:
{question}
"""


def create_summary_chain(llm: BaseChatModel):
    """Create the transcript summarization chain."""
    return PromptTemplate.from_template(SUMMARY_PROMPT) | llm | StrOutputParser()


def create_qa_chain(llm: BaseChatModel):
    """Create the retrieval question-answering chain."""
    return PromptTemplate.from_template(QA_PROMPT) | llm | StrOutputParser()
