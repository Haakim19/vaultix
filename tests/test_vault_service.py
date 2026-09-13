from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.models.models import Vault
from app.services.vault_service import (unlock_vault, 
                                        create_vault, 
                                        get_vault_by_id)

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

testSession = sessionmaker(engine)

vault_name = "personal"
password = "12345678"

def test_create_vault():
    with testSession() as db:
        created_test_vault = create_vault(vault_name, password, db)
    print(f"vault '{vault_name}' created")

    found_vault = get_vault_by_id(
        created_test_vault.vault_id,
        db
    )
    
    assert found_vault is not None
    assert found_vault.name == vault_name
    print(f"✅ Found the vault '{vault_name}'")

    result = unlock_vault(created_test_vault, password)
    assert result is True
    print("✅ Correct password: vault unlocked")

    wrong_result = unlock_vault(created_test_vault, "123456789")
    assert wrong_result is False
    print("✅ Wrong Password: vault not-unlocked")
    
if __name__ == "__main__":
    test_create_vault()