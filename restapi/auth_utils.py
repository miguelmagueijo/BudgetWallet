from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlmodel import Session, select as sql_select

from db_models import DbUser
from main import Settings

password_hasher = PasswordHash.recommended()

def create_token(settings: Settings, user: DbUser, data: dict | None = None, expires_delta: timedelta | None = None) -> str:
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