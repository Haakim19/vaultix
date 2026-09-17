from app.database.database import SessionLocal
from app.utils.ui_loader import load_ui, show_message
from app.utils.password_toggle import wire_password_toggle
from app.services.vault_service import unlock_vault, get_vaults, get_vault_by_id
from app.session.session import VaultSession
from app.views.dashboard import dashboard_window


def login_window():
    window = load_ui("ui/login.ui")
    if window is None:
        raise RuntimeError("Failed to load UI file: ui/login.ui")

    wire_password_toggle(window.masterPassword, window.toggleMasterPasswordButton)
    
    combo = window.vaultName
    
    combo.clear()
    
    combo.addItem("-Select a vault-", None)
    
    with SessionLocal() as db:
        vaults = get_vaults(db)

    for vault in vaults:
        combo.addItem(vault.name, vault.vault_id)
        
    combo.setCurrentIndex(0)
    
    window.unlockVault.clicked.connect(
        lambda: validate_login_data(window)
    )
    return window


def validate_login_data(window):
    vault_id = window.vaultName.currentData()
    master_password = window.masterPassword.text()

    if vault_id is None:
        show_message(window, "Please select a vault.", is_error=True)
        return
    
    if not master_password:
        show_message(window, "Master password is required.", is_error=True)
        return

    try:
        with SessionLocal() as db:
            found_vault = get_vault_by_id(db, vault_id)
    except Exception as e:
        show_message(window, f"Login error: {e}", is_error=True)
        return

    if found_vault is None:
        show_message(window, "Vault not found.", is_error=True)
        return

    vault_key = unlock_vault(found_vault, master_password)
    if vault_key is None:
        show_message(window, "Incorrect master password.", is_error=True)
        window.masterPassword.clear()
        return

    session = VaultSession(found_vault, vault_key)
    window.dashboard = dashboard_window(session)
    window.dashboard.show()
    window.close()