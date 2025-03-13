from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_index():
    return {"message": "Welcome to the AI-Crypto Trader API"}
