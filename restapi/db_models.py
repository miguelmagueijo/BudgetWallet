from datetime import datetime
from datetime import UTC as DATETIME_UTC

from sqlmodel import SQLModel, Field

class BaseDbModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(nullable=False, default=lambda: datetime.now(DATETIME_UTC))
    updated_at: datetime = Field(nullable=False, default=lambda: datetime.now(DATETIME_UTC))

class DbUser(BaseDbModel, table=True):
    __tablename__ = "user"

    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    is_active: bool = Field(nullable=False, default=False)
    is_admin: bool = Field(nullable=False, default=False)