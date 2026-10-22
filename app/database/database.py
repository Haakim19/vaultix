
import os
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def get_database_path() -> Path:
    # Preserve the existing project database during development.
    if not getattr(sys, "frozen", False):
        return Path(__file__).resolve().parents[2] / "vaultix.db"

    # Store packaged-app data in the user's persistent application-data folder.
    app_data = Path(
        QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
    )
    app_data.mkdir(parents=True, exist_ok=True)

    database_path = app_data / "vaultix.db"

    # Import an existing database only if the destination doesn't exist.
    # Never overwrite an existing user database.
    if not database_path.exists():
        bundled_source = Path(sys.executable).resolve().parent / "vaultix.db"
        if bundled_source.is_file():
            import shutil
            shutil.copy2(bundled_source, database_path)

    return database_path


class Base(DeclarativeBase):
    pass


database_path = get_database_path()
engine = create_engine(f"sqlite:///{database_path.as_posix()}")

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


