# import jwt
# from datetime import datetime, timedelta
# from fastapi import HTTPException
# from bson import ObjectId
# from passlib.context import CryptContext
# from app.db.database import users_collection
# import os
# from dotenv import load_dotenv
# import logging


# load_dotenv()

# SECRET_KEY=os.getenv("SECRET_KEY")
# ALGORITHM=os.getenv("ALGORITHM")        
# ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class AuthService:
#     def register_user(self, username: str, email: str, password: str):
#         if users_collection.find_one({"username": username}):
#             raise HTTPException(status_code=400, detail="Username already registered")
        
#         if users_collection.find_one({"email": email}):
#             raise HTTPException(status_code=400, detail="Email already registered")

#         hashed_password = pwd_context.hash(password)
#         print(f"Hashed password: {hashed_password}")

#         print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")


#         new_user = {
#             "username": username,
#             "email": email,
#             "password": hashed_password
#         }
#         result = users_collection.insert_one(new_user)
#         print(result.inserted_id)

#         return {"id": str(result.inserted_id), "username": username, "email": email}

#     def login_user(self, username: str, password: str):
#         user = users_collection.find_one({"username": username})
#         if not user or not pwd_context.verify(password, user["password"]):
#             raise HTTPException(status_code=401, detail="Incorrect username or password")

#         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         payload = {
#             "sub": str(user["_id"]),
#             "username": user["username"],
#             "exp": expire
#         }
#         token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#         return {"access_token": token, "token_type": "bearer"}
import psycopg2
from pymongo import MongoClient

# ----------------------------
# Postgres: Auth DB
# ----------------------------
try:
    auth_conn = psycopg2.connect(
        dbname="auth_db",
        user="auth_user",
        password="auth_pass",
        host="localhost",
        port=5433,
        sslmode="disable"
    )
    print("✅ Connected to Auth DB")
except Exception as e:
    print("❌ Auth DB connection failed:", e)
    auth_conn = None

# ----------------------------
# Postgres: Inventory DB
# ----------------------------
try:
    inventory_conn = psycopg2.connect(
        dbname="inventory_db",
        user="inventory_user",
        password="inventory_pass",
        host="localhost",
        port=5434,
        sslmode="disable"
    )
    print("✅ Connected to Inventory DB")
except Exception as e:
    print("❌ Inventory DB connection failed:", e)
    inventory_conn = None

# ----------------------------
# MongoDB
# ----------------------------
try:
    mongo_client = MongoClient(
        "mongodb://mongo_user:mongo_pass@localhost:27018/?authSource=admin"
    )
    db_list = mongo_client.list_database_names()
    print("✅ Connected to MongoDB, databases:", db_list)
except Exception as e:
    print("❌ MongoDB connection failed:", e)
    mongo_client = None

# ----------------------------
# Cleanup
# ----------------------------
if auth_conn:
    auth_conn.close()
if inventory_conn:
    inventory_conn.close()
if mongo_client:
    mongo_client.close()






# pick your db



