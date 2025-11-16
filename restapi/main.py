from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status, Form, Cookie
from fastapi.responses import JSONResponse
from sqlmodel import create_engine, Session
from jwt import decode as jwt_decode

from auth_utils import create_token, authenticate_user
from requests_models import ReqJwtUserData, ReqLogin
from utils_classes import Settings

settings = Settings()
db_engine = create_engine(settings.db_url)
app = FastAPI()

########################################################################################################################
# Dependencies
########################################################################################################################
def get_db_session():
    with Session(db_engine) as db_session:
        yield db_session

async def get_current_user(bw_token: Annotated[str | None, Cookie()]) -> ReqJwtUserData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt_decode(bw_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm], issuer=settings.jwt_issuer)
    except Exception as e:
        print(e)
        raise credentials_exception

    return ReqJwtUserData(**payload.get("user_data"))

DbSessionDependency = Annotated[Session, Depends(get_db_session)]
JwtUserDataDependency = Annotated[ReqJwtUserData, Depends(get_current_user)]


########################################################################################################################
# Routes
########################################################################################################################
@app.get("/")
def root():
    return {"name": settings.app_name, "version": settings.version}

@app.post("/login")
async def login(form_data: Annotated[ReqLogin, Form()], db_session: DbSessionDependency):
    user = authenticate_user(form_data.username, form_data.password, db_session)

    response = JSONResponse(content={"message": "Login successful", "user_id": user.id})
    response.set_cookie(key="bw_token", value=create_token(settings, user), httponly=True)

    return response

@app.get("/my-data")
async def my_data(user: JwtUserDataDependency):
    return user