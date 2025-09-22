from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str                
    username: str
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
