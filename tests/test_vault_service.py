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
    
if __name__ == "__main__":
    test_create_vault()