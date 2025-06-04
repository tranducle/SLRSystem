"""Database models for SLR System."""

from sqlalchemy import Column, Integer, String, Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, default="")

    studies = relationship("Study", back_populates="project")

class Study(Base):
    __tablename__ = 'studies'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    title = Column(Text)
    abstract = Column(Text)
    doi = Column(String)
    pdf_path = Column(String)

    project = relationship("Project", back_populates="studies")


# Database helpers
engine = None
SessionLocal = None

def init_db(db_url: str):
    global engine, SessionLocal
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal
