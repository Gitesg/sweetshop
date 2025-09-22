# app/routes/sweet_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_inventory_db
from app.services.sweet_service import SweetService
from app.schemas.sweets_schemas import SweetCreate, SweetUpdate, SweetResponse

router = APIRouter(prefix="/api/sweets", tags=["sweets"])

@router.post("/", response_model=SweetResponse, status_code=201)
def create_sweet(sweet: SweetCreate, db: Session = Depends(get_inventory_db)):
    service = SweetService(db)
    return service.create_sweet(sweet)

@router.get("/", response_model=List[SweetResponse])
def list_sweets(db: Session = Depends(get_inventory_db)):
    service = SweetService(db)
    return service.list_sweets()

@router.get("/{sweet_id}", response_model=SweetResponse)
def get_sweet(sweet_id: int, db: Session = Depends(get_inventory_db)):
    service = SweetService(db)
    sweet = service.get_sweet(sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return sweet

@router.put("/{sweet_id}", response_model=SweetResponse)
def update_sweet(sweet_id: int, sweet: SweetUpdate, db: Session = Depends(get_inventory_db)):
    service = SweetService(db)
    updated = service.update_sweet(sweet_id, sweet)
    if not updated:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return updated

@router.delete("/{sweet_id}", response_model=SweetResponse)
def delete_sweet(sweet_id: int, db: Session = Depends(get_inventory_db)):
    service = SweetService(db)
    deleted = service.delete_sweet(sweet_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return deleted
