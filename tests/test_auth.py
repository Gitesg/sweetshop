import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
# from app.db.database import get_db
# from app.db.models import User
# from sqlalchemy.orm import Session
import json

@pytest.mark.asyncio
async def test_register_user_success():
    """Test successful user registration"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "123456"
        })

    assert response.status_code == 201
    data = response.json()
    assert "username" in data
    assert "email" in data
    assert "id" in data
    assert data["username"] == "testuser"
    assert data["email"] == "test@gmail.com"
    assert "password" not in data
    assert "hashed_password" not in data

@pytest.mark.asyncio
async def test_register_user_missing_fields():
    """Test registration with missing required fields"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/auth/register", json={
            "email": "test@gmail.com",
            "password": "123456"
        })
        assert response.status_code == 422  

        
        response = await ac.post("/api/auth/register", json={
            "username": "testuser",
            "password": "123456"
        })
        assert response.status_code == 422

       
        response = await ac.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@gmail.com"
        })
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_user_duplicate_username():
    """Test registration with duplicate username"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
       
        await ac.post("/api/auth/register", json={
            "username": "duplicateuser",
            "email": "test1@gmail.com",
            "password": "123456"
        })
        
        
        response = await ac.post("/api/auth/register", json={
            "username": "duplicateuser",
            "email": "test2@gmail.com",
            "password": "123456"
        })

    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_register_user_duplicate_email():
    """Test registration with duplicate email"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        await ac.post("/api/auth/register", json={
            "username": "user1",
            "email": "duplicate@gmail.com",
            "password": "123456"
        })
        
        
        response = await ac.post("/api/auth/register", json={
            "username": "user2",
            "email": "duplicate@gmail.com",
            "password": "123456"
        })

    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_register_user_invalid_email():
    """Test registration with invalid email format"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/auth/register", json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "123456"
        })

    assert response.status_code == 422  

@pytest.mark.asyncio
async def test_login_user_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
       
        await ac.post("/api/auth/register", json={
            "username": "loginuser",
            "email": "login@gmail.com",
            "password": "123456"
        })
        
        response = await ac.post("/api/auth/login", data={
            "username": "loginuser",
            "password": "123456"
        })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0  

@pytest.mark.asyncio
async def test_login_user_wrong_password():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Register first
        await ac.post("/api/auth/register", json={
            "username": "testuser",
            "email": "testlogin@gmail.com",
            "password": "correctpassword"
        })
        
        # Then login with wrong password
        response = await ac.post("/api/auth/login", data={
            "username": "testuser",
            "password": "wrongpassword"
        })

    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_user_nonexistent():
    """Test login with non-existent user"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/auth/login", data={
            "username": "nonexistent",
            "password": "123456"
        })

    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_user_missing_credentials():
    """Test login with missing credentials"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Missing username
        response = await ac.post("/api/auth/login", data={
            "password": "123456"
        })
        assert response.status_code == 422

        # Missing password
        response = await ac.post("/api/auth/login", data={
            "username": "testuser"
        })
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/sweets")

    assert response.status_code == 401  # Unauthorized
    assert "Not authenticated" in response.json()["detail"]

@pytest.mark.asyncio
async def test_protected_endpoint_with_valid_token():
    """Test accessing protected endpoint with valid token"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
      
        await ac.post("/api/auth/register", json={
            "username": "protecteduser",
            "email": "protected@gmail.com",
            "password": "123456"
        })
        
        login_response = await ac.post("/api/auth/login", data={
            "username": "protecteduser",
            "password": "123456"
        })
        
        token = login_response.json()["access_token"]
        
       
        response = await ac.get("/api/sweets", headers={
            "Authorization": f"Bearer {token}"
        })

 
    assert response.status_code != 401

@pytest.mark.asyncio
async def test_protected_endpoint_with_invalid_token():
    """Test accessing protected endpoint with invalid token"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/sweets", headers={
            "Authorization": "Bearer invalidtoken123"
        })

    assert response.status_code == 401  

@pytest.mark.asyncio
async def test_login_health_check():
    """Test login health check endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/auth/login")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

