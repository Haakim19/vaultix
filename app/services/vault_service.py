from app.models.models import Vault
from sqlalchemy import select
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
    
    # decrypt the verification data using the vault key created with user password
    try:
        decrypted_data = decrypt_data(
            vault.encrypted_verification,
            vault.verification_nonce,
            new_vault_key
        )
        if decrypted_data == "VAULTIX_VERIFICATION":
            return new_vault_key
        else:
            return None
    except Exception:
        return False

def get_vaults(db):
        vaults = db.execute(select(Vault).order_by(Vault.vault_id)).scalars().all()
        for vault in vaults:
            db.expunge(vault)
        return vaults

def get_vault_by_id(vault_id, db):
    result = db.execute(
        select(Vault).where(Vault.vault_id == vault_id)
    )
    return result.scalar_one_or_none()