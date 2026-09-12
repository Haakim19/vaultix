from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.models.models import Vault
from app.services.vault_service import unlock_vault, create_vault

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

testSession = sessionmaker(engine)

vault_name = "personal"
password = "12345678"

def test_create_vault():
    with testSession() as db:
        created_test_vault = create_vault(vault_name, password, db)
    print(f"vault '{vault_name}' created")

    result = unlock_vault(created_test_vault, password)
    assert result is True
    print("✅ Correct password: vault unlocked")

    wrong_result = unlock_vault(created_test_vault, "123456789")
    assert wrong_result is False
    print("✅ Wrong Password: vault not-unlocked")
    
if __name__ == "__main__":
    test_create_vault()