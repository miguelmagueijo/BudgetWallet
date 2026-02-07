from fastapi import APIRouter

router = APIRouter(prefix="/budgets")

@router.get("/")
def tmp():
    return {}