from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import select as sql_select, and_ as sql_and_

from dependencies import DbSessionDependency, AuthedUserDependency
from db_models import DbWallet

router = APIRouter(prefix="/wallets")

class ReqNewWallet(BaseModel):
    name: str = Field(min_length=3, max_length=32)
    description: str | None = Field(default=None, max_length=512)
    start_balance: float = Field(default=0, lt=1000000, gt=-1000000)
    iconify_name: str | None = Field(default=None, pattern=r"^[a-z0-9]+(-[a-z0-9]+)*+:[a-z0-9]+(-[a-z0-9]+)*$")
    color: str | None = Field(default=None, pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$")

@router.get("/")
async def get_all_wallets(db_session: DbSessionDependency, user: AuthedUserDependency):
    return db_session.exec(sql_select(DbWallet).where(DbWallet.user == user)).all()

@router.get("/{wallet_id}")
async def get_all_wallets(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int):
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