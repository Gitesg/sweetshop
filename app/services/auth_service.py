from fastapi import HTTPException
import secrets


fake_users = []
user_id_counter = 1

class AuthService:
    def register_user(self, username: str, email: str, password: str):
        global user_id_counter

        
        for user in fake_users:
            if user["username"] == username:
                raise HTTPException(status_code=400, detail="Username already registered")
            if user["email"] == email:
                raise HTTPException(status_code=400, detail="Email already registered")

        new_user = {
            "id": user_id_counter,
            "username": username,
            "email": email,
            "password": password   # NOTE: plain for now, hash later
        }
        user_id_counter += 1
        fake_users.append(new_user)

        return new_user

    def login_user(self, username: str, password: str):
        for user in fake_users:
            if user["username"] == username and user["password"] == password:
                # Generate fake token
                token = secrets.token_hex(16)
                return {"access_token": token, "token_type": "bearer"}

        raise HTTPException(status_code=401, detail="Incorrect username or password")
