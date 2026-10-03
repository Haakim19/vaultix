import pytest
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import create_engine, select
from app.database.database import Base
from app.models.models import Vault, Category, Credential

@pytest.fixture
def TestingSession():
    test_engine = create_engine("sqlite://")
    Base.metadata.create_all(test_engine)

    TestSession = sessionmaker(bind=test_engine)

    yield TestSession

    test_engine.dispose()


def test_vault(TestingSession):
    now = datetime.now(timezone.utc)

    with TestingSession() as session:
        vault = Vault(
            name="test",
            salt=b"salt",
            encrypted_verification=b"encrypted_verification",
            verification_nonce=b"nonce",
            created_at=now,
            updated_at=now,
        )

        session.add(vault)
        session.commit()

        vault_id = vault.vault_id
        assert vault_id is not None

    with TestingSession() as session:
        vault = session.get(Vault, vault_id)

        assert vault is not None
        assert vault.name == "test"
        assert vault.salt == b"salt"

        session.delete(vault)
        session.commit()

    with TestingSession() as session:
        assert session.scalar(select(Vault)) is None


def test_vault_category_relationship(TestingSession):
    now = datetime.now(timezone.utc)

    with TestingSession() as session:
        vault = Vault(
            name="Personal",
            salt=b"salt",
            encrypted_verification=b"encrypted_verification",
            verification_nonce=b"nonce",
            created_at=now,
            updated_at=now,
        )

        category = Category(
            name="Social Media",
            description="Social media accounts",
            vault=vault,
        )

        session.add(vault)
        session.add(category)
        session.commit()

        vault_id = vault.vault_id

    with TestingSession() as session:
        vault = session.get(Vault, vault_id)

        assert vault is not None
        assert len(vault.categories) == 1
        assert vault.categories[0].name == "Social Media"
        assert vault.categories[0].description == "Social media accounts"


def test_vault_credential_relationship(TestingSession):
    now = datetime.now(timezone.utc)

    with TestingSession() as session:
        vault = Vault(
            name="Work",
            salt=b"salt",
            encrypted_verification=b"encrypted_verification",
            verification_nonce=b"nonce",
            created_at=now,
            updated_at=now,
        )

        credential = Credential(
            title="GitHub",
            website="https://github.com",
            encrypted_username=b"encrypted_username",
            username_nonce=b"user_nonce",
            encrypted_password=b"encrypted_password",
            password_nonce=b"password_nonce",
            vault=vault,
        )

        session.add(vault)
        session.add(credential)
        session.commit()

        vault_id = vault.vault_id

    with TestingSession() as session:
        vault = session.get(Vault, vault_id)

        assert vault is not None
        assert len(vault.credentials) == 1
        assert vault.credentials[0].title == "GitHub"
        assert vault.credentials[0].website == "https://github.com"


def test_vault_cascade_delete(TestingSession):
    now = datetime.now(timezone.utc)

    with TestingSession() as session:
        vault = Vault(
            name="Temporary",
            salt=b"salt",
            encrypted_verification=b"encrypted_verification",
            verification_nonce=b"nonce",
            created_at=now,
            updated_at=now,
        )

        category = Category(
            name="Social",
            description="Social accounts",
            vault=vault,
        )

        credential = Credential(
            title="GitHub",
            website="https://github.com",
            encrypted_username=b"encrypted_username",
            username_nonce=b"user_nonce",
            encrypted_password=b"encrypted_password",
            password_nonce=b"password_nonce",
            vault=vault,
            category=category,
        )

        session.add(vault)
        session.commit()
        vault_id = vault.vault_id

    with TestingSession() as session:
        vault = session.get(Vault, vault_id)
        assert vault is not None

        session.delete(vault)
        session.commit()
    with TestingSession() as session:
        assert session.get(Vault, vault_id) is None

        assert session.scalar(
            select(func.count()).select_from(Category)
        ) == 0

        assert session.scalar(
            select(func.count()).select_from(Credential)
        ) == 0
if __name__ == "__main__":
    test_vault()   