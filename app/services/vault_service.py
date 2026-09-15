from sqlalchemy import select
from app.models.models import Vault
from app.security.crypto import (
    generate_salt,
    derive_key,
    encrypt_data,
    decrypt_data,
)

VERIFICATION_PLAINTEXT = "VAULTIX_VERIFICATION"

def any_vault_exist(db) -> bool:
    return db.execute(
        select(Vault.vault_id).limit(1)
    ).first() is not None


def vault_name_exists(db, vault_name: str) -> bool:
    normalized_name = vault_name.strip().lower()

    vaults = db.execute(select(Vault)).scalars().all()

    return any(
        vault.name.strip().lower() == normalized_name
        for vault in vaults
    )


def create_vault(   db, 
                    vault_name: str, 
                    master_password: str
                    ) -> tuple[Vault, bytes]:
    salt = generate_salt()
    vault_key = derive_key(master_password, salt)
    ciphertext, nonce = encrypt_data(VERIFICATION_PLAINTEXT, vault_key)

    vault = Vault(
        name=vault_name,
        salt=salt,
        encrypted_verification=ciphertext,
        verification_nonce=nonce,
    )
    db.add(vault)
    db.commit()
    db.refresh(vault)
    db.expunge(vault)
    return vault, vault_key


def unlock_vault(vault: Vault, master_password: str) -> bytes | None:
    candidate_key = derive_key(master_password, vault.salt)
    try:
        decrypted = decrypt_data(
            vault.encrypted_verification,
            vault.verification_nonce,
            candidate_key,
        )
    except Exception:
        return None

    if decrypted == VERIFICATION_PLAINTEXT:
        return candidate_key
    return None


def get_vaults(db):
    vaults = db.execute(
        select(Vault).order_by(Vault.vault_id)
    ).scalars().all()
    for vault in vaults:
        db.expunge(vault)
    return vaults


def get_vault_by_id(db, vault_id: int) -> Vault | None:
    vault = db.execute(
        select(Vault).where(Vault.vault_id == vault_id)
    ).scalar_one_or_none()
    if vault is not None:
        db.expunge(vault)
    return vault
