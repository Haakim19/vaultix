import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from app.database.database import Base, engine, SessionLocal
from app.models import models

Base.metadata.create_all(engine)

from app.services.vault_service import any_vault_exist
from app.views.create_vault import main_vault_creation
from app.views.login import login_window
from app.utils.ui_loader import resource_path


def main():
    app = QApplication(sys.argv)

    app.setWindowIcon(
        QIcon(str(resource_path("assets/icons/vaultix.png")))
    )
    with SessionLocal() as db:
        has_vault = any_vault_exist(db)
    
    if has_vault:
        window = login_window()
    else:
        window = main_vault_creation()
    # window = main_vault_creation()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    sys.exit(main())