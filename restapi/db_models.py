from datetime import datetime
from datetime import UTC as DATETIME_UTC

from sqlalchemy import MetaData
from sqlmodel import SQLModel, Field, Relationship


class BaseDbModel(SQLModel):
    metadata = MetaData(schema="public")

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(nullable=False, default_factory=lambda: datetime.now(DATETIME_UTC))
    updated_at: datetime = Field(nullable=False, default_factory=lambda: datetime.now(DATETIME_UTC))

class DbUser(BaseDbModel, table=True):
    __tablename__ = "user_account"

    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    is_active: bool = Field(nullable=False, default=False)
    is_admin: bool = Field(nullable=False, default=False)

    wallets: list["DbWallet"] = Relationship(back_populates="user")

class DbWallet(BaseDbModel, table=True):
    __tablename__ = "wallet"

    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    iconify_name: str = Field(nullable=False)
    color: str = Field(nullable=False)
    start_balance: float = Field(default=0, lt=1000000, gt=-1000000)
    user_id: int = Field(nullable=False, foreign_key="user_account.id")
    user: DbUser = Relationship(back_populates="wallets")