from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///vaultix.db")

# creating the session factory using engine
SessionLocal = sessionmaker(engine)

from app.models.models import  Vault, Category, Credential
Base.metadata.create_all(engine)