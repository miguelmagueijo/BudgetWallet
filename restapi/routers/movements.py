from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated, Any

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import (select as sql_select, and_ as sql_and_, or_ as sql_or_, Session)

from db_models import DbMovement, DbBudget, DbWallet, DbMovementCategory, DbUser
from db_utils import generic_record_patch, generic_record_delete
from dependencies import DbSessionDependency, AuthedUserDependency
from rules import RegexPatterns

router = APIRouter(prefix="/movements")

class ReqNewMovementCategory(BaseModel):
    title: str = Field(pattern=RegexPatterns.WALLET_BUDGET_NAME)
    description: Optional[str] = Field(default=None, max_length=64)
    color: Optional[str] = Field(default=None, pattern=RegexPatterns.HEX_COLOR)
    is_global: Optional[bool] = Field(default=False)

class ReqEditMovementCategory(ReqNewMovementCategory):
    title: Optional[str] = Field(default=None, pattern=RegexPatterns.WALLET_BUDGET_NAME)
    is_global: Optional[bool] = Field(default=None)

class EditMovementCategoryInterceptor(ReqEditMovementCategory):
    user_id: int = Field()

class ReqEditMovement(BaseModel):
    title: Optional[str] = Field(default=None, pattern=RegexPatterns.WALLET_BUDGET_NAME)
    description: Optional[str] = Field(default=None, max_length=512)
    amount: Optional[Decimal] = Field(default=Decimal(0))
    is_deposit: bool = Field(default=True)
    done_at: Optional[datetime] = Field(default=None)
    category_id: Optional[int] = Field(default=None)

class ResMovementCategory(BaseModel):
    id: int
    title: str
    description: Optional[str]
    color: Optional[str]
    is_global: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

# Inner functions
def fetch_target_movement(db_session: Session, movement_id: int, user_id: int) -> DbMovement | None:
    return db_session.exec(
        sql_select(DbMovement)
        .join_from(DbMovement, DbBudget)
        .join_from(DbBudget, DbWallet)
        .where(sql_and_(DbMovement.id == movement_id, DbWallet.user_id == user_id))
    ).first()

def fetch_target_category(db_session: Session, category_id: int, user: DbUser) -> DbMovementCategory | None:
    or_filters = [DbMovementCategory.user_id == user.id]

    if user.is_admin:
        or_filters.append(DbMovementCategory.user_id.is_(None))

    return db_session.exec(
        sql_select(DbMovementCategory)
        .where(sql_and_(DbMovementCategory.id == category_id, sql_or_(*or_filters)))
    ).first()

# Movements Categories
# They need to go first because if not /<movement_id> doesn't let /categories register. It resolves first
@router.get("/categories")
async def get_movements_categories(db_session: DbSessionDependency, user: AuthedUserDependency):
    query_categories = (
        sql_select(DbMovementCategory)
        .where(sql_or_(DbMovementCategory.user_id.is_(None), DbMovementCategory.user_id == user.id))
        .order_by(DbMovementCategory.title)
    )

    categories_result: dict[int, ResMovementCategory] = {}

    for row in db_session.exec(query_categories):
        category = ResMovementCategory(**row.model_dump(), is_global=row.user_id is None)

        categories_result[category.id] = category

    return categories_result

@router.post("/categories")
async def create_movement_category(db_session: DbSessionDependency, user: AuthedUserDependency,
                                   form_data: Annotated[ReqNewMovementCategory, Form()]):
    if form_data.is_global:
        form_data.is_global = user.is_admin == True

    category = DbMovementCategory(**form_data.model_dump())

    if not form_data.is_global:
        category.user = user

    db_session.add(category)
    db_session.commit()

    return {"id": category.id}

@router.patch("/categories/{category_id}")
async def update_movement_category(db_session: DbSessionDependency, user: AuthedUserDependency, category_id: int,
                        form_data: Annotated[ReqEditMovementCategory, Form()]):
    target_category = fetch_target_category(db_session, category_id, user)

    def before_update(target: DbMovementCategory, update_data: dict[str, Any]):
        if "is_global" in update_data.keys():
            if update_data["is_global"]:
                target.user = None if user.is_admin else target.user
            else:
                target.user = user

    generic_record_patch(db_session, target_category, form_data, "Movement category not found", before_update)

    return {"id": category_id}

@router.delete("/categories/{category_id}")
async def delete_movement_category(db_session: DbSessionDependency, user: AuthedUserDependency, category_id: int):
    target_category = fetch_target_category(db_session, category_id, user)

    generic_record_delete(db_session, target_category,  "Movement category not found")

    return {"id": category_id}

# Movements
@router.get("/{movement_id}")
async def get_movement(db_session: DbSessionDependency, user: AuthedUserDependency, movement_id: int):
    target_movement = fetch_target_movement(db_session, movement_id, user.id)

    return target_movement

@router.patch("/{movement_id}")
async def update_movement(db_session: DbSessionDependency, user: AuthedUserDependency, movement_id: int,
                        form_data: Annotated[ReqEditMovement, Form()]):
    target_movement = fetch_target_movement(db_session, movement_id, user.id)

    def before_update(target: DbMovement, update_data: dict[str, Any]):
        if "category_id" in update_data.keys():
            if update_data["category_id"] <= 0:
                update_data["category_id"] = None
            else:
                target_category = (
                    sql_select(DbMovementCategory)
                    .where(sql_and_(DbMovementCategory.id == form_data.category_id,
                                    sql_or_(DbMovementCategory.user_id.is_(None),
                                            DbMovementCategory.user_id == user.id))
                           )
                )
                if db_session.exec(target_category).first() is None:
                    raise HTTPException(status_code=404, detail="Movement category not found")

    generic_record_patch(db_session, target_movement, form_data, "Movement not found", before_update)

    return {"id": movement_id}

@router.delete("/{movement_id}")
async def delete_movement(db_session: DbSessionDependency, user: AuthedUserDependency, movement_id: int):
    target_movement = fetch_target_movement(db_session, movement_id, user.id)

    generic_record_delete(db_session, target_movement, "Movement not found")

    return {"id": movement_id}