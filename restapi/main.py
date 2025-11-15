import jwt

from typing import Annotated
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Form, Cookie
from fastapi.responses import JSONResponse
from pwdlib import PasswordHash
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import create_engine, Session, select as sql_select

from db_models import DbUser
from requests_models import ReqJwtUserData, ReqLogin


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
password_hasher = PasswordHash.recommended()
app = FastAPI()
db_engine = create_engine(settings.db_url)

def get_db_session():
    with Session(db_engine) as db_session:
        yield db_session

DbSessionDependency = Annotated[Session, Depends(get_db_session)]

class BasicUserData(BaseModel):
    id: int
    username: str

def create_token(user: DbUser, data: dict | None = None, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.minutes_to_expire_token)

    data_to_encode = {
        "iss": settings.jwt_issuer,
        "sub": f"{user.id}:{user.username}",
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "user_data": {
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin,
        },
    }

    if isinstance(data, dict):
        data_to_encode.update(data)

    encoded_jwt = jwt.encode(data_to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    return encoded_jwt

def authenticate_user(username: str, password: str, db_session: Session) -> DbUser:
    get_user_stmt = sql_select(DbUser).where(DbUser.username == username)

    user: DbUser = db_session.exec(get_user_stmt).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User for given credentials was not found")

    if not password_hasher.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User for given credentials was not found")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

    return user

async def get_current_user(bw_token: Annotated[str | None, Cookie()]) -> ReqJwtUserData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(bw_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm], issuer=settings.jwt_issuer)
    except Exception as e:
        print(e)
        raise credentials_exception

    return ReqJwtUserData(**payload.get("user_data"))

JwtUserDataDependency = Annotated[ReqJwtUserData, Depends(get_current_user)]

@app.get("/")
def root():
    return {"name": settings.app_name, "version": settings.version}

@app.post("/login")
async def login(form_data: Annotated[ReqLogin, Form()], db_session: DbSessionDependency):
    user = authenticate_user(form_data.username, form_data.password, db_session)

    response = JSONResponse(content={"message": "Login successful", "user_id": user.id})
    response.set_cookie(key="bw_token", value=create_token(user), httponly=True)

    return response

@app.get("/my-data")
async def my_data(user: JwtUserDataDependency):
    return user