from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

client = MongoClient(MONGO_URI)
db = client["sweetsshop"]

# Collections defined at top-level
users_collection = db["user"]
sweet_collection = db["sweets"]
inventory_collection = db["inventory"]



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Auth DB
AUTH_DATABASE_URL = "postgresql://auth_user:auth_pass@localhost:5433/auth_db"
auth_engine = create_engine(AUTH_DATABASE_URL)
AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)
AuthBase = declarative_base()

def get_auth_db():
    db = AuthSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inventory DB
INVENTORY_DATABASE_URL = "postgresql://inventory_user:inventory_pass@localhost:5434/inventory_db"
inventory_engine = create_engine(INVENTORY_DATABASE_URL)
InventorySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=inventory_engine)
InventoryBase = declarative_base()

def get_inventory_db():
    db = InventorySessionLocal()
    try:
        yield db
    finally:
        db.close()
