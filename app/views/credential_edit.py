from app.utils.ui_loader import load_ui, show_message
from app.utils.password_toggle import wire_password_toggle
from app.services.credential_service import decrypt_credential
from app.services.credential_service import update_credential
from app.services.category_services import get_categories
from app.database.database import SessionLocal

def load_category(window):
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


def credential_edit_window(session, credential):
    window = load_ui("ui/credential_edit.ui")

    if window is None:
        raise RuntimeError(
            "Failed to load UI file: ui/credential_edit.ui"
        )

    window.session = session
    
    load_category(window)
    if credential.category_id is not None:
        index = window.categoryInput.findData(
            credential.category_id
        )
        if index != -1:
            window.categoryInput.setCurrentIndex(index)
    
    window.credential = credential

    username, password, notes = decrypt_credential(
        credential,
        session
    )

    window.titleInput.setText(credential.title)
    window.websiteInput.setText(credential.website or "")
    window.usernameInput.setText(username)
    window.passwordInput.setText(password)
    window.notesInput.setPlainText(notes)

    wire_password_toggle(
        window.passwordInput,
        window.togglePasswordButton
    )

    window.cancelButton.clicked.connect(
        window.close
    )

    window.saveButton.clicked.connect(
        lambda: save_credential_changes(window, credential)
    )

    return window


def save_credential_changes( window, credential):
    
    title = window.titleInput.text().strip()
    website = window.websiteInput.text().strip()
    username = window.usernameInput.text()
    password = window.passwordInput.text()
    notes = window.notesInput.toPlainText().strip()
    category_id = window.categoryInput.currentData()
    
    if not title:
        show_message(window, "Title is required", is_error=True)
        return
    if not username:
        show_message(window, "User Name is required", is_error=True)
        return
    if not password:
        show_message(window, "Password is required", is_error=True)
        return
    
    try:
        with SessionLocal() as db:
            update_credential(
                db, 
                window.session,
                credential,
                title,
                website,
                username,
                password,
                notes,
                category_id
            )
    except Exception as e:
        show_message(
            window,
            f"Faild to Update: {e}",
            is_error= True
        )
        return
        
    show_message(window, "Credentials Updated Successfully")
    window.close()
