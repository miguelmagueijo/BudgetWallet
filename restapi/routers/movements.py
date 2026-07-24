from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated

from fastapi import APIRouter, Form
from pydantic import BaseModel, Field
from sqlmodel import (select as sql_select, and_ as sql_and_, Session)

from db_models import DbMovement, DbBudget, DbWallet
from db_utils import generic_record_patch, generic_record_delete
from dependencies import DbSessionDependency, AuthedUserDependency
from rules import RegexPatterns

router = APIRouter(prefix="/movements")

class ReqEditMovement(BaseModel):
    title: Optional[str] = Field(default=None, pattern=RegexPatterns.WALLET_BUDGET_NAME)
    description: Optional[str] = Field(default=None, max_length=512)
    amount: Optional[Decimal] = Field(default=Decimal(0))
    is_deposit: bool = Field(default=True)
    done_at: Optional[datetime] = Field(default=None)
    category_id: Optional[int] = Field(default=None)

def fetch_target_movement(db_session: Session, movement_id: int, user_id: int) -> DbMovement | None:
    return db_session.exec(
        sql_select(DbMovement)
        .join_from(DbMovement, DbBudget)
        .join_from(DbBudget, DbWallet)
        .where(sql_and_(DbMovement.id == movement_id, DbWallet.user_id == user_id))
    ).first()

@router.get("/{movement_id}")
async def update_movement(db_session: DbSessionDependency, user: AuthedUserDependency, movement_id: int):
    target_movement = fetch_target_movement(db_session, movement_id, user.id)

    return target_movement

@router.patch("/{movement_id}")
async def update_movement(db_session: DbSessionDependency, user: AuthedUserDependency, movement_id: int,
                        form_data: Annotated[ReqEditMovement, Form()]):
    target_movement = fetch_target_movement(db_session, movement_id, user.id)

    generic_record_patch(db_session, target_movement, form_data, "Movement not found")

    return {"id": movement_id}

@router.delete("/{movement_id}")
async def delete_budget(db_session: DbSessionDependency, user: AuthedUserDependency, movement_id: int):
    target_movement = fetch_target_movement(db_session, movement_id, user.id)

    generic_record_delete(db_session, target_movement, "Movement not found")

    return {"id": movement_id}