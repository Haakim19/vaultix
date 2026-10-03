import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.models.models import Credential
from app.services.vault_service import create_vault
from app.services.credential_service import (
    add_credentials, 
    decrypt_credential, 
    get_credentials,
    search_credentials,
    get_credentials_by_category,
    update_credential,
    delete_credential)
from app.session.session import VaultSession


@pytest.fixture
def testing_session():
    test_engine = create_engine("sqlite://")
    Base.metadata.create_all(test_engine)

    TestSession = sessionmaker(bind=test_engine)

    yield TestSession

    test_engine.dispose()


def test_add_credentials(testing_session):
    with testing_session() as db:
        vault, vault_key = create_vault(
            db,
            "Personal Vault",
            "12345678"
        )
        session = VaultSession(vault, vault_key)

        credential = add_credentials(
            db,
            session,
            title="GitHub",
            website="https://github.com",
            username="haakim19",
            password="my-secret-password"
        )

        assert credential.credential_id is not None
        assert credential.title == "GitHub"
        assert credential.website == "https://github.com"

        assert credential.encrypted_username != b"haakim19"
        assert credential.encrypted_password != b"my-secret-password"

        assert credential.encrypted_notes is None
        assert credential.notes_nonce is None

def test_decrypt_credential(testing_session):
    with testing_session() as db:
        vault, vault_key = create_vault(
            db, 
            "Personal Vault",
            "12345678"
        )
        session = VaultSession(vault, vault_key)
        
        credential = add_credentials(
            db,
            session,
            title="GitHub",
            website="https://github.com",
            username="haakim19",
            password="my-secret-password",
            notes="My GitHub account"
        )
        
        username, password, notes = decrypt_credential(
            credential,
            session
        )
        
        assert username == "haakim19"
        assert password == "my-secret-password"
        assert notes == "My GitHub account"

def test_get_credentials(testing_session):
    db = testing_session()
    
    vault, vault_key = create_vault(db, "Personal", "12345678")
    session = VaultSession(vault, vault_key)
    
    add_credentials(
        db, session,
        "GitHub", "https://github.com",
        "haakim", "github123"
    )
    add_credentials(
        db, session,
        "Google", "https://google.com",
        "haakim@gmail.com", "google123"
    )
    credentials = get_credentials(db, session)
    
    assert len(credentials) == 2
    assert credentials[0].title == "GitHub"
    assert credentials[1].title == "Google"
    
    db.close()


