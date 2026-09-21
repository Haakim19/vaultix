from sqlalchemy import select
from app.models.models import Category

def add_category(db, session, name, description = ""):
    name = name.strip()
    
    if not name:
        raise ValueError("Category name cannot be empty")
    
    category = Category(
        vault_id = session.vault.vault_id,
        name = name,
        description = description.strip() or None
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    db.expunge(category)
    
    return category

def get_categories(db, session):
    categories = db.execute(
        select(Category).where(
            Category.vault_id == session.vault.vault_id
        ).order_by(Category.name)
    ).scalars().all()
    
    for category in categories:
        db.expunge(category)
    return categories

def delete_category(db, session, category: Category):
    if category.vault_id != session.vault.vault_id:
        raise ValueError("Category does not belong to ths vault")
    
    db.add(category)
    db.delete(category)
    db.commit()


def category_name_exists(db, session, category_name):
    normalized_name = category_name.strip().lower()
    
    categories = db.execute(
        select(Category).where(
            Category.vault_id == session.vault.vault_id
        )
    ).scalars().all()
    
    return any(
        category.name.strip().lower() == normalized_name
        for category in categories
    )