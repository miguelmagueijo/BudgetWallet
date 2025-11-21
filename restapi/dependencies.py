from typing import Annotated

from fastapi import Depends, Cookie, HTTPException, status
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, Select
from sqlmodel import Session, select as sql_select
from jwt import decode as jwt_decode

from db_models import DbUser


class Settings(BaseSettings):
    app_name: str = "Budget Wallet REST API"
    version: str = "0.0.1"
    jwt_secret: str
    jwt_algorithm: str
    jwt_issuer: str
    db_url: str
    minutes_to_expire_token: int = 60 * 24 * 7

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

db_engine = create_engine(settings.db_url)

def get_db_session():
    db_session = Session(db_engine)
    try:
        yield db_session
    finally:
        db_session.close()

DbSessionDependency = Annotated[Session, Depends(get_db_session)]

async def get_authenticated_user(db_session: DbSessionDependency, bw_token: Annotated[str | None, Cookie()]) -> DbUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if bw_token is None:
        raise credentials_exception

    try:
        payload = jwt_decode(bw_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm], issuer=settings.jwt_issuer)
    except Exception as e:
        print(e)
        raise credentials_exception

    user: DbUser | None = db_session.exec(sql_select(DbUser).where(DbUser.id == payload["user_data"]["id"])).first()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="User is not active")

    return user

AuthedUserDependency = Annotated[DbUser, Depends(get_authenticated_user)]