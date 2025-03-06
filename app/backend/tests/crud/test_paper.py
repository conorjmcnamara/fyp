import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from uuid import UUID
from typing import Generator
from src.models.base import Base
from src.models import Paper, Venue, Author, Citation
from src.crud.paper import get_papers_by_ids


@pytest.fixture
def fake_db() -> Generator[Session, None, None]:
    # Create a fake database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    db = Session()

    # Populate with fake data
    venue = Venue(id=UUID("010d4ce9-0279-4166-ae73-14551ded6404"), name="Venue 1")
    author1 = Author(
        id=UUID("3b2a5324-7b66-4101-9982-3a26e82afa3d"),
        first_name="John",
        last_name="Doe"
    )
    author2 = Author(
        id=UUID("3b2a5324-7b66-4101-9982-3a26e82afa3e"),
        first_name="Jane",
        last_name="Smith"
    )

    paper1 = Paper(
        id=UUID("0abc9de7-e047-44fc-998d-4bf02b9bc9ab"),
        title="Paper 1",
        year=2025,
        abstract="Abstract for paper 1",
        venue=venue,
        authors=[author1, author2]
    )
    paper2 = Paper(
        id=UUID("3b2a5324-7b66-4101-9982-3a26e82afa3d"),
        title="Paper 2",
        year=2025,
        abstract="Abstract for paper 2",
        venue=venue,
        authors=[author1]
    )
    citation = Citation(citing_paper_id=paper1.id, cited_paper_id=paper2.id)

    db.add_all([venue, author1, author2, paper1, paper2, citation])
    db.commit()

    yield db
    db.close()


def test_get_papers_by_ids(fake_db: Session):
    ids = [
        UUID("0abc9de7-e047-44fc-998d-4bf02b9bc9ab"),
        UUID("3b2a5324-7b66-4101-9982-3a26e82afa3d")
    ]

    papers = get_papers_by_ids(fake_db, ids)
    assert len(papers) == 2

    # Validate paper 1
    paper1 = papers[0]
    assert paper1.id == UUID('0abc9de7-e047-44fc-998d-4bf02b9bc9ab')
    assert paper1.title == "Paper 1"
    assert paper1.year == 2025
    assert paper1.abstract == "Abstract for paper 1"
    assert paper1.venue.name == "Venue 1"
    assert len(paper1.authors) == 2
    assert paper1.authors[0].first_name == "John"
    assert paper1.authors[1].first_name == "Jane"

    # Validate paper 2
    paper2 = papers[1]
    assert paper2.id == UUID('3b2a5324-7b66-4101-9982-3a26e82afa3d')
    assert paper2.title == "Paper 2"
    assert paper2.year == 2025
    assert paper2.abstract == "Abstract for paper 2"
    assert paper2.venue.name == "Venue 1"
    assert len(paper2.authors) == 1
    assert paper2.authors[0].first_name == "John"

    # Validate the citation relationships
    assert len(paper1.citing_papers) == 1
    assert paper1.citing_papers[0].cited_paper_id == paper2.id
    assert len(paper2.cited_papers) == 1
    assert paper2.cited_papers[0].citing_paper_id == paper1.id


def test_get_papers_by_ids_missing(fake_db: Session):
    missing_ids = [
        UUID("00000000-0000-0000-0000-000000000000"),
        UUID("11111111-1111-1111-1111-111111111111")
    ]

    papers = get_papers_by_ids(fake_db, missing_ids)
    assert len(papers) == 0
