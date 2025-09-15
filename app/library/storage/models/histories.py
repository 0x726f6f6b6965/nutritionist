from sqlalchemy import BigInteger, SmallInteger, Text, LargeBinary, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text
from .base import Base

# Define a Python class (model) mapping to a PostgreSQL table
class History(Base):
    __tablename__ = 'histories'
    id: Mapped[int] = mapped_column(primary_key=True)
    line_id: Mapped[int] = mapped_column(Text,ForeignKey('users.line_id', ondelete='CASCADE'), nullable=False)
    meal: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    photo: Mapped[bytes] = mapped_column(LargeBinary)
    calories_kcal: Mapped[int] = mapped_column(BigInteger)
    protein_g: Mapped[int] = mapped_column(BigInteger)
    carbs_g: Mapped[int] = mapped_column(BigInteger)
    fat_g: Mapped[int] = mapped_column(BigInteger)
    sodium_mg: Mapped[int] = mapped_column(BigInteger)
    ai_description: Mapped[str] = mapped_column(Text)
    ai_suggest: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(TIMESTAMP,nullable=False, server_default=text('now()'))
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text('now()'))

    def __repr__(self):
        return f"<History(line_id={self.line_id!r}, meal={self.meal!r}, description={self.description!r}, calories_kcal={self.calories_kcal!r}, protein_g={self.protein_g!r}, carbs_g={self.carbs_g!r}, fat_g={self.fat_g!r}, sodium_mg={self.sodium_mg!r}, ai_description={self.ai_description!r}, ai_suggest={self.ai_suggest!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r})>"
