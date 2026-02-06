from typing import Annotated, Optional

from fastapi import APIRouter, Form, HTTPException, Request
from sqlmodel import select as sql_select
from pydantic import BaseModel, Field

from auth_utils import password_hasher
from db_models import DbUser
from dependencies import DbSessionDependency, AuthedUserDependency

router = APIRouter(prefix="/user")

# pattern=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[.,;:#?!@$€%^&+*_|\/\\\<\>\-]).{8,}$"
class ReqUpdateUser(BaseModel):
    username: Optional[str] = Field(default=None,
                                 pattern=r"^[a-zA-Z][A-Za-z0-9_]{2,7}$",
                                 description="Username doesn't match the requirements")
    password: str | None = Field(default=None)
    newPassword: str | None = Field(default=None)

@router.patch("/")
async def update_user(db_session: DbSessionDependency, user: AuthedUserDependency, form_data: Annotated[ReqUpdateUser, Form()]):
    data_changed = False

    if form_data.username:
        existing_username = db_session.exec(sql_select(DbUser.id).where(DbUser.username == form_data.username.lower())).first()

        if existing_username:
            raise HTTPException(status_code=400, detail="Username already exists")

        user.username = form_data.username
        data_changed = True

    if form_data.password and form_data.newPassword:
        if form_data.password == form_data.newPassword:
            raise HTTPException(status_code=400, detail="New password is equal to the current one")

        if not password_hasher.verify(form_data.password, user.password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        user.password = password_hasher.hash(form_data.newPassword)
        data_changed = True


    if not data_changed:
        raise HTTPException(status_code=400, detail="Must provide username and/or password")

    db_session.add(user)
    db_session.commit()

    return {"username": user.username}