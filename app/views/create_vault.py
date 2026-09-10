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

    
    if vault_name.strip() == "":
        show_message(window, "Vault name is empty")
        return
    elif password == "":
        show_message(window, "Password is empty")
        return
    elif len(password) < 8:
        show_message(window, "Password lenght is not 8 charecters")
        return
    elif confirm_password == "":
        show_message(window, "Confim password is empty")
        return
        
    elif password != confirm_password:
        show_message(window, "Password is not same")
        return
    show_message(window, "All ok, vault creaded")
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
    window.confirmPassword1kInput.clear()