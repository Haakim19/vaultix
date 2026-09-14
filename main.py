import sys

from PySide6.QtWidgets import QApplication

from app.database.database import SessionLocal
from app.services.vault_service import any_vault_exist

from app.views.create_vault import main_vault_creation
from app.views.login import login_window


def main():
    app = QApplication(sys.argv)

    with SessionLocal() as db:
        has_vault = any_vault_exist(db)
    
    if has_vault:
        window = login_window()
    else:
        window = main_vault_creation()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    sys.exit(main())