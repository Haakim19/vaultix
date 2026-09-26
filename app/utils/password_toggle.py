from pathlib import Path

from PySide6.QtWidgets import  QLineEdit, QToolButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

ICON_SHOW = Path("ui/icons/Show.svg")
ICON_HIDE = Path("ui/icons/Hide.svg")


def wire_password_toggle(line_edit: QLineEdit, button: QToolButton) -> None:
    button.setIcon(QIcon(str(ICON_SHOW)))
    button.setCursor(Qt.PointingHandCursor)
    button.setToolTip("Show password")
    button.setFixedWidth(38)

    def toggle():
        if line_edit.echoMode() == QLineEdit.Password:
            line_edit.setEchoMode(QLineEdit.Normal)
            button.setIcon(QIcon(str(ICON_HIDE)))
            button.setToolTip("Hide password")
        else:
            line_edit.setEchoMode(QLineEdit.Password)
            button.setIcon(QIcon(str(ICON_SHOW)))
            button.setToolTip("Show password")

    button.clicked.connect(toggle)