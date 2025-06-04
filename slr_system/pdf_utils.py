"""PDF utilities."""

from typing import Optional

import PyPDF2


def extract_text(pdf_path: str) -> str:
    """Extract all text from a PDF file."""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text
