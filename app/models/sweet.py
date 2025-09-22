# app/db/models_inventory.py
from sqlalchemy import Column, Integer, String, Float
from app.db.database import InventoryBase

class Sweet(InventoryBase):
    __tablename__ = "sweets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
