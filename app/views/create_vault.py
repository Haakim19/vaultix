from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


def load_ui(filename):
    loader = QUiLoader()
    ui_file = QFile(filename)

    ui_file.open(QFile.ReadOnly)
    window = loader.load(ui_file)
    ui_file.close()

    return window


def create_vault():

    window = load_ui("ui/create_vault.ui")

    window.createVaultButton.clicked.connect(
        lambda: get_data(window)
    )

    return window


def get_data(window):

    vault_name = window.vaultNameInput.text()
    password = window.passwordInput.text()
    confirm_password = window.confirmPasswordInput.text()

    print(vault_name)
    print(password)
    print(confirm_password)