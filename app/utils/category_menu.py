from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu, QMessageBox
from app.database.database import SessionLocal
from app.services.category_services import delete_category
from app.views.add_category import category_window


def setup_category_context_menu(window):
    window.categoryList.setContextMenuPolicy(
        Qt.CustomContextMenu
    )

    window.categoryList.customContextMenuRequested.connect(
        lambda position: show_category_menu(window, position)
    )


def show_category_menu(window, position):
    item = window.categoryList.itemAt(position)

    if item is None:
        return

    category = item.data(Qt.UserRole)

    if category is None:
        return

    menu = QMenu(window)

    edit_action = menu.addAction("Edit Category")
    delete_action = menu.addAction("Delete Category")

    action = menu.exec(
        window.categoryList.mapToGlobal(position)
    )

    if action == edit_action:
        edit_category(window, category)

    elif action == delete_action:
        delete_selected_category(window, category)

def edit_category(window, category):
    window.edit_category_window = category_window(
        window.session,
        category
    )

    window.edit_category_window.finished.connect(
        lambda: refresh_after_category_change(window)
    )

    window.edit_category_window.show()

def delete_selected_category(window, category):
    reply = QMessageBox.question(
        window,
        "Delete Category",
        f"Are you sure you want to delete category: {category.name}?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply != QMessageBox.Yes:
        return
    
    with SessionLocal() as db:
        delete_category(
            db,
            window.session,
            category
        )
    refresh_after_category_change(window)

def refresh_after_category_change(window):
    from app.views.dashboard import load_category

    load_category(window)