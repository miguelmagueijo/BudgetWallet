from pydantic import BaseModel

class ReqLogin(BaseModel):
    username: str
    password: str

class ReqJwtUserData(BaseModel):
    id: int
    username: str
    is_admin: bool