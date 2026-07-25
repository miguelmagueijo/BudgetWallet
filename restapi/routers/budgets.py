from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import (select as sql_select, and_ as sql_and_, func as sql_func, case as sql_case,
                      literal as sql_literal, Session, desc as sql_desc, or_ as sql_or_)

from db_models import DbWallet, DbBudget, DbMovement, DbMovementCategory
from db_utils import generic_record_delete, generic_record_patch
from dependencies import AuthedUserDependency, DbSessionDependency
from rules import RegexPatterns

router = APIRouter(prefix="/budgets")

# Requests classes
class ReqNewBudget(BaseModel):
    name: str = Field(pattern=RegexPatterns.WALLET_BUDGET_NAME)
    description: Optional[str] = Field(default=None, max_length=512)
    iconify_name: Optional[str] = Field(default=None, pattern=RegexPatterns.ICONIFY_ICON, alias="icon")
    color: Optional[str] = Field(default=None, pattern=RegexPatterns.HEX_COLOR)
    wallet_id: int = Field()

class ReqEditBudget(ReqNewBudget):
    name: Optional[str] = Field(default=None, pattern=RegexPatterns.WALLET_BUDGET_NAME)
    wallet_id: None = None

class ReqNewBudgetMovement(BaseModel):
    title: str = Field(pattern=RegexPatterns.WALLET_BUDGET_NAME)
    description: Optional[str] = Field(default=None, max_length=512)
    amount: Decimal = Field()
    is_deposit: bool = Field(default=True)
    done_at: Optional[datetime] = Field(default=None)
    category_id: Optional[int] = Field(default=None)

