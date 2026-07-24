from typing import Annotated, Optional, Union

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import (select as sql_select, and_ as sql_and_, func as sql_func, case as sql_case,
                      literal as sql_literal, desc as sql_desc, over as sql_over)

from dependencies import DbSessionDependency, AuthedUserDependency
from db_models import DbWallet, DbBudget, DbMovement
from rules import RegexPatterns

router = APIRouter(prefix="/wallets")

class ReqNewWallet(BaseModel):
    name: str = Field(min_length=3, max_length=32)
    description: Optional[str] = Field(default=None, max_length=512)
    iconify_name: Optional[str] = Field(default=None, pattern=RegexPatterns.ICONIFY_ICON)
    color: Optional[str] = Field(default=None, pattern=RegexPatterns.HEX_COLOR)

class ReqEditWallet(ReqNewWallet):
    name: Optional[str] = Field(default=None, min_length=3, max_length=32)

class ResWalletBudget(BaseModel):
    id: int
    name: str
    color: Optional[str]
    total: float = 0

class ResWallet(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    color: Optional[str]
    balance: float = 0
    budgets: Optional[list[ResWalletBudget]] = None

def fetch_wallets(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: Optional[int] = None,
                  with_budgets: bool = False):
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
                total=row["budget_balance"]
            ))

        wallet.balance += row["budget_balance"]

    return wallets_results

@router.get("/", response_model=Union[dict[int,ResWallet], ResWallet], response_model_exclude_none=True)
async def get_wallets(db_session: DbSessionDependency, user: AuthedUserDependency, with_budgets: bool = False):
    return fetch_wallets(db_session, user, with_budgets=with_budgets)

@router.get("/{wallet_id}")
async def get_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int,
                     with_budgets: bool = False):
    result = fetch_wallets(db_session, user, wallet_id, with_budgets)

    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return result[wallet_id]

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

    if target_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    update_data = form_data.model_dump(exclude_unset=True)

    if len(update_data.keys()) == 0:
        return {"id": wallet_id}

    for key, value in update_data.items():
        setattr(target_wallet, key, value)

    db_session.add(target_wallet)
    db_session.commit()

    return {"id": wallet_id}

@router.delete("/{wallet_id}")
async def delete_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int):
    target_wallet = db_session.exec(
        sql_select(DbWallet)
        .where(sql_and_(DbWallet.id == wallet_id, DbWallet.user == user))
    ).first()

    if target_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    db_session.delete(target_wallet)
    db_session.commit()

    return {"id": target_wallet.id}