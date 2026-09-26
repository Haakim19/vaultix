from app.utils.ui_loader import load_ui, show_message
from app.utils.dashboard_helper import load_categories
from app.utils.password_toggle import wire_password_toggle
from app.database.database import SessionLocal
from app.services.credential_service import add_credentials

def credential_window(session):
    window = load_ui("ui/credential_dialog.ui")

    if window is None:
        raise RuntimeError("Failed to load UI file: ui/credential_form.ui")

    window.session = session
    
    load_categories(window)
    
    wire_password_toggle(
        window.passwordInput,
        window.togglePasswordButton
    )
    window.saveButton.clicked.connect(
    lambda: save_credential(window)
)

    window.cancelButton.clicked.connect(
        window.close
    )
    return window


def save_credential(window):
    title = window.titleInput.text().strip()
    website = window.websiteInput.text().strip()
    username = window.usernameInput.text()
    password = window.passwordInput.text()
    notes = window.notesInput.toPlainText().strip()
    category_id = window.categoryInput.currentData()


    if not title:
        show_message(
            window,
            "title is required",
            is_error=True
        )
        return

    if not username:
        show_message(
            window,
            "User Name is required",
            is_error=True
        )
        return

    if not password:
        show_message(
            window,
            "Password is required",
            is_error=True
        )
        return


    try:
        with SessionLocal() as db:
            add_credentials(
                db,
                window.session,
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
            f"Faild to save credentials: {e}",
            is_error=True
        )
    
    show_message(
        window,
        "Credential saved succesfully"
    )
    
    window.close()