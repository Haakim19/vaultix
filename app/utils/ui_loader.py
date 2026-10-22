from pathlib import Path
import sys
from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

def resource_path(relative_path: str) -> Path:
    """Find a bundled resource or a project resource."""
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent.parent

    return base_path / relative_path


THEME_PATH = resource_path("ui/themes.qss")


def _theme_text() -> str:
    return THEME_PATH.read_text() if THEME_PATH.exists() else ""


def load_ui(filename):
    loader = QUiLoader()

    ui_path = resource_path(filename)
    ui_file = QFile(str(ui_path))

    if not ui_file.open(QFile.OpenModeFlag.ReadOnly):
        raise RuntimeError(f"Failed to load UI file: {ui_path}")

    try:
        window = loader.load(ui_file)
    finally:
        ui_file.close()

    if window is None:
        raise RuntimeError(f"Failed to create window from UI file: {ui_path}")

    window.setStyleSheet(_theme_text())
    return window


def show_message(window, message, is_error=False):
    box = QMessageBox(window)
    box.setWindowTitle("Vaultix")
    box.setText(message)
    box.setIcon(QMessageBox.Warning if is_error else QMessageBox.Information)
    box.setStyleSheet(_theme_text())
    box.exec()