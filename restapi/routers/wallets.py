from typing import Annotated, Optional

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import select as sql_select, and_ as sql_and_, func as sql_func, case as sql_case

from dependencies import DbSessionDependency, AuthedUserDependency
from db_models import DbWallet, DbBudget, DbMovement

router = APIRouter(prefix="/wallets")

class ReqNewWallet(BaseModel):
    name: str = Field(min_length=3, max_length=32)
    description: str | None = Field(default=None, max_length=512)
    start_balance: float = Field(default=0, lt=1000000, gt=-1000000)
    iconify_name: str | None = Field(default=None, pattern=r"^[a-z0-9]+(-[a-z0-9]+)*+:[a-z0-9]+(-[a-z0-9]+)*$")
    color: str | None = Field(default=None, pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$")

class ResWalletBudgetCard(BaseModel):
    id: int
    name: str
    color: Optional[str]
    total: float

class ResWalletCard(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    color: Optional[str]
    budgets: list[ResWalletBudgetCard] = []

@router.get("/", response_model=list[ResWalletCard])
async def get_all_wallets(db_session: DbSessionDependency, user: AuthedUserDependency):
    wallets_results: dict[int, ResWalletCard] = {}

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
                0
            ).label("budget_total")
        )
        .join(DbBudget, DbWallet.id == DbBudget.wallet_id)
        .outerjoin(DbMovement, DbBudget.id == DbMovement.budget_id)
        .where(DbWallet.user == user)
        .group_by(DbWallet.id, DbWallet.name, DbBudget.id, DbBudget.name)
    )

    for row in db_session.exec(wallets_query):
        row_dict = row._mapping

        wallet = wallets_results.get(row_dict["wallet_id"])
        if not wallet:
            wallet = ResWalletCard(
                id=row_dict["wallet_id"],
                name=row_dict["wallet_name"],
                icon=row_dict["wallet_icon"],
                color=row_dict["wallet_color"],
                budgets=[]
            )
            wallets_results[wallet.id] = wallet

        wallet.budgets.append(ResWalletBudgetCard(
                                id=row_dict["budget_id"],
                                name=row_dict["budget_name"],
                                color=row_dict["budget_color"],
                                total=row_dict["budget_total"]
                            ))

    return list(wallets_results.values())

@router.get("/{wallet_id}")
async def get_single_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int):
    wallet = db_session.exec(sql_select(DbWallet).where(sql_and_(DbWallet.id == wallet_id, DbWallet.user == user))).first()

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return wallet

@router.post("/new")
async def new_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, form_data: Annotated[ReqNewWallet, Form()]):
    new_wallet = DbWallet(user=user, **form_data.model_dump())

    db_session.add(new_wallet)
    db_session.commit()

    db_session.refresh(new_wallet)

    return {"id": new_wallet.id}


@router.delete("/delete/{wallet_id}")
async def delete_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int):
    target_wallet = db_session.exec(sql_select(DbWallet).where(sql_and_(DbWallet.id == wallet_id, DbWallet.user == user))).first()

    if target_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    db_session.delete(target_wallet)
    db_session.commit()

    return {"id": target_wallet.id}