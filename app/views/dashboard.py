from app.utils.ui_loader import load_ui

def dashboard_window(session):
    window = load_ui("ui/dashboard.ui")
    
    if window is None:
        raise RuntimeError("Faild to load: 'ui/dashboard.ui'")
    
    window.vaultLabel.setText(session.vault.name)
    
    return window