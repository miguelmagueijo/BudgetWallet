from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import select as sql_select, and_ as sql_and_, func as sql_func, literal as sql_literal, case as sql_case

from db_models import DbBudget, DbWallet, DbMovement
from dependencies import AuthedUserDependency, DbSessionDependency

router = APIRouter(prefix="/budgets")



@router.get("/{wallet_id}")
async def get_all_of_wallet(db_session: DbSessionDependency, user: AuthedUserDependency, wallet_id: int):
    query_budgets = (
        sql_select(
            DbBudget.id,
            DbBudget.name,
            DbBudget.iconify_name,
            DbBudget.color,
            DbBudget.is_permanent,
            sql_func.coalesce(
                sql_func.sum(
                    sql_case((DbMovement.is_deposit, DbMovement.amount), else_=-DbMovement.amount)
                ),
                sql_literal(0)
            ).label("budget_total")
        )
        .join_from(DbBudget, DbWallet).outerjoin_from(DbBudget, DbMovement)
        .where(sql_and_(DbBudget.wallet_id == wallet_id, DbWallet.user_id == user.id))
        .group_by(DbBudget.id, DbBudget.name)
    )

    budgets_data = []
    for row in db_session.exec(query_budgets):
        budgets_data.append(row._mapping)

    return budgets_data
