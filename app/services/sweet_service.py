# app/services/sweet_service.py
from sqlalchemy.orm import Session
from app.db.models_inventory import Sweet
from app.schemas.sweet_schemas import SweetCreate, SweetUpdate

class SweetService:
    def __init__(self, db: Session):
        self.db = db

    def create_sweet(self, sweet: SweetCreate):
        new_sweet = Sweet(**sweet.dict())
        self.db.add(new_sweet)
        self.db.commit()
        self.db.refresh(new_sweet)
        return new_sweet

    def list_sweets(self):
        return self.db.query(Sweet).all()

    def get_sweet(self, sweet_id: int):
        return self.db.query(Sweet).filter(Sweet.id == sweet_id).first()

    def update_sweet(self, sweet_id: int, sweet: SweetUpdate):
        db_sweet = self.get_sweet(sweet_id)
        if not db_sweet:
            return None
        for field, value in sweet.dict(exclude_unset=True).items():
            setattr(db_sweet, field, value)
        self.db.commit()
        self.db.refresh(db_sweet)
        return db_sweet

    def delete_sweet(self, sweet_id: int):
        db_sweet = self.get_sweet(sweet_id)
        if not db_sweet:
            return None
        self.db.delete(db_sweet)
        self.db.commit()
        return db_sweet
