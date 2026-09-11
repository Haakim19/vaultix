from datetime import datetime

from sqlalchemy.orm import DeclarativeBase,  Mapped, mapped_column
from sqlalchemy import create_engine, String, LargeBinary, DateTime

class Base(DeclarativeBase):
    pass
# Table declaration
class Vault(Base):
    __tablename__ = 'vault'
    vault_id : Mapped[int] = mapped_column(primary_key= True)
    name : Mapped[str] = mapped_column(String(50))
    salt : Mapped[bytes] = mapped_column(LargeBinary)
    encrypted_verification : Mapped[bytes] = mapped_column(LargeBinary)
    verification_nonce : Mapped[bytes] = mapped_column(LargeBinary)
    created_at : Mapped[datetime] = mapped_column(DateTime)
    updated_at : Mapped[datetime] = mapped_column(DateTime)
    

    

