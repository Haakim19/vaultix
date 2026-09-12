from app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import LargeBinary, DateTime, String, ForeignKey

#? vault table
class Vault(Base):
    __tablename__ = 'vault'
    
    vault_id : Mapped[int] = mapped_column(primary_key= True)
    name : Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    salt : Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    encrypted_verification : Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    verification_nonce : Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        nullable=False)
    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        onupdate= lambda: datetime.now(timezone.utc),
        nullable=False)

#! Relationships
    categories: Mapped[list["Category"]] = relationship (
        back_populates= "vault",
        cascade= "all, delete-orphan"
    )
    credentials: Mapped[list["Credential"]] = relationship(
        back_populates="vault",
        cascade= "all, delete-orphan"
    )

#? Category table
class Category(Base):
    __tablename__ = 'category'
    
    category_id : Mapped[int] = mapped_column(primary_key=True)
    vault_id : Mapped[int] = mapped_column(
        ForeignKey("vault.vault_id", ondelete="CASCADE"),
        nullable= False
    )
    name : Mapped[str] = mapped_column(String(50), nullable=False)
    description : Mapped[str | None] = mapped_column(String(255), nullable=True)

#! Relationship
    vault: Mapped["Vault"] = relationship(back_populates="categories")
    credentials: Mapped[list["Credential"]] = relationship(back_populates="category")


#? Credential table
class Credential(Base):
    __tablename__ = "credential"

    credential_id: Mapped[int] = mapped_column(primary_key=True)
    vault_id: Mapped[int] = mapped_column(
        ForeignKey("vault.vault_id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("category.category_id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    encrypted_username: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    username_nonce: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    encrypted_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    password_nonce: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

#! Relationship
    vault: Mapped["Vault"] = relationship(back_populates="credentials")
    category: Mapped["Category | None"] = relationship(back_populates="credentials")