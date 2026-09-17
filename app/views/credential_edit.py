from app.utils.ui_loader import load_ui
from app.utils.password_toggle import wire_password_toggle
from app.services.credential_service import decrypt_credential

def credential_edit_window(session, credential):
    window = load_ui("ui/credential_edit.ui")

    if window is None:
        raise RuntimeError(
            "Failed to load UI file: ui/credential_edit.ui"
        )

    window.session = session
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

    return window