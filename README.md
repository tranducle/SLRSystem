# SLRSystem

This project provides a basic command line interface to manage systematic literature reviews (SLRs) while following the PRISMA workflow. It stores projects and studies in an SQLite database and integrates with OpenAI or OpenRouter APIs for refining search strings and asking questions about PDF contents.

## Features

- Create projects to organize your SLRs.
- Import search results from CSV files and avoid duplicates.
- Attach PDF files to studies.
- Extract text from PDFs and ask questions using a language model (OpenAI or OpenRouter).
- Refine search strings using OpenAI or OpenRouter.

## Requirements

- Python 3.10+
- An API key for your chosen AI provider.  
  Set `OPENAI_API_KEY` for OpenAI or `OPENROUTER_API_KEY` for OpenRouter.

## Installation

Install the required packages:

```bash
pip install -r requirements.txt

Configuration
	•	The database location can be configured with the SLR_DB_URL environment variable.
	•	Set OPENAI_API_KEY or OPENROUTER_API_KEY as environment variables to authenticate with your AI provider.

Usage

The CLI is implemented with Typer:

View all commands and options

python -m slr_system.cli --help

Create a project

python -m slr_system.cli create-project "My Review"

Refine a search string using AI

By default, provider is "auto". You can specify --provider openai or --provider openrouter if desired.

python -m slr_system.cli refine "cancer genomics"
python -m slr_system.cli refine "cancer genomics" --provider openrouter

Import studies from a CSV file

The CSV must have a title column, and optionally abstract, doi.

python -m slr_system.cli import-csv 1 results.csv

Attach a PDF to a study

python -m slr_system.cli add-pdf 2 paper.pdf

Ask a question about a study’s PDF

You can optionally specify the AI provider:

python -m slr_system.cli ask 2 "What methods were used?"
python -m slr_system.cli ask 2 "What methods were used?" --provider openrouter


⸻

Environment Variables Summary
	•	SLR_DB_URL: Path/URL to the database (default is SQLite file slr.db)
	•	OPENAI_API_KEY: Your OpenAI API key (for OpenAI-based features)
	•	OPENROUTER_API_KEY: Your OpenRouter API key (for OpenRouter-based features)

⸻

Feel free to open an issue or submit a PR if you have suggestions or improvements!

