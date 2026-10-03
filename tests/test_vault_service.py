import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.services.vault_service import (unlock_vault, 
                                        create_vault, 
                                        get_vault_by_id,
                                        vault_name_exists,
                                        get_vaults)

@pytest.fixture
def testing_session():
    test_engine = create_engine("sqlite://")
    Base.metadata.create_all(test_engine)

    TestSession = sessionmaker(bind=test_engine)

    yield TestSession

    test_engine.dispose()

def test_vault_name_exists(testing_session):
    with testing_session() as db:
        create_vault(db, "Personal Vault", "12345678")

        assert vault_name_exists(db, "Personal Vault")
        assert vault_name_exists(db, "personal vault")
        assert vault_name_exists(db, " Personal Vault ")

        assert not vault_name_exists(db, "Work Vault")


def test_create_vault_with_empty_name(testing_session):
    with testing_session() as db:
        vault, _ = create_vault(db, "", "12345678")

        assert vault.name == ""


def test_create_vault(testing_session):
    with testing_session() as db:
        vault, vault_key = create_vault(
            db,
            "Personal Vault",
            "12345678"
        )

        assert vault.vault_id is not None
        assert vault.name == "Personal Vault"
        assert isinstance(vault_key, bytes)
        assert len(vault_key) == 32


def test_unlock_vault(testing_session):
    with testing_session() as db:
        vault, original_key = create_vault(
            db,
            "Personal Vault",
            "12345678"
        )

        correct_key = unlock_vault(vault, "12345678")
        wrong_key = unlock_vault(vault, "wrongpassword")

        assert correct_key == original_key
        assert wrong_key is None


def test_get_vaults(testing_session):
    with testing_session() as db:
        create_vault(db, "Personal Vault", "12345678")
        create_vault(db, "Work Vault", "87654321")

        vaults = get_vaults(db)

        assert len(vaults) == 2
        assert [vault.name for vault in vaults] == [
            "Personal Vault",
            "Work Vault"
        ]


def test_get_vault_by_id(testing_session):
    with testing_session() as db:
        created_vault, _ = create_vault(
            db,
            "Personal Vault",
            "12345678"
        )

        vault_id = created_vault.vault_id

        found_vault = get_vault_by_id(db, vault_id)
        missing_vault = get_vault_by_id(db, 999)

        assert found_vault is not None
        assert found_vault.vault_id == vault_id
        assert found_vault.name == "Personal Vault"
        assert missing_vault is None