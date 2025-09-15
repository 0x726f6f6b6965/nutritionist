from .base import Base
from sqlalchemy import Integer, TIMESTAMP, SmallInteger, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text


# Define a Python class (model) mapping to a PostgreSQL table
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    line_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    height: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    weight: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text('now()'))
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text('now()'))

    def __repr__(self):
        return f"<User(id={self.id!r}, line_id='{self.line_id!r}', height={self.height!r}, weight={self.weight!r}, age={self.age!r}, gender={self.gender!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r})>"