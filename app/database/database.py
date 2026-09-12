from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.models import models 

class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///vaultix.db")

# creating the session factory using engine
SessionLocal = sessionmaker(engine)

Base.metadata.create_all(engine)