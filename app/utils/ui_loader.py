import pathlib
from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

THEME_PATH = pathlib.Path(__file__).resolve().parent.parent.parent / "ui" / "theme.qss"


def _theme_text() -> str:
    return THEME_PATH.read_text() if THEME_PATH.exists() else ""


def load_ui(filename):
    loader = QUiLoader()
    ui_file = QFile(str(filename))
    if not ui_file.open(QFile.ReadOnly):
        return None
    window = loader.load(ui_file)
    ui_file.close()
    window.setStyleSheet(_theme_text())
    return window


def show_message(window, message, is_error=False):
    box = QMessageBox(window)
    box.setWindowTitle("Vaultix")
    box.setText(message)
    box.setIcon(QMessageBox.Warning if is_error else QMessageBox.Information)
    box.setStyleSheet(_theme_text())
    box.exec()