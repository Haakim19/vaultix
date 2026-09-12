from app.models.models import Vault
from app.security.crypto import(
    generate_salt,
    derive_key,
    encrypt_data,
    decrypt_data
)

def create_vault(vault_name : str, master_password: str, db) -> Vault:
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
    
    try:
        db.add(vault)
        db.commit()
        db.refresh(vault)
        db.expunge(vault)
        return vault
    except Exception:
        db.rollback()
        raise

def unlock_vault(vault, master_password):
    new_vault_key = derive_key(master_password, vault.salt)
    
    # decrypt the varification data using the vault key created with user password
    try:
        decrypted_data = decrypt_data(
            vault.encrypted_verification,
            vault.verification_nonce,
            new_vault_key
        )
        return decrypted_data == "VAULTIX_VERIFICATION"
    except Exception:
        return False