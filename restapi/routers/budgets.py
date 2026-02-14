from typing import Optional, Annotated

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session, select as sql_select, and_ as sql_and_

from db_models import DbWallet, DbBudget, DbMovement
from dependencies import AuthedUserDependency, DbSessionDependency
from rules import RegexPatterns

router = APIRouter(prefix="/budgets")

class ReqNewBudget(BaseModel):
    name: str = Field(pattern=RegexPatterns.BUDGET_NAME)
    description: Optional[str] = Field(default=None, max_length=512)
    start_balance: Optional[float] = Field(default=0)
    iconify_name: Optional[str] = Field(default=None, pattern=RegexPatterns.ICONIFY_ICON)
    color: Optional[str] = Field(default=None, pattern=RegexPatterns.HEX_COLOR)
    wallet_id: int = Field()

def does_wallet_belong_to_user(db_session: Session, wallet_id: int, user_id: int) -> bool:
    return db_session.exec(
        sql_select(DbWallet.id).where(sql_and_(DbWallet.id == wallet_id, DbWallet.user_id == user_id))
    ).first() is not None

@router.post("/")
async def create_budget(db_session: DbSessionDependency, user: AuthedUserDependency, form_data: Annotated[ReqNewBudget, Form()]):
    if not does_wallet_belong_to_user(db_session, form_data.wallet_id, user.id):
        raise HTTPException(status_code=400, detail="Wallet not found")

    new_budget = DbBudget(**form_data.model_dump())
    db_session.add(new_budget)

    start_balance_mvt = None
    if form_data.start_balance != 0:
        start_balance_mvt = DbMovement(
            budget=new_budget,
            title="Start balance",
            description="This movement represents the start balance of the budget",
            is_manual=False,
            amount=form_data.start_balance,
            is_deposit=form_data.start_balance > 0
        )
        db_session.add(start_balance_mvt)

    db_session.commit()

    result: dict = {
        "id": new_budget.id,
    }

    if start_balance_mvt is not None:
        result["movement"] = {
            "id": start_balance_mvt.id,
            "title": start_balance_mvt.title
        }

    return result