from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem
from app.database.database import SessionLocal
from app.services.category_services import get_categories
from app.services.credential_service import(
    get_credentials,
    get_credentials_by_category,
    search_credentials
)

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


def display_password_strength(window, label, score):
    window._strength_score = score
    # Track width = strengthBarBg's current width. Fill width = score/6 of that.
    track = window.strengthBarBg
    fill = window.strengthBarFill

    # Make sure sizes are computed after the widget has been laid out
    track_width = track.width() or 200
    fill_width = max(0, int(track_width * score / 6))
    fill.setFixedWidth(fill_width)

    colour = {
        "Weak":   "#ef4444",
        "Medium": "#f59e0b",
        "Strong": "#22c55e",
    }[label]
    fill.setStyleSheet(
        f"background-color: {colour}; border-radius: 3px;"
    )
    window.strengthLabel.setText(label)
    window.strengthLabel.setStyleSheet(
        f"color: {colour}; font-weight: 700; font-size: 14px;"
    )

def refresh_credential_list(window):
    search_text = window.searchInput.text().strip()
    
    category_item = window.categoryList.currentItem()
    category = category_item.data(Qt.UserRole) if category_item else None
    category_id = category.category_id if category else None
    
    if search_text:
        with SessionLocal() as db:
            credentials = search_credentials(
                db,
                window.session,
                search_text,
                category_id
            )
    elif category_id is not None:
        with SessionLocal() as db:
            credentials = get_credentials_by_category(
                db,
                window.session,
                category_id
            )
    else:
        with SessionLocal() as db:
            credentials = get_credentials(
                db,
                window.session
            )
    display_credentials(window, credentials)