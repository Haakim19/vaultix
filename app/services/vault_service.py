from app.database.database import SessionLocal
from app.models.models import Vault
from app.security.crypto import(
    generate_salt,
    derive_key,
    encrypt_data
)


def create_vault(vault_name, master_password):
    # generate the salt
    salt = generate_salt()
    
    # generate vault key
    vault_key = derive_key(master_password, salt)
    
    # encrypting the verification data using the vault key
    ciphertext, nonce = encrypt_data(
        "VAULTIX_VERIFICATION",
        vault_key
    )
    
    vault = Vault(
        name = vault_name,
        salt = salt,
        encrypted_verification = ciphertext,
        verification_nonce = nonce
    )
    
    with SessionLocal() as db:
        try:
            db.add(vault)
            db.commit()
            db.refresh(vault)
            db.expunge(vault)
            return vault
        except Exception:
            db.rollback()
            raise
        
def unlock_vault():
    pass