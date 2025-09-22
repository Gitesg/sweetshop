from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.inventory_service import InventoryService
from app.schemas.inventory_schemas import InventoryUpdate, InventoryResponse

router = APIRouter(prefix="/api/inventory", tags=["inventory"])

@router.get("/", response_model=List[InventoryResponse])
def get_inventory(db: Session = Depends(get_db)):
    svc = InventoryService(db)
    return svc.get_inventory()

@router.put("/update", response_model=InventoryResponse)
def update_stock(payload: InventoryUpdate, db: Session = Depends(get_db)):
    svc = InventoryService(db)
    return svc.update_stock(payload.sweet_id, payload.quantity)

@router.post("/increase", response_model=InventoryResponse)
def increase_stock(payload: InventoryUpdate, db: Session = Depends(get_db)):
    svc = InventoryService(db)
    return svc.increase_stock(payload.sweet_id, payload.quantity)

@router.post("/decrease", response_model=InventoryResponse)
def decrease_stock(payload: InventoryUpdate, db: Session = Depends(get_db)):
    svc = InventoryService(db)
    return svc.decrease_stock(payload.sweet_id, payload.quantity)
