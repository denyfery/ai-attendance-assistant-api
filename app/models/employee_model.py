from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DECIMAL
from decimal import Decimal

from app.database.base import Base

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    salary: Mapped[Decimal] = mapped_column(
        DECIMAL(15,2),
        nullable=False
    )