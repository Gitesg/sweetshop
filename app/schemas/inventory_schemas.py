from pydantic import BaseModel

class InventoryUpdate(BaseModel):
    sweet_id: int
    quantity: int

class InventoryResponse(BaseModel):
    id: int
    name: str
    quantity: int

    class Config:
        from_attributes = True
