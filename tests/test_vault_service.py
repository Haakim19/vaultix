from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.models.models import Vault
from app.session.session import VaultSession
from app.services.credential_service import (   add_credentials, 
                                                get_credentials, 
                                                decrypt_credential,
                                                update_credential)
from app.security.crypto import decrypt_data
from app.services.vault_service import (unlock_vault, 
                                        create_vault, 
                                        get_vault_by_id)

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

TestingSession = sessionmaker(engine)

vault_name = "home"
password = "12345678"

def test_create_vault():
    with TestingSession() as db:
        created_test_vault, vault_key = create_vault(db, vault_name, password)
    print(f"vault '{vault_name}' created")

    found_vault = get_vault_by_id(
        db,
        created_test_vault.vault_id
    )


    assert found_vault is not None
    assert isinstance(vault_key, bytes)
    assert len(vault_key) == 32
    assert found_vault.name == vault_name
    print(f"✅ Found the vault '{vault_name}'")

    result = unlock_vault(created_test_vault, password)

    assert result is not None
    assert isinstance(result, bytes)
    assert len(result) == 32
    print("✅ Correct password: vault unlocked")

    wrong_result = unlock_vault(created_test_vault, "123456789")
    assert wrong_result is None
    print("✅ Wrong Password: vault not-unlocked")
    

def test_add_credentials():
    with TestingSession() as db:
        vault, vault_key = create_vault(
            db,
            "Test Vault",
            "12345678"
        )

        session = VaultSession(vault, vault_key)

        credential = add_credentials(
            db,
            session,
            "GitHub",
            "https://github.com",
            "haakim19",
            "my-secret-password"
        )

        assert credential.credential_id is not None

        assert credential.encrypted_username != b"haakim19"
        assert credential.encrypted_password != b"my-secret-password"

        username = decrypt_data(
            credential.encrypted_username,
            credential.username_nonce,
            session.vault_key
        )

        password = decrypt_data(
            credential.encrypted_password,
            credential.password_nonce,
            session.vault_key
        )

        assert username == "haakim19"
        assert password == "my-secret-password"

def test_get_credentials():
    with TestingSession() as db:
        vault, vault_key = create_vault(
            db,
            "Personal Vault",
            "12345678"
        )

        session = VaultSession(vault, vault_key)

        add_credentials(
            db,
            session,
            "GitHub",
            "https://github.com",
            "haakim19",
            "github-password"
        )

        add_credentials(
            db,
            session,
            "Google",
            "https://google.com",
            "haakim19@gmail.com",
            "google-password"
        )

        credentials = get_credentials(db, session)

        assert len(credentials) == 2
        assert credentials[0].title == "GitHub"
        assert credentials[1].title == "Google"

def test_credentials_are_isolated_between_vaults():
    with TestingSession() as db:
        personalVault, personalKey = create_vault(
            db,
            "personal",
            "12345678")
        
        workVault, workKey = create_vault(
            db,
            "work",
            "87654321"
        )
        
        personalSession = VaultSession(personalVault, personalKey)
        workSession = VaultSession(workVault, workKey)
        
        add_credentials(
            db,
            personalSession,
            "GitHub",
            "https://github.com",
            "haakim19",
            "personal-password"
        )

        add_credentials(
            db,
            workSession,
            "Slack",
            "https://slack.com",
            "haakim19",
            "work-password"
        )
        
        personalCredentials = get_credentials(db, personalSession)
        workCredentials = get_credentials(db, workSession)
        
        assert len(personalCredentials) == 1
        assert personalCredentials[0].title == "GitHub"
        
        assert len(workCredentials) == 1
        assert workCredentials[0].title == "Slack"

        personalCredential = personalCredentials[0]
        username, pwsh = decrypt_credential(
            personalCredential,
            personalSession
        )
        assert username == "haakim19"
        assert pwsh == "personal-password"
        
        updated = update_credential(
            db,
            personalSession,
            personalCredential,
            "Updated Gmail",
            "https://gmail.com",
            "new_username",
            "old_password",)
        
        updated_username, updated_password = decrypt_credential(
            updated,
            personalSession
        )
        assert updated_username == "new_username"
        assert updated_password == "old_password"
        assert updated.title == "Updated Gmail"

if __name__ == "__main__":
    test_add_credentials()