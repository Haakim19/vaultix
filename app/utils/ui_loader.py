
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QMessageBox

def load_ui(filename):
    loader = QUiLoader()
    ui_file = QFile(filename)

    if ui_file.open(QFile.ReadOnly):
        window = loader.load(ui_file)
        ui_file.close()
        return window
    return None

def show_message(window, message, is_error = False):
    if is_error:
        QMessageBox.warning(window, "Vaultix", message)
    else:
        QMessageBox.information(window, "Vaultix", message)

