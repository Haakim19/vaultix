from app.models.models import Credential
from app.security.crypto import encrypt_data

def add_credentials(
    db,
    session,
    title,
    website,
    username,
    password,
    category_id = None
):
    encrypted_username, username_nonce = encrypt_data(
        username,
        session.vault_key
    )
    encrypted_password, password_nonce = encrypt_data(
        password,
        session.vault_key
    )
    credential = Credential(
        vault_id = session.vault.vault_id,
        category_id = category_id,
        title = title.srip(),
        website = website.strip() if website else None,
        encrypted_username = encrypted_username,
        username_nonce = username_nonce,
        encrypted_password = encrypted_password,
        password_nonce = password_nonce
    )
    db.add(credential)
    db.commit()
    db.refresh(credential)
    db.expunge(credential)
    return credential


def get_credentials():
    pass