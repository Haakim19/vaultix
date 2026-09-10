import sys

from PySide6.QtWidgets import QApplication

from app.views.create_vault import create_vault


def main():
    app = QApplication(sys.argv)

    window = create_vault()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()