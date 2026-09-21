from app.utils.ui_loader import load_ui, show_message
from app.database.database import SessionLocal
from app.services.category_services import add_category, category_name_exists


def category_window(session):
    window = load_ui("ui/add_category.ui")
    
    if window is None:
        raise RuntimeError("Failed to load UI file: ui/add_category.ui")
    
    window.session = session
    
    window.saveButton.clicked.connect(
        lambda: save_category(window, session)
    )
    
    window.cancelButton.clicked.connect(
        window.close
    )
    return window

    
def save_category(window, session):
    name = window.nameInput.text().strip()
    description = window.descriptionInput.toPlainText()
    
    if not name:
        show_message(
            window,
            "category name is required"
        )
        return
    
    try:
        with SessionLocal() as db:
            if category_name_exists(db, session, name):
                show_message(
                    window,
                    "A category with this name already exists.",
                    is_error= True
                )
                return
            add_category(
                db,
                window.session,
                name,
                description
            )
    except Exception as e:
        show_message(
            window,
            f"Faild to add new category: {e}"
        )
        return
    
    show_message(
        window,
        "New Category added"
    )
    
    window.close()
