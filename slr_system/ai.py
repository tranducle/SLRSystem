"""AI integration helpers using OpenAI or OpenRouter APIs."""

import os
from typing import List
import json
import requests

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENROUTER_API_KEY_ENV = "OPENROUTER_API_KEY"


def _chat_completion(messages: List[dict], provider: str = "auto") -> str:
    """Call either OpenAI or OpenRouter chat completion API."""
    if provider == "auto":
        provider = (
            "openrouter" if os.getenv(OPENROUTER_API_KEY_ENV) else "openai"
        )

    if provider == "openrouter":
        api_key = os.getenv(OPENROUTER_API_KEY_ENV)
        if not api_key:
            raise RuntimeError("OpenRouter API key not set")
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": "openai/gpt-3.5-turbo", "messages": messages},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    elif provider == "openai":
        api_key = os.getenv(OPENAI_API_KEY_ENV)
        if not api_key or openai is None:
            raise RuntimeError(
                "OpenAI API key not set or openai package not installed"
            )
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        return response.choices[0].message["content"].strip()
    else:
        raise ValueError("Unknown provider")


def refine_search_string(search_string: str, provider: str = "auto") -> str:
    """Suggest refinements to a search string using an AI provider."""
    prompt = f"Suggest an improved academic database search string based on: {search_string}"
    return _chat_completion([{"role": "user", "content": prompt}], provider)


def ask_question_about_text(text: str, question: str, provider: str = "auto") -> str:
    """Ask a question about a block of text using an AI provider."""
    prompt = "Given the following text, answer the question.\n" + text + "\nQuestion: " + question
    return _chat_completion([{"role": "user", "content": prompt}], provider)