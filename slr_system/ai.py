"""AI integration helpers using OpenAI API."""

import os
from typing import List

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def refine_search_string(search_string: str) -> str:
    """Use OpenAI API to suggest refinements to a search string."""
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key or openai is None:
        raise RuntimeError(
            "OpenAI API key not set or openai package not installed"
        )
    openai.api_key = api_key
    prompt = (
        "Suggest an improved academic database search string based on:"\
        f" {search_string}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message["content"].strip()


def ask_question_about_text(text: str, question: str) -> str:
    """Ask a question about a block of text using OpenAI API."""
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key or openai is None:
        raise RuntimeError(
            "OpenAI API key not set or openai package not installed"
        )
    openai.api_key = api_key
    prompt = (
        "Given the following text, answer the question.\n" + text + "\nQuestion: " + question
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message["content"].strip()
