from datetime import datetime
from datetime import UTC as DATETIME_UTC
from decimal import Decimal

from sqlalchemy import MetaData, Column, Numeric
from sqlmodel import SQLModel, Field, Relationship


class BaseDbModel(SQLModel):
    metadata = MetaData(schema="public")

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(nullable=False, default_factory=lambda: datetime.now(DATETIME_UTC))
    updated_at: datetime = Field(nullable=False,
                                 default_factory=lambda: datetime.now(DATETIME_UTC),
                                 sa_column_kwargs={
                                     "onupdate": lambda: datetime.now(DATETIME_UTC),
                                 })

class DbUser(BaseDbModel, table=True):
    __tablename__ = "user_account"

    username: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    is_active: bool = Field(nullable=False, default=False)
    is_admin: bool = Field(nullable=False, default=False)

    wallets: list["DbWallet"] = Relationship(back_populates="user")
    movement_category: list["DbMovementCategory"] = Relationship(back_populates="user")

class DbWallet(BaseDbModel, table=True):
    __tablename__ = "wallet"

    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    iconify_name: str = Field(nullable=False)
    color: str = Field(nullable=True, regex=r"^#[0-9a-fA-F]{6}$")
    user_id: int = Field(nullable=False, foreign_key="user_account.id")
    user: DbUser = Relationship(back_populates="wallets")

    budgets: list["DbBudget"] = Relationship(back_populates="wallet")

class DbBudget(BaseDbModel, table=True):
    __tablename__ = "budget"

    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    iconify_name: str = Field(nullable=True)
    color: str = Field(nullable=True, regex=r"^#[0-9a-fA-F]{6}$")

    wallet_id: int = Field(nullable=False, foreign_key="wallet.id")
    wallet: DbWallet = Relationship(back_populates="budgets")

    movements: list["DbMovement"] = Relationship(back_populates="budget")

class DbMovementCategory(BaseDbModel, table=True):
    __tablename__ = "movement_category"

    title: str = Field(nullable=False)
    description: str = Field(nullable=True)
    color: str = Field(nullable=True, regex=r"^#[0-9a-fA-F]{6}$")

    user_id: int = Field(nullable=False, foreign_key="user_account.id")
    user: DbUser = Relationship(back_populates="movement_category")

    movements: list["DbMovement"] = Relationship(back_populates="category")

class DbMovement(BaseDbModel, table=True):
    __tablename__ = "movement"

    title: str = Field(nullable=False)
    amount: Decimal = Field(sa_column=Column(Numeric(12, 4), nullable=False))
    is_deposit: bool = Field(nullable=False)
    done_at: datetime = Field(nullable=False, default_factory=lambda: datetime.now(DATETIME_UTC))

    budget_id: int = Field(nullable=False, foreign_key="budget.id")
    budget: DbBudget = Relationship(back_populates="movements")

    category_id: int = Field(nullable=True, foreign_key="movement_category.id")
    category: DbMovementCategory = Relationship(back_populates="movements")