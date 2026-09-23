from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem

def display_credentials(window, credentials):
    window.credentialList.clear()

    for credential in credentials:
        item = QListWidgetItem(credential.title)
        item.setData(Qt.UserRole, credential)
        window.credentialList.addItem(item)