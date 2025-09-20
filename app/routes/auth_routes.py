
from fastapi import APIRouter

router = APIRouter()


@router.get("/register")
def resgister_user():
    return {"status": "ok"}


@router.post("/register")
def create_user():
    return {"status": "ok"}


@router.get("/login")
def health_check(): 
    return {"status": "ok"}

@router.post("/login")
def login_user():
    return {"status": "ok"}