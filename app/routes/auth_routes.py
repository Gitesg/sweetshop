from fastapi import APIRouter, status

from app.schemas.auth_schemas import RegisterRequest,LoginRequest,UserResponse,TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])
auth_service = AuthService()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest):
    return auth_service.register_user(payload.username, payload.email, payload.password)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_user(payload: LoginRequest):
    return auth_service.login_user(payload.username, payload.password)

@router.get("/login")
def login_health_check():
    return {"status": "ok"}
