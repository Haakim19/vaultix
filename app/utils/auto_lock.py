from PySide6.QtCore import QTimer, QObject, QEvent

class ActivityFilter(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
    
    def eventFilter(self, obj, event):
        if event.type() in (
            QEvent.MouseButtonPress,
            QEvent.KeyPress,
        ):
            reset_auto_lock_timer(self.window)
        
        return False
def remove_activity_filter(window):
    from PySide6.QtWidgets import QApplication
    
    app = QApplication.instance()
    
    if app is not None and hasattr(window, "activity_filter"):
        app.removeEventFilter(window.activity_filter)

def create_auto_lock_timer(window, timeout = 5 * 60 * 1000):
    timer = QTimer(window)
    timer.setInterval(timeout)
    
    window.auto_lock_timer = timer
    
    return timer

def reset_auto_lock_timer(window):
    if hasattr(window, "activity_filter"):
        window.auto_lock_timer.start()
        
