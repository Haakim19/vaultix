from app.models.models import Credential
from app.security.crypto import encrypt_data, decrypt_data
from sqlalchemy import select


def add_credentials(
    db,
    session,
    title,
    website,
    username,
    password,
    notes = "",
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
    if notes:
        encrypted_notes, notes_nonce = encrypt_data(
            notes,
            session.vault_key
        )
    else:
        encrypted_notes = None
        notes_nonce = None
    
    credential = Credential(
        vault_id = session.vault.vault_id,
        category_id = category_id,
        title = title.strip(),
        website = website.strip() if website else None,
        encrypted_username = encrypted_username,
        username_nonce = username_nonce,
        encrypted_password = encrypted_password,
        password_nonce = password_nonce,
        encrypted_notes=encrypted_notes,
        notes_nonce=notes_nonce,
    )
    db.add(credential)
    db.commit()
    db.refresh(credential)
    db.expunge(credential)
    return credential



def get_credentials(db, session):
    credentials = db.execute(
        select(Credential).where(
            Credential.vault_id == session.vault.vault_id)
    ).scalars().all()
    for credential in credentials:
        db.expunge(credential)
    return credentials


def decrypt_credential(credential: Credential, session):
    username = decrypt_data(
        credential.encrypted_username,
        credential.username_nonce,
        session.vault_key)
    
    password = decrypt_data(
        credential.encrypted_password,
        credential.password_nonce,
        session.vault_key
    )
    
    if credential.encrypted_notes:
        notes = decrypt_data(
            credential.encrypted_notes,
            credential.notes_nonce,
            session.vault_key
        )
    else:
        notes = ""
    
    return username, password, notes

def update_credential(
    db, 
    session,
    credential: Credential, 
    title,
    website,
    username,
    password,
    notes,
    category_id = None):
    
    if credential.vault_id != session.vault.vault_id:
        raise ValueError("Credential does not belong to this vault")
    
    db.add(credential)
    
    orginal_username, orginal_password, orginal_notes = decrypt_credential(
        credential,
        session
    )
        
    
    credential.category_id = category_id
    credential.title = title.strip()
    credential.website = website.strip() if website else None

    # Check if the old username/ password/ notes and new are same if not it updates with old ones
    if orginal_username != username:
        new_encrypted_username, new_username_nonce = encrypt_data(
            username,
            session.vault_key
        )
        credential.encrypted_username = new_encrypted_username
        credential.username_nonce = new_username_nonce
    
    if orginal_password != password:
        new_encrypted_password, new_password_nonce = encrypt_data(
            password,
            session.vault_key
        )
        credential.encrypted_password = new_encrypted_password
        credential.password_nonce = new_password_nonce

    if orginal_notes != notes:
        # check whether notes have any vaule and encrypt it
        if notes:    
            new_encrypted_notes, new_notes_nonce = encrypt_data(
                notes,
                session.vault_key
            )
        else:
            new_encrypted_notes = None
            new_notes_nonce = None
        
        credential.encrypted_notes = new_encrypted_notes
        credential.notes_nonce = new_notes_nonce
    
    db.commit()
    db.refresh(credential)
    db.expunge(credential)
    
    return credential

def delete_credential(db, session, credential):
    if credential.vault_id != session.vault.vault_id:
        raise ValueError("Credential does not belong to this vault")
    
    db.add(credential)
    db.delete(credential)
    db.commit()