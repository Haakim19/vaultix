from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from app.database.database import Base, Vault


engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

testSession = sessionmaker(engine)


def test_vault():
    now = datetime.now(timezone.utc)
    with testSession() as session:
        with session.begin():
            vault = Vault(  name = "test", 
                            salt = b"salt",
                            encrypted_verification = b"encrypted_varification",
                            verification_nonce = b"nonce",
                            created_at =now,
                            updated_at = now) 
            session.add(vault)
            session.flush()
            pid = vault.vault_id
            
    with testSession() as session:
        with session.begin():
            vault = session.get(Vault, pid)
            assert vault.name == "test" and vault.salt == b"salt"
            session.delete(vault)
        
    
    with testSession() as session:
        assert session.scalar(select(Vault)) is None
    
    print("✅ passed")
    

if __name__ == "__main__":
    test_vault()   