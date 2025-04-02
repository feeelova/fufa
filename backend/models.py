from sqlalchemy import (
    String,
    BigInteger,
)
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
