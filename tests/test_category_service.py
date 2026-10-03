import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.services.vault_service import create_vault
from app.services.category_services import add_category
from app.session.session import VaultSession


@pytest.fixture
def testing_session():
    test_engine = create_engine("sqlite://")
    Base.metadata.create_all(test_engine)
    TestSession = sessionmaker(bind=test_engine)

    yield TestSession

    test_engine.dispose()

def test_add_category(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(
        db, "Personal", "master123"
    )
    session = VaultSession(vault, vault_key)

    category = add_category(
        db, session,
        "Development",
        "Programming accounts"
    )

    assert category.category_id is not None
    assert category.vault_id == vault.vault_id
    assert category.name == "Development"
    assert category.description == "Programming accounts"

    db.close()