""""Command line interface for SLR System."""

import os
import csv
from pathlib import Path

import typer
from rich import print

from .models import init_db, SessionLocal, Project, Study
from .pdf_utils import extract_text
from .ai import refine_search_string, ask_question_about_text


def get_db() -> SessionLocal:
    db_url = os.environ.get("SLR_DB_URL", "sqlite:///slr.db")
    Session = init_db(db_url)
    return Session()

app = typer.Typer(help="SLR System CLI")


@app.command()
def create_project(name: str, description: str = ""):
    """Create a new SLR project."""
    session = get_db()
    project = Project(name=name, description=description)
    session.add(project)
    session.commit()
    print(f"Created project {project.id}: {project.name}")


@app.command()
def list_projects():
    """List projects."""
    session = get_db()
    for p in session.query(Project).all():
        print(f"{p.id}: {p.name}")


@app.command()
def import_csv(project_id: int, file: str):
    """Import search results from a CSV file."""
    session = get_db()
    project = session.query(Project).get(project_id)
    if not project:
        print("Project not found")
        raise typer.Exit(1)

    with open(file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            title = row.get("title") or row.get("Title")
            abstract = row.get("abstract") or row.get("Abstract")
            doi = row.get("doi") or row.get("DOI")
            if not title:
                continue
            existing = session.query(Study).filter_by(project=project, title=title).first()
            if existing:
                continue
            study = Study(project=project, title=title, abstract=abstract, doi=doi)
            session.add(study)
            count += 1
        session.commit()
    print(f"Imported {count} studies.")


@app.command()
def refine(
    search_string: str, 
    provider: str = typer.Option("auto", help="AI provider: openai or openrouter")
):
    """Refine a search string using an AI provider."""
    try:
        refined = refine_search_string(search_string, provider)
        print(refined)
    except RuntimeError as exc:
        print(f"[red]Error:[/red] {exc}")


@app.command()
def add_pdf(study_id: int, pdf_path: str):
    """Attach a PDF file to a study."""
    session = get_db()
    study = session.query(Study).get(study_id)
    if not study:
        print("Study not found")
        raise typer.Exit(1)
    study.pdf_path = pdf_path
    session.commit()
    print("PDF attached")


@app.command()
def ask(
    study_id: int,
    question: str,
    provider: str = typer.Option("auto", help="AI provider: openai or openrouter"),
):
    """Ask a question about the study's PDF."""
    session = get_db()
    study = session.query(Study).get(study_id)
    if not study or not study.pdf_path:
        print("Study or PDF not found")
        raise typer.Exit(1)

    text = extract_text(study.pdf_path)
    try:
        answer = ask_question_about_text(text, question, provider)
        print(answer)
    except RuntimeError as exc:
        print(f"[red]Error:[/red] {exc}")


if __name__ == "__main__":
    app()