# Response classes
class ResBudgetMovementCategory(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_global: bool

class ResBudgetMovement(BaseModel):
    id: int
    title: str
    amount: Decimal
    is_deposit: bool
    done_at: datetime
    category: Optional[ResBudgetMovementCategory] = None

class ResBudget(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    color: Optional[str]
    balance: Decimal = Decimal(0)
    movements: Optional[list[ResBudgetMovement]] = None

def does_wallet_belong_to_user(db_session: Session, wallet_id: int, user_id: int) -> bool:
    return db_session.exec(
        sql_select(DbWallet.id).where(sql_and_(DbWallet.id == wallet_id, DbWallet.user_id == user_id))
    ).first() is not None

@router.get("/", response_model=dict[int, ResBudget], response_model_exclude_none=True)
async def get_budgets(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int,
                      with_movements: bool = False):
    budgets_results: dict[int, ResBudget] = {}

    filters = [DbWallet.id == wallet_id, DbWallet.user_id == user.id]
    budgets_query = (
        sql_select(
            DbBudget.id.label("budget_id"),
            DbBudget.name.label("budget_name"),
            DbBudget.iconify_name.label("budget_icon"),
            DbBudget.color.label("budget_color"),
            sql_func.coalesce(
                sql_func.sum(
                    sql_case(
                        (DbMovement.is_deposit, DbMovement.amount),
                        else_=-DbMovement.amount
                    )
                ),
                sql_literal(0)
            ).label("balance")
        )
        .outerjoin_from(DbBudget, DbMovement)
        .join(DbWallet)
        .where(sql_and_(*filters))
        .group_by(DbBudget.id, DbBudget.name)
        .order_by(DbBudget.name)
    )

    budgets_ids = []
    for row in db_session.exec(budgets_query).mappings():
        budget = ResBudget(
            id=row["budget_id"],
            name=row["budget_name"],
            icon=row["budget_icon"],
            color=row["budget_color"],
            movements=[] if with_movements else None,
        )

        budgets_results[budget.id] = budget

        if with_movements:
            budgets_ids.append(budget.id)

        budget.balance = row["balance"]

    if len(budgets_ids) > 0:
        movements_query = (
            sql_select(
                DbMovement.id,
                DbMovement.budget_id,
                DbMovement.title,
                DbMovement.amount,
                DbMovement.is_deposit,
                DbMovement.done_at,
                DbMovementCategory.id.label("mvt_id"),
                DbMovementCategory.title.label("mvt_title"),
                DbMovementCategory.description.label("mvt_desc"),
                DbMovementCategory.user_id.label("mvt_user_id"),
            )
            .outerjoin(DbMovementCategory)
            .where(DbMovement.budget_id.in_(budgets_ids))
            .order_by(sql_desc(DbMovement.done_at))
        )

        for row in db_session.exec(movements_query).mappings():
            movement = ResBudgetMovement(**row)
            if row["mvt_id"] is not None:
                movement.category = ResBudgetMovementCategory(
                    id=row["mvt_id"],
                    title=row["mvt_title"],
                    description=row["mvt_desc"],
                    is_global=row["mvt_user_id"] is None,
                )
            budgets_results.get(row.budget_id).movements.append(movement)

    return budgets_results

@router.get("/{budget_id}")
async def get_budget(db_session: DbSessionDependency, user: AuthedUserDependency, budget_id: int,
                     with_budgets: bool = False):
    # TODO

    return {}

@router.post("/")
async def create_budget(db_session: DbSessionDependency, user: AuthedUserDependency, form_data: Annotated[ReqNewBudget, Form()]):
    if not does_wallet_belong_to_user(db_session, form_data.wallet_id, user.id):
        raise HTTPException(status_code=400, detail="Wallet to insert budget not found")

    new_budget = DbBudget(**form_data.model_dump())

    db_session.add(new_budget)
    db_session.commit()

    return { "id": new_budget.id }

@router.patch("/{budget_id}")
async def update_budget(db_session: DbSessionDependency, user: AuthedUserDependency, budget_id: int,
                        form_data: Annotated[ReqEditBudget, Form()]):
    target_budget: DbBudget | None = db_session.exec(
        sql_select(DbBudget)
        .join(DbWallet)
        .where(sql_and_(DbBudget.id == budget_id, DbWallet.user_id == user.id))
    ).first()

    generic_record_patch(db_session, target_budget, form_data, "Budget not found")

    return {"id": budget_id}

@router.delete("/{budget_id}")
async def delete_budget(db_session: DbSessionDependency, user: AuthedUserDependency, budget_id: int):
    target_budget: DbBudget | None = db_session.exec(
        sql_select(DbBudget)
        .join(DbWallet)
        .where(sql_and_(DbBudget.id == budget_id, DbWallet.user_id == user.id))
    ).first()

    generic_record_delete(db_session, target_budget, "Budget not found")

    return {"id": budget_id}

# Movements
@router.get("/{budget_id}/movements", response_model=dict[int, ResBudgetMovement], response_model_exclude_none=True)
async def get_budget_movements(db_session: DbSessionDependency, user: AuthedUserDependency, budget_id: int):
    target_budget: DbBudget | None = db_session.exec(
        sql_select(DbBudget)
        .join(DbWallet)
        .where(sql_and_(DbBudget.id == budget_id, DbWallet.user_id == user.id))
    ).first()

    if target_budget is None:
        raise HTTPException(status_code=400, detail="Budget to fetch movements not found")

    query_movements = (
        sql_select(
            DbMovement.id,
            DbMovement.budget_id,
            DbMovement.title,
            DbMovement.amount,
            DbMovement.is_deposit,
            DbMovement.done_at,
            DbMovementCategory.id.label("mvt_id"),
            DbMovementCategory.title.label("mvt_title"),
            DbMovementCategory.description.label("mvt_desc"),
            DbMovementCategory.user_id.label("mvt_user_id"),
        )
        .outerjoin(DbMovementCategory)
        .where(DbMovement.budget_id == budget_id)
        .order_by(sql_desc(DbMovement.done_at))
    )

    movements: dict[int, ResBudgetMovement] = {}

    for row in db_session.exec(query_movements).mappings():
        movement = ResBudgetMovement(**row)
        if row["mvt_id"] is not None:
            movement.category = ResBudgetMovementCategory(
                id=row["mvt_id"],
                title=row["mvt_title"],
                description=row["mvt_desc"],
                is_global=row["mvt_user_id"] is None,
            )
        movements[movement.id] = movement

    return movements

@router.post("/{budget_id}/movements")
async def create_new_budget_movement(db_session: DbSessionDependency, user: AuthedUserDependency, budget_id: int,
                                     form_data: Annotated[ReqNewBudgetMovement, Form()]):
    target_budget: DbBudget | None = db_session.exec(
        sql_select(DbBudget)
        .join(DbWallet)
        .where(sql_and_(DbBudget.id == budget_id, DbWallet.user_id == user.id))
    ).first()

    if target_budget is None:
        raise HTTPException(status_code=400, detail="Budget to create movement not found")

    if form_data.category_id is not None:
        target_category = (
            sql_select(DbMovementCategory)
            .where(sql_and_(DbMovementCategory.id == form_data.category_id,
                            sql_or_(DbMovementCategory.user_id.is_(None),
                                    DbMovementCategory.user_id == user.id))
                   )
        )
        if db_session.exec(target_category).first() is None:
            raise HTTPException(status_code=404, detail="Movement category not found")

    movement = DbMovement(**form_data.model_dump())

    movement.budget_id = budget_id

    if movement.amount < 0:
        movement.is_deposit = False
        movement.amount = -movement.amount

    db_session.add(movement)
    db_session.commit()

    return {"id": movement.id}