from PySide6.QtWidgets import QToolButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from app.utils.ui_loader import resource_path

ICON_COPY = resource_path("ui/icons/copy.svg")


def setup_copy_icon(button: QToolButton) -> None:
    button.setIcon(QIcon(str(ICON_COPY)))
    button.setCursor(Qt.PointingHandCursor)
    button.setToolTip("Copy to clipboard")
    button.setFixedWidth(38)