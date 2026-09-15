from app.utils.ui_loader import load_ui

def dashboard_window(session):
    window = load_ui("ui/dashboard.ui")
    
    if window is None:
        raise RuntimeError("Faild to load: 'ui/dashboard.ui'")
    
    window.session = session
    window.vaultLabel.setText(session.vault.name)
    
    window.lockVault.clicked.connect(
        lambda: lock_vault(window)
    )
    return window

def lock_vault(window):
    from app.views.login import login_window
    
    window.session = None
    
    window.login = login_window()
    window.login.show()
    
    window.close()