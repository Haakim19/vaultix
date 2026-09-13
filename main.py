import sys

from PySide6.QtWidgets import QApplication

from app.views.create_vault import main_vault_creation
from app.views.login import login_window


def main():
    app = QApplication(sys.argv)

    window = login_window()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()