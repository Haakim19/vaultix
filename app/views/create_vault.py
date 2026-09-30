from app.database.database import SessionLocal
from app.services.vault_service import create_vault, vault_name_exists
from app.utils.ui_loader import load_ui, show_message
from app.utils.password_toggle import wire_password_toggle
from app.session.session import VaultSession
from app.views.dashboard import dashboard_window


def main_vault_creation(show_login_link = False):

    window = load_ui("ui/create_vault.ui")

    if window is None:
        raise RuntimeError("Failed to load UI file: ui/create_vault.ui")
    
    window.switchToLoginLabel.setVisible(show_login_link)
    
    if show_login_link:
        window.switchToLoginLabel.linkActivated.connect(
            lambda link: open_login(window)
        )
    
    wire_password_toggle(window.passwordInput, window.togglePasswordButton)
    wire_password_toggle(window.confirmPasswordInput, window.toggleConfirmPasswordButton)
    
    window.createVaultButton.clicked.connect(
        lambda: validate_data(window)
    )

    return window


def validate_data(window):

    vault_name = window.vaultNameInput.text().strip()
    password = window.passwordInput.text()
    confirm_password = window.confirmPasswordInput.text()

    error =(
        "Vault name is required." if not vault_name else
        "Password is required." if not password else
        "Password must be at least 8 characters." if len(password) < 8 else
        "Confirm password is empty." if not confirm_password else
        "Passwords do not match." if confirm_password != password else 
        None
    )
    if error:
        show_message(window, error, is_error = True)
        return
    # Save to Database 
    try:
        with SessionLocal() as db:
            
            if vault_name_exists(db, vault_name):
                show_message(
                    window,
                    "A vault with this name already exists.",
                    is_error=True
                )
                return
            created_vault, vault_key = create_vault(
                db, 
                vault_name, 
                password
                )
            
    except Exception as e:
        # Handle database error
        show_message(window, f"Failed to create vault: {e}", is_error= True)
        return
    
    session = VaultSession(created_vault, vault_key)
        
    # open dashboard on successfull vault creation
    window.dashboard = dashboard_window(session)
    window.dashboard.show()
    clear_fields(window)
    window.close()

def clear_fields(window):
    window.vaultNameInput.clear()
    window.passwordInput.clear()
    window.confirmPasswordInput.clear()


def open_login(window):
    from app.views.login import login_window
    
    window.login = login_window()
    window.login.show()
    window.hide()