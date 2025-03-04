import os
import sys
import json
from dotenv import load_dotenv
from uuid import UUID
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Tuple
from src.models.base import Base
from src.core.database import engine, get_db
from src.models.paper import Paper
from src.models.venue import Venue
from src.models.author import Author
from src.models.paper_author import PaperAuthor
from src.models.citation import Citation

PAPERS_BATCH_THRESHOLD = 300


def init_db(db_path: str) -> None:
    os.makedirs(os.path.dirname(db_path.split(":///", 1)[1]), exist_ok=True)
    Base.metadata.create_all(engine)


def populate_db(json_path: str) -> None:
    with next(get_db()) as db:
        with open(json_path, 'r') as file:
            papers_data = json.load(file)

        # Process papers
        papers_batch = {}
        paper_authors_batch = []

        for paper_data in papers_data:
            populate_paper(db, paper_data, papers_batch, paper_authors_batch)

            if len(papers_batch) >= PAPERS_BATCH_THRESHOLD:
                db.add_all(list(papers_batch.values()))
                db.add_all(paper_authors_batch)
                db.commit()
                papers_batch.clear()
                paper_authors_batch.clear()

        if papers_batch:
            db.add_all(list(papers_batch.values()))
            db.add_all(paper_authors_batch)
            db.commit()

        # Process citations
        citations_batch = {}

        for paper_data in papers_data:
            populate_citation(db, paper_data, citations_batch)

            if len(citations_batch) >= PAPERS_BATCH_THRESHOLD:
                db.add_all(list(citations_batch.values()))
                db.commit()
                citations_batch.clear()

        if citations_batch:
            db.add_all(list(citations_batch.values()))
            db.commit()

    print("Database populated successfully!")


def populate_paper(
    db: Session,
    paper_data: Dict[str, Any],
    papers_batch: Dict[UUID, Paper],
    paper_authors_batch: List[PaperAuthor]
) -> None:
    paper_id = UUID(paper_data["id"])
    if is_existing_paper(db, paper_id, papers_batch):
        return

    venue = get_or_create_venue(db, paper_data["venue"])

    paper = Paper(
        id=paper_id,
        title=paper_data["title"],
        year=paper_data["year"],
        abstract=paper_data["abstract"],
        venue_id=venue.id
    )
    papers_batch[paper_id] = paper

    for author_name in paper_data["authors"]:
        author = get_or_create_author(db, author_name)
        paper_author = PaperAuthor(paper_id=paper.id, author_id=author.id)
        paper_authors_batch.append(paper_author)


def populate_citation(
    db: Session,
    paper_data: Dict[str, Any],
    citations_batch: Dict[Tuple[UUID, UUID], Citation]
) -> None:
    references = get_references(db, paper_data["references"])

    for reference in references:
        citing_id = UUID(paper_data["id"])
        cited_id = reference.id

        if is_existing_citation(db, citing_id, cited_id, citations_batch):
            continue
        else:
            citation = Citation(citing_paper_id=citing_id, cited_paper_id=cited_id)
            citations_batch[(citing_id, cited_id)] = citation


def is_existing_paper(db: Session, paper_id: UUID, papers_batch: Dict[UUID, Paper]) -> bool:
    is_in_batch = paper_id in papers_batch
    is_in_db = db.query(Paper).filter(Paper.id == paper_id).first() is not None
    return is_in_batch or is_in_db


def is_existing_citation(
    db: Session,
    citing_paper_id: UUID,
    cited_paper_id: UUID,
    citations_batch: Dict[Tuple[UUID, UUID], Citation]
) -> bool:
    is_in_batch = (citing_paper_id, cited_paper_id) in citations_batch
    is_in_db = (
        db.query(Citation)
        .filter(
            Citation.citing_paper_id == citing_paper_id,
            Citation.cited_paper_id == cited_paper_id
        )
        .first()
    )
    return is_in_batch or is_in_db


def get_or_create_venue(db: Session, venue_name: str) -> Venue:
    venue = db.query(Venue).filter(Venue.name == venue_name).first()
    if not venue:
        venue = Venue(name=venue_name)
        db.add(venue)
        db.commit()
        db.refresh(venue)
    return venue


def get_or_create_author(db: Session, author_name: str) -> Author:
    name_parts = author_name.split(' ', 1)
    if len(name_parts) == 1:
        first_name = name_parts[0]
        last_name = None
    else:
        first_name, last_name = name_parts

    author = (
        db.query(Author)
        .filter(Author.first_name == first_name, Author.last_name == last_name)
        .first()
    )

    if not author:
        author = Author(first_name=first_name, last_name=last_name)
        db.add(author)
        db.commit()
        db.refresh(author)
    return author


def get_references(db: Session, ref_ids: List[str]) -> List[Paper]:
    references = []
    for ref_id in ref_ids:
        reference = db.query(Paper).filter(Paper.id == UUID(ref_id)).first()
        if reference:
            references.append(reference)
    return references


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Expected a path to a papers JSON file.")
        sys.exit(1)

    load_dotenv()
    init_db(os.getenv("DATABASE_URL"))
    populate_db(sys.argv[1])
