from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import FastAPI, Depends, HTTPException, status, Form, Cookie
from fastapi.responses import JSONResponse
from pwdlib import PasswordHash
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Budget Wallet REST API"
    version: str = "0.0.1"
    jwt_secret: str
    jwt_algorithm: str
    minutes_to_expire_token: int = 60 * 24 * 7

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
password_hasher = PasswordHash.recommended()
app = FastAPI()

fake_db = {
    "users": {
        "test": {
            "id": 1,
            "username": "test",
            "name": "Test user",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$nTJzzhYSdyik+FH1NdokvQ$DuewEtUkC3IMhZhz36c8QkePENsNpc+6P9++a4E6GaQ",
            "is_active": True,
        },
        "disabled": {
            "id": 2,
            "username": "disabled",
            "name": "Disabled user",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$nTJzzhYSdyik+FH1NdokvQ$DuewEtUkC3IMhZhz36c8QkePENsNpc+6P9++a4E6GaQ",
            "is_active": False,
        }
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class BasicUserData(BaseModel):
    id: int
    username: str

class ReqLogin(BaseModel):
    username: str
    password: str

def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.minutes_to_expire_token)

    data_to_encode = {
        #"iss": "https://budgetwallet.miguelmagueijo.pt",
        "sub": data["username"],
        #"aud": "s6BhdRkqt3",
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "data": data.copy()
    }

    encoded_jwt = jwt.encode(data_to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    return encoded_jwt

def authenticate_user(username: str, password: str) -> BasicUserData:
    user = fake_db["users"].get(username, False)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not password_hasher.verify(password, user["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User credentials invalid")

    return BasicUserData(**user)

async def get_current_user(bw_token: Annotated[str | None, Cookie()]) -> BasicUserData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(bw_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except Exception as e:
        print(e)

        raise credentials_exception

    user = fake_db["users"].get(username, False)

    if not user:
        raise credentials_exception

    return BasicUserData(**user)

@app.get("/")
def root():
    print("here")
    return {"name": settings.app_name, "version": settings.version}

@app.post("/login")
async def login(form_data: Annotated[ReqLogin, Form()]):
    user = authenticate_user(form_data.username, form_data.password)

    response = JSONResponse(content={"message": "Login successful", "user_id": user.id})
    response.set_cookie(key="bw_token", value=create_token({"id": user.id, "username": user.username}), httponly=True)

    return response

@app.get("/my-data")
async def my_data(user: Annotated[BasicUserData, Depends(get_current_user)]):
    return {"id": user.id, "username": user.username}