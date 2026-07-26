from decimal import Decimal
from typing import Annotated, Optional, Union

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import (select as sql_select, and_ as sql_and_, func as sql_func, case as sql_case,
                      literal as sql_literal, desc as sql_desc, over as sql_over)

from db_utils import generic_record_delete, generic_record_patch
from dependencies import DbSessionDependency, AuthedUserDependency
from db_models import DbWallet, DbBudget, DbMovement, DbMovementCategory
from response_models import ArrayDataResponseModel, ObjectDataResponseModel
from routers.budgets import ReqNewBudget, ResBudget, ResBudgetMovement, ResBudgetMovementCategory
from rules import RegexPatterns

router = APIRouter(prefix="/wallets")

class ReqNewWallet(BaseModel):
    name: str = Field(pattern=RegexPatterns.WALLET_BUDGET_NAME)
    description: Optional[str] = Field(default=None, max_length=512)
    iconify_name: Optional[str] = Field(default=None, pattern=RegexPatterns.ICONIFY_ICON, alias="icon")
    color: Optional[str] = Field(default=None, pattern=RegexPatterns.HEX_COLOR)

class ReqEditWallet(ReqNewWallet):
    name: Optional[str] = Field(default=None, pattern=RegexPatterns.WALLET_BUDGET_NAME)

class ResWalletBudget(BaseModel):
    id: int
    name: str
    color: Optional[str]
    balance: Decimal = Decimal(0)

