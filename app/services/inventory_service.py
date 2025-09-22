from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db import models

class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_inventory(self):
        return self.db.query(models.Sweet).all()

    def update_stock(self, sweet_id: int, qty: int):
        sweet = self.db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
        if not sweet:
            raise HTTPException(status_code=404, detail="Sweet not found")
        sweet.quantity = qty
        self.db.commit()
        self.db.refresh(sweet)
        return sweet

    def increase_stock(self, sweet_id: int, qty: int):
        sweet = self.db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
        if not sweet:
            raise HTTPException(status_code=404, detail="Sweet not found")
        sweet.quantity += qty
        self.db.commit()
        self.db.refresh(sweet)
        return sweet

    def decrease_stock(self, sweet_id: int, qty: int):
        sweet = self.db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
        if not sweet:
            raise HTTPException(status_code=404, detail="Sweet not found")
        if sweet.quantity < qty:
            raise HTTPException(status_code=400, detail="Not enough stock available")
        sweet.quantity -= qty
        self.db.commit()
        self.db.refresh(sweet)
        return sweet
