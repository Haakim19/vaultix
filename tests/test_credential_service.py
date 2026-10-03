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


def test_get_credentials_vault_isolation(testing_session):
    db = testing_session()

    personal_vault, personal_key = create_vault(
        db, "Personal", "personal123"
    )
    work_vault, work_key = create_vault(
        db, "Work", "work123"
    )

    personal_session = VaultSession(personal_vault, personal_key)
    work_session = VaultSession(work_vault, work_key)

    add_credentials(
        db, personal_session,
        "GitHub", "https://github.com",
        "personal_user", "personal_pass"
    )
    add_credentials(
        db, work_session,
        "Company Portal", "https://company.com",
        "work_user", "work_pass"
    )

    personal_credentials = get_credentials(db, personal_session)
    work_credentials = get_credentials(db, work_session)

    assert len(personal_credentials) == 1
    assert personal_credentials[0].title == "GitHub"

    assert len(work_credentials) == 1
    assert work_credentials[0].title == "Company Portal"

    db.close()


def test_search_credentials(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(db, "Personal", "master123")
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
    add_credentials(
        db, session,
        "GitLab", "https://gitlab.com",
        "haakim", "gitlab123"
    )
    
    result = search_credentials(db, session, "git")
    
    assert len(result) == 2
    assert {credential.title for credential in result} == {
        "GitHub", "GitLab"
    }
    
    db.close()


def test_get_credentials_by_category(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    from app.services.category_services import add_category

    category = add_category(db, session, "Development")

    add_credentials(
        db, session,
        "GitHub", "https://github.com",
        "haakim", "github123",
        category_id=category.category_id
    )
    add_credentials(
        db, session,
        "Google", "https://google.com",
        "haakim@gmail.com", "google123"
    )

    results = get_credentials_by_category(
        db, session, category.category_id
    )

    assert len(results) == 1
    assert results[0].title == "GitHub"
    assert results[0].category_id == category.category_id

    db.close()


def test_update_credential(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    credential = add_credentials(
        db, session,
        "GitHub", "https://github.com",
        "old_user", "old_password",
        notes="Old notes"
    )

    from app.services.credential_service import update_credential

    updated = update_credential(
        db, session, credential,
        title="GitHub Updated",
        website="https://github.com",
        username="new_user",
        password="new_password",
        notes="New notes"
    )

    username, password, notes = decrypt_credential(updated, session)

    assert updated.title == "GitHub Updated"
    assert username == "new_user"
    assert password == "new_password"
    assert notes == "New notes"

    db.close()

def test_update_credential_preserves_unchanged_encryption(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    credential = add_credentials(
        db, session,
        "GitHub", "https://github.com",
        "haakim", "github123",
        notes="My account"
    )

    original_username = credential.encrypted_username
    original_username_nonce = credential.username_nonce
    original_password = credential.encrypted_password
    original_password_nonce = credential.password_nonce
    original_notes = credential.encrypted_notes
    original_notes_nonce = credential.notes_nonce

    updated = update_credential(
        db, session, credential,
        title="GitHub Updated",
        website="https://github.com",
        username="haakim",
        password="github123",
        notes="My account"
    )

    assert updated.encrypted_username == original_username
    assert updated.username_nonce == original_username_nonce
    assert updated.encrypted_password == original_password
    assert updated.password_nonce == original_password_nonce
    assert updated.encrypted_notes == original_notes
    assert updated.notes_nonce == original_notes_nonce

    db.close()

def test_delete_credential(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    credential = add_credentials(
        db, session,
        "GitHub", "https://github.com",
        "haakim", "github123"
    )
    
    delete_credential(db, session, credential)
    
    credential = get_credentials(db, session)
    
    assert len(credential) == 0
    
    db.close()


def test_delete_credential_from_another_vault(testing_session):
    db = testing_session()

    personal_vault, personal_key = create_vault(
        db, "Personal", "personal123"
    )
    work_vault, work_key = create_vault(
        db, "Work", "work123"
    )

    personal_session = VaultSession(personal_vault, personal_key)
    work_session = VaultSession(work_vault, work_key)

    credential = add_credentials(
        db, personal_session,
        "GitHub", "https://github.com",
        "haakim", "github123"
    )

    with pytest.raises(ValueError):
        delete_credential(db, work_session, credential)

    remaining = get_credentials(db, personal_session)

    assert len(remaining) == 1
    assert remaining[0].title == "GitHub"

    db.close()

def test_update_credential_from_another_vault(testing_session):
    db = testing_session()

    personal_vault, personal_key = create_vault(
        db, "Personal", "personal123"
    )
    work_vault, work_key = create_vault(
        db, "Work", "work123"
    )

    personal_session = VaultSession(personal_vault, personal_key)
    work_session = VaultSession(work_vault, work_key)

    credential = add_credentials(
        db, personal_session,
        "GitHub", "https://github.com",
        "haakim", "github123"
    )
    
    with pytest.raises(ValueError):
        update_credential(
            db, work_session, credential,
            title="Changed",
            website="https://example.com",
            username="other_user",
            password="other_password",
            notes="Changed notes"
        )
    
    remaining = get_credentials(db, personal_session)

    assert len(remaining) == 1
    assert remaining[0].title == "GitHub"

    db.close()