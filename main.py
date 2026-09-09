import sys

from PySide6.QtWidgets import QApplication, QLabel


def main():
    app = QApplication(sys.argv)

    window = QLabel("Vaultix")
    window.resize(400, 200)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())