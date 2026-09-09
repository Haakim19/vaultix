import sys

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


def load_ui(filename):
    loader = QUiLoader()
    ui_file = QFile(filename)

    ui_file.open(QFile.ReadOnly)
    window = loader.load(ui_file)
    ui_file.close()

    return window


def main():
    app = QApplication(sys.argv)

    window = load_ui("ui/login.ui")
    
    window.unlockButton.clicked.connect(
        lambda : show_message(window)
    )
    window.show()

    sys.exit(app.exec())

def show_message(window):
    QMessageBox.information(
        window,
        "Vaultix",
        "Unlock Button Clicked"
    )
if __name__ == "__main__":
    main()