from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem
from app.database.database import SessionLocal
from app.services.category_services import get_categories
def display_credentials(window, credentials):
    window.credentialList.clear()

    for credential in credentials:
        item = QListWidgetItem(credential.title)
        item.setData(Qt.UserRole, credential)
        window.credentialList.addItem(item)



def load_categories(window):
    with SessionLocal() as db:
        categories = get_categories(
            db,
            window.session
        )
    window.categoryInput.clear()
    
    window.categoryInput.addItem(
        "No category",
        None
    )
    
    for category in categories:
        window.categoryInput.addItem(
            category.name,
            category.category_id
        )
