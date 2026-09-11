from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


def load_ui(filename):
    loader = QUiLoader()
    ui_file = QFile(filename)

    if ui_file.open(QFile.ReadOnly):
        window = loader.load(ui_file)
        ui_file.close()
        return window
    return None


def create_vault():

    window = load_ui("ui/create_vault.ui")

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
        "Password lenght is not 8 charecters" if len(password) < 8 else
        "Confirm password is empty" if not confirm_password else
        "Password is not same" if confirm_password != password else None
    )
    if error:
        show_message(window, error)
        return
        
    show_message(window, "Validation successful")
    clear_fields(window)

def show_message(window, message):
    QMessageBox.information(
        window,
        "Vaultix",
        message
    )

def clear_fields(window):
    window.vaultNameInput.clear()
    window.passwordInput.clear()
    window.confirmPasswordInput.clear()