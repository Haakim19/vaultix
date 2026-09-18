from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem
from app.views.credential_form import credential_window
from app.views.credential_edit import credential_edit_window
from app.utils.ui_loader import load_ui
from app.utils.password_toggle import wire_password_toggle
from app.database.database import SessionLocal
from app.services.credential_service import get_credentials, decrypt_credential

def dashboard_window(session):
    window = load_ui("ui/dashboard.ui")
    
    if window is None:
        raise RuntimeError("Faild to load: 'ui/dashboard.ui'")
    
    window.session = session
    window.vaultNameLabel.setText(f"Vault: {session.vault.name}")
    window.detailStack.setCurrentIndex(0)
    load_credentials(window)
    
    window.credentialList.currentRowChanged.connect(
    lambda row: show_credential_details(window, row)
    )
    
    window.lockVaultButton.clicked.connect(
        lambda: lock_vault(window)
    )
    
    window.newCredentialButton.clicked.connect(
        lambda: open_credential_form(window)
    )
    
    window.editButton.clicked.connect(
        lambda: open_credential_edit(window)
    )
    return window

def lock_vault(window):
    from app.views.login import login_window
    
    window.session = None
    
    window.login = login_window()
    window.login.show()
    
    window.close()


def load_credentials(window):
    with SessionLocal() as db:
        credentials = get_credentials(db, window.session)
    
    window.credentialList.clear()
    
    for credential in credentials:
        item = QListWidgetItem(credential.title)
        item.setData(Qt.UserRole, credential)
        window.credentialList.addItem(item)


def open_credential_form(window):
    window.credential_form = credential_window(window.session)
    window.credential_form.finished.connect(
        lambda: load_credentials(window)
    )
    window.credential_form.show()


def show_credential_details(window, row):
    if row < 0:
        return

    item = window.credentialList.item(row)

    credential = item.data(Qt.UserRole)

    username, password, notes = decrypt_credential(
        credential,
        window.session
    )

    window.titleLabel.setText(credential.title)
    window.websiteLabel.setText(credential.website or "")
    window.usernameField.setText(username)
    window.passwordField.setText(password)
    window.notesField.setPlainText(notes)
    
    window.detailStack.setCurrentIndex(1)


def open_credential_edit(window):
    row = window.credentialList.currentRow()
    if row < 0:
        return
    
    item = window.credentialList.item(row)
    credential = item.data(Qt.UserRole)
    
    window.edit_credential = credential_edit_window(
        window.session,
        credential
        )
    def refresh_after_edit():
        load_credentials(window)
        window.credentialList.setCurrentRow(row)
        
    window.edit_credential.finished.connect(
        refresh_after_edit
    )
    window.edit_credential.show()