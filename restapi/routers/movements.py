from fastapi import APIRouter

router = APIRouter(prefix="/movements")

@router.get("/")
def temp():
    return {}