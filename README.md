# SLRSystem

This project provides a basic command line interface to manage systematic literature reviews (SLRs) while following the PRISMA workflow. It stores projects and studies in an SQLite database and integrates with OpenAI or OpenRouter APIs for refining search strings and asking questions about PDF contents.
=======


## Features

- Create projects to organise your SLRs.
- Import search results from CSV files and avoid duplicates.
- Attach PDF files to studies.
- Extract text from PDFs and ask questions using an LLM.

- Refine search strings via OpenAI or OpenRouter.
=======


## Requirements

- Python 3.10+
- An API key for your chosen AI provider. Set `OPENAI_API_KEY` for OpenAI or `OPENROUTER_API_KEY` for OpenRouter.
=======


## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

The CLI is implemented with [Typer](https://typer.tiangolo.com/):

```bash
python -m slr_system.cli --help
```

Create a project:

```bash
python -m slr_system.cli create-project "My Review"
```

Refine a search string using AI:

```bash
python -m slr_system.cli refine "cancer genomics" --provider openrouter
```

=======

Import studies from a CSV file (must have `title` and optional `abstract`, `doi` columns):

```bash
python -m slr_system.cli import-csv 1 results.csv
```

Attach a PDF to a study and ask a question about it:

```bash
python -m slr_system.cli add-pdf 2 paper.pdf
python -m slr_system.cli ask 2 "What methods were used?"

# specify provider explicitly if desired
python -m slr_system.cli ask 2 "What methods were used?" --provider openrouter
=======


The database location can be configured with the `SLR_DB_URL` environment variable.
