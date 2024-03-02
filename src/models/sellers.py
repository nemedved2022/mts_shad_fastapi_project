from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Seller(BaseModel):
    __tablename__ = "sellers_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[int] = mapped_column(Text(), nullable=False)
    books: Mapped[list["Book"]] = relationship(
        back_populates="seller",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=True,
    )
