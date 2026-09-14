from app.database.database import SessionLocal
from app.utils.ui_loader import load_ui, show_message
from app.services.vault_service import unlock_vault, get_vaults, get_vault_by_id
from app.session.session import VaultSession

def login_window():
    window = load_ui("ui/login.ui")
    
    if window is None:
        raise RuntimeError("Failed to load UI File: ui/login.ui")
    
    with SessionLocal() as db:
        vaults = get_vaults(db)
    
    for vault in vaults:
        window.vaultName.addItem(vault.name, vault.vault_id)
    
    window.unlockVault.clicked.connect(
        lambda: validate_login_data(window)
    )
    return window
    
def validate_login_data(window):
    vault_id = window.vaultName.currentData()
    master_password = window.masterPassword.text()
    
    if not master_password:
        show_message(
            window,
            "Master password is required.",
            is_error=True
        )
        return
    
    try:
        with SessionLocal() as db:
            found_vault = get_vault_by_id(vault_id, db)

        vault_key = unlock_vault(found_vault, master_password)

        if vault_key is not None:
            session = VaultSession(found_vault, vault_key)
            
            print("Vault: ",session.vault.name)
            print("Vault_key: ", session.vault_key)
        else:
            show_message(window,"❌ Incorrect password: vault rejected!", is_error=True)
        
        window.masterPassword.clear()
    except Exception as e:
        show_message(window, f"Login error: {e}", is_error = True)
        