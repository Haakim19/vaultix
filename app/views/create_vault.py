from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from app.services.vault_service import create_vault

def load_ui(filename):
    loader = QUiLoader()
    ui_file = QFile(filename)

    if ui_file.open(QFile.ReadOnly):
        window = loader.load(ui_file)
        ui_file.close()
        return window
    return None


def main():

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
        "Password must be at least 8 charecters" if len(password) < 8 else
        "Confirm password is empty" if not confirm_password else
        "Password is not same" if confirm_password != password else 
        None
    )
    if error:
        show_message(window, error, is_error = True)
        return
    # Save to Database 
    try:
        created_vault = create_vault(vault_name, password)
        # show success message 
        show_message(window, f"Vault '{created_vault.name}' created successfully!")
        clear_fields(window)
    except Exception as e:
        # Handle database error gracfully
        show_message(window, f"Faild to create vault {e}", is_error= True)

def show_message(window, message, is_error = False):
    if is_error:
        QMessageBox.warning(window, "Vaultix", message)
    else:
        QMessageBox.information(window, "Vaultix", message)

def clear_fields(window):
    window.vaultNameInput.clear()
    window.passwordInput.clear()
    window.confirmPasswordInput.clear()