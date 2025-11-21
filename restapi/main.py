from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import dependencies
from auth_utils import create_token, authenticate_user
from requests_models import ReqLogin

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app = FastAPI(
    title=dependencies.settings.app_name,
    version=dependencies.settings.version,
    contact={
        "name": "Miguel Magueijo",
        "url": "https://miguelmagueijo.pt",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

########################################################################################################################
# Dependencies
########################################################################################################################

########################################################################################################################
# Routes
########################################################################################################################
from routers.wallets import router as wallets_router

app.include_router(wallets_router)

@app.get("/")
def root():
    return {"name": dependencies.settings.app_name, "version": dependencies.settings.version}

@app.post("/login")
async def login(form_data: Annotated[ReqLogin, Form()], db_session: dependencies.DbSessionDependency):
    user = authenticate_user(form_data.username, form_data.password, db_session)

    response = JSONResponse(content={"message": "Login successful", "user_id": user.id})
    response.set_cookie(key="bw_token", value=create_token(dependencies.settings, user), path="/", samesite="lax", secure=False, httponly=True)

    return response