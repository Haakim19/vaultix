import sys

from PySide6.QtWidgets import QApplication

from app.views.create_vault import main_vault_creation


def main():
    app = QApplication(sys.argv)

    window = main_vault_creation()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()