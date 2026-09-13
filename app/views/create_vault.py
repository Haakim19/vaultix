from app.database.database import SessionLocal
from PySide6.QtWidgets import QMessageBox
from app.services.vault_service import create_vault
from app.utils.ui_loader import load_ui, show_message

def main_vault_creation():

    window = load_ui("ui/create_vault.ui")

    if window is None:
        raise RuntimeError("Failed to load UI file: ui/create_vault.ui")
    
    window.createVaultButton.clicked.connect(
        lambda: validate_data(window)
    )

    return window


def validate_data(window):

    vault_name = window.vaultNameInput.text()
    password = window.passwordInput.text()
    confirm_password = window.confirmPasswordInput.text()

    error =(
        "Vault name is empty" if not vault_name.strip() else
        "Password is empty" if not password else
        "Password must be at least 8 characters" if len(password) < 8 else
        "Confirm password is empty" if not confirm_password else
        "Password do not match" if confirm_password != password else 
        None
    )
    if error:
        show_message(window, error, is_error = True)
        return
    # Save to Database 
    try:
        with SessionLocal() as db:
            created_vault = create_vault(vault_name, password, db)
        # show success message 
        show_message(window, f"Vault '{created_vault.name}' created successfully!")
        clear_fields(window)
    except Exception as e:
        # Handle database error gracefully
        show_message(window, f"Failed to create vault {e}", is_error= True)

def clear_fields(window):
    window.vaultNameInput.clear()
    window.passwordInput.clear()
    window.confirmPasswordInput.clear()