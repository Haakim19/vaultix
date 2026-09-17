from PySide6.QtWidgets import QLineEdit, QToolButton
from PySide6.QtCore import Qt


ICON_SHOW = "👁"
ICON_HIDE = "🚫"


def wire_password_toggle(line_edit: QLineEdit, button: QToolButton) -> None:
    button.setText(ICON_SHOW)
    button.setCursor(Qt.PointingHandCursor)
    button.setToolTip("Show password")
    button.setFixedWidth(38)

    def toggle():
        if line_edit.echoMode() == QLineEdit.Password:
            line_edit.setEchoMode(QLineEdit.Normal)
            button.setText(ICON_HIDE)
            button.setToolTip("Hide password")
        else:
            line_edit.setEchoMode(QLineEdit.Password)
            button.setText(ICON_SHOW)
            button.setToolTip("Show password")

    button.clicked.connect(toggle)