class ResWallet(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    color: Optional[str]
    balance: Decimal = Decimal(0)
    budgets: Optional[list[ResWalletBudget]] = None

def fetch_wallets(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: Optional[int] = None,
                  with_budgets: bool = False) -> tuple[dict[int, ResWallet], Decimal]:
    wallets_results: dict[int, ResWallet] = {}

    filters = [DbWallet.user == user]
    if wallet_id is not None:
        filters.append(DbWallet.id == wallet_id)

    wallets_query = (
        sql_select(
            DbWallet.id.label("wallet_id"),
            DbWallet.name.label("wallet_name"),
            DbWallet.iconify_name.label("wallet_icon"),
            DbWallet.color.label("wallet_color"),
            DbBudget.id.label("budget_id"),
            DbBudget.name.label("budget_name"),
            DbBudget.color.label("budget_color"),
            sql_func.coalesce(
                sql_func.sum(
                    sql_case(
                        (DbMovement.is_deposit, DbMovement.amount),
                        else_=-DbMovement.amount
                    )
                ),
                sql_literal(0)
            ).label("budget_balance")
        )
        .outerjoin_from(DbWallet, DbBudget)
        .outerjoin_from(DbBudget, DbMovement)
        .where(sql_and_(*filters))
        .group_by(DbWallet.id, DbWallet.name, DbBudget.id, DbBudget.name)
        .order_by(DbWallet.name)
    )

    account_balance = Decimal(0)

    for row in db_session.exec(wallets_query).mappings():
        wallet = wallets_results.get(row["wallet_id"])
        if not wallet:
            wallet = ResWallet(
                id=row["wallet_id"],
                name=row["wallet_name"],
                icon=row["wallet_icon"],
                color=row["wallet_color"],
                budgets=[] if with_budgets else None,
            )
            wallets_results[wallet.id] = wallet

        if with_budgets and row["budget_id"] is not None:
            wallet.budgets.append(ResWalletBudget(
                id=row["budget_id"],
                name=row["budget_name"],
                color=row["budget_color"],
                balance=row["budget_balance"]
            ))

        wallet.balance += row["budget_balance"]
        account_balance += row["budget_balance"]

    return wallets_results, account_balance

# Budgets part
@router.post("/{wallet_id}/budgets")
async def create_budget(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int,
                        form_data: Annotated[ReqNewBudget, Form()]):
    target_wallet = db_session.exec(
        sql_select(DbWallet.id).where(sql_and_(DbWallet.id == wallet_id, DbWallet.user_id == user.id))
    ).first()

    if target_wallet is None:
        raise HTTPException(status_code=400, detail="Wallet to insert budget not found")

    new_budget = DbBudget(**form_data.model_dump(), wallet_id=wallet_id)

    db_session.add(new_budget)
    db_session.commit()

    return { "id": new_budget.id }

@router.get("/{wallet_id}/budgets", response_model=dict[int, ResBudget], response_model_exclude_none=True)
async def get_budgets(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int,
                      with_movements: bool = False):
    budgets_results: dict[int, ResBudget] = {}

    filters = [DbWallet.id == wallet_id, DbWallet.user_id == user.id]
    budgets_query = (
        sql_select(
            DbBudget.id,
            DbBudget.name,
            DbBudget.iconify_name.label("icon"),
            DbBudget.color,
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
            **row,
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

# Wallets
@router.get("/", response_model=ArrayDataResponseModel[ResWallet], response_model_exclude_none=True)
async def get_wallets(db_session: DbSessionDependency, user: AuthedUserDependency, with_budgets: bool = False):
    result = fetch_wallets(db_session, user, with_budgets=with_budgets)

    meta = {
        "account_balance": result[1]
    }

    return ArrayDataResponseModel(data=result[0].values(), meta=meta)

@router.get("/{wallet_id}", response_model=ObjectDataResponseModel[ResWallet], response_model_exclude_none=True)
async def get_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int,
                     with_budgets: bool = False):
    result = fetch_wallets(db_session, user, wallet_id, with_budgets)[0]

    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return ObjectDataResponseModel(data=result[wallet_id])

@router.get("/{wallet_id}/budgets")
async def get_budgets_of_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int):
    query_budgets = (
        sql_select(
            DbBudget.id,
            DbBudget.name,
            DbBudget.iconify_name,
            DbBudget.color,
            sql_func.coalesce(
                sql_func.sum(
                    sql_case((DbMovement.is_deposit, DbMovement.amount), else_=-DbMovement.amount)
                ),
                sql_literal(0)
            ).label("budget_total")
        )
        .outerjoin_from(DbBudget, DbWallet)
        .outerjoin_from(DbBudget, DbMovement)
        .where(sql_and_(DbBudget.wallet_id == wallet_id, DbWallet.user_id == user.id))
        .group_by(DbBudget.id, DbBudget.name)
    )

    budgets_data = []
    for row in db_session.exec(query_budgets).mappings():
        budgets_data.append(row)

    return budgets_data

@router.get("/{wallet_id}/movements")
async def get_budgets_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int,
                             budget_id: Optional[int] = None):
    filters = [DbWallet.id == wallet_id, DbWallet.user_id == user.id]

    if budget_id is not None:
        filters.append(DbBudget.id == budget_id)

    query_movements = (
        sql_select(
            DbMovement,
            DbBudget.name,
            sql_over(
                sql_func.sum(
                    sql_case(
                        (DbMovement.is_deposit, DbMovement.amount),
                        else_=-DbMovement.amount
                    )
                ),
                DbMovement.budget_id,
                order_by=DbMovement.done_at
            )
        )
        .join_from(DbMovement, DbBudget).join_from(DbBudget, DbWallet)
        .where(sql_and_(*filters))
        .order_by(sql_desc(DbMovement.done_at))
    )

    data = []
    for row in db_session.exec(query_movements):
        row_data = row[0].model_dump()
        row_data["budget_name"] = row[1]
        row_data["budget_balance"] = row[2]
        data.append(row_data)

    return data

@router.post("/")
async def new_wallet(db_session: DbSessionDependency, user: AuthedUserDependency,
                     form_data: Annotated[ReqNewWallet, Form()]):
    new_wallet = DbWallet(user=user, **form_data.model_dump())

    db_session.add(new_wallet)
    db_session.commit()

    return {"id": new_wallet.id}

@router.patch("/{wallet_id}")
async def update_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int,
                        form_data: Annotated[ReqEditWallet, Form()]):
    target_wallet: DbWallet | None = db_session.exec(
        sql_select(DbWallet).where(sql_and_(DbWallet.id == wallet_id, DbWallet.user == user))).first()

    generic_record_patch(db_session, target_wallet, form_data, "Wallet not found")

    return {"id": wallet_id}

@router.delete("/{wallet_id}")
async def delete_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int):
    target_wallet = db_session.exec(
        sql_select(DbWallet)
        .where(sql_and_(DbWallet.id == wallet_id, DbWallet.user == user))
    ).first()

    generic_record_delete(db_session, target_wallet, "Wallet not found")

    return {"id": wallet_id}