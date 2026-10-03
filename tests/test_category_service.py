import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.services.vault_service import create_vault
from app.services.category_services import (
    add_category,
    get_categories,
    category_name_exists,
    update_category,
    delete_category)
from app.session.session import VaultSession


@pytest.fixture
def testing_session():
    test_engine = create_engine("sqlite://")
    Base.metadata.create_all(test_engine)
    TestSession = sessionmaker(bind=test_engine)

    yield TestSession

    test_engine.dispose()

def test_add_category(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(
        db, "Personal", "master123"
    )
    session = VaultSession(vault, vault_key)

    category = add_category(
        db, session,
        "Development",
        "Programming accounts"
    )

    assert category.category_id is not None
    assert category.vault_id == vault.vault_id
    assert category.name == "Development"
    assert category.description == "Programming accounts"

    db.close()


def test_add_category_trims_whitespace(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    category = add_category(
        db, session,
        "  Development  ",
        "  Programming accounts  "
    )

    assert category.name == "Development"
    assert category.description == "Programming accounts"

    db.close()


def test_add_category_with_empty_name(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    with pytest.raises(ValueError, match="Category name cannot be empty"):
        add_category(db, session, "   ")

    db.close()


def test_get_categorys(testing_session):
    db = testing_session()
    
    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    add_category(db, session, "Social Media")
    add_category(db, session, "Development")
    add_category(db, session, "Finance")

    categories = get_categories(db, session)
    
    assert len(categories) == 3
    assert [category.name for category in categories] == [
        "Development",
        "Finance",
        "Social Media"
    ]
    
    db.close()
    
def test_get_categories_vault_isolation(testing_session):
    db = testing_session()

    personal_vault, personal_key = create_vault(
        db, "Personal", "personal123"
    )
    work_vault, work_key = create_vault(
        db, "Work", "work123"
    )

    personal_session = VaultSession(personal_vault, personal_key)
    work_session = VaultSession(work_vault, work_key)

    add_category(db, personal_session, "Social Media")
    add_category(db, personal_session, "Finance")
    add_category(db, work_session, "Development")
    
    personal_category = get_categories(db, personal_session)
    work_category = get_categories(db, work_session)
    
    assert [category.name for category in personal_category] == [
        "Finance",
        "Social Media"
    ]
    assert [category.name for category in work_category] == [
        "Development"
    ]
    
    db.close()


def test_category_name_exists(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    add_category(db, session, "Development")

    assert category_name_exists(db, session, "Development") is True
    assert category_name_exists(db, session, "development") is True
    assert category_name_exists(db, session, "  Development  ") is True
    assert category_name_exists(db, session, "Finance") is False

    db.close()

def test_category_name_exists_vault_isolation(testing_session):
    db = testing_session()

    personal_vault, personal_key = create_vault(
        db, "Personal", "personal123"
    )
    work_vault, work_key = create_vault(
        db, "Work", "work123"
    )

    personal_session = VaultSession(personal_vault, personal_key)
    work_session = VaultSession(work_vault, work_key)

    add_category(db, personal_session, "Development")

    assert category_name_exists(
        db, personal_session, "Development"
    ) is True

    assert category_name_exists(
        db, work_session, "Development"
    ) is False

    db.close()

def test_update_category(testing_session):
    db = testing_session()
    
    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    category = add_category(
        db, session, "Development", "Old description"
    )
    
    updated = update_category(
        db, session, category,
        name = "Programming",
        description= "New description"    
    )
    
    assert updated.category_id == category.category_id
    assert updated.name == "Programming"
    assert updated.description == "New description"
    
    db.close()


def test_update_category_trims_whitespace(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    category = add_category(db, session, "Development")

    updated = update_category(
        db, session, category,
        name="  Programming  ",
        description="  Coding accounts  "
    )

    assert updated.name == "Programming"
    assert updated.description == "Coding accounts"

    db.close()


def test_update_category_with_empty_name(testing_session):
    db = testing_session()

    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    category = add_category(db, session, "Development")

    with pytest.raises(
        ValueError,
        match="Category name cannot be empty"
    ):
        update_category(
            db, session, category,
            name="   ",
            description="Some description"
        )

    db.close()

def test_update_category_from_another_vault(testing_session):
    db = testing_session()

    personal_vault, personal_key = create_vault(
        db, "Personal", "personal123"
    )
    work_vault, work_key = create_vault(
        db, "Work", "work123"
    )

    personal_session = VaultSession(personal_vault, personal_key)
    work_session = VaultSession(work_vault, work_key)

    category = add_category(
        db, personal_session, "Development"
    )

    with pytest.raises(
        ValueError,
        match="Category does not belong to this vault"
    ):
        update_category(
            db, work_session, category,
            name="Changed",
            description="Changed description"
        )

    categories = get_categories(db, personal_session)

    assert len(categories) == 1
    assert categories[0].name == "Development"

    db.close()

def test_delete_category(testing_session):
    db = testing_session()
    
    vault, vault_key = create_vault(db, "Personal", "master123")
    session = VaultSession(vault, vault_key)

    category = add_category(db, session, "Development")
    
    delete_category(db, session, category)
    
    categories = get_categories(db, session)
    
    assert len(categories) == 0
    
    db.close()