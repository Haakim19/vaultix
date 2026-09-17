from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem
from app.utils.ui_loader import load_ui
from app.database.database import SessionLocal
from app.services.credential_service import get_credentials, decrypt_credential
from app.views.credential_form import credential_window

def dashboard_window(session):
    window = load_ui("ui/dashboard.ui")
    
    if window is None:
        raise RuntimeError("Faild to load: 'ui/dashboard.ui'")
    
    window.session = session
    window.vaultNameLabel.setText(f"Vault: {session.vault.name}")
    
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
    window.credential_form.show()


def show_credential_details(window, row):
    if row < 0:
        return

    item = window.credentialList.item(row)

    credential = item.data(Qt.UserRole)

    username, password = decrypt_credential(
        credential,
        window.session
    )

    window.titleLabel.setText(credential.title)
    window.websiteLabel.setText(credential.website or "")
    window.usernameField.setText(username)
    window.passwordField.setText(password)
    
    window.detailStack.setCurrentIndex(1)