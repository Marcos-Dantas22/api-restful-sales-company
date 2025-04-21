from pydantic import BaseModel, model_validator, field_validator
from typing import Optional, List, Dict, Any
from datetime import date
from api_restful.schemas.images import Images
from datetime import datetime
import json
class ProductsBase(BaseModel):
    description: str
    price: float
    barcode: str
    section: str
    initial_stock: int
    expiration_date: Optional[date] = None

    images: Optional[List[str]] = []
    

class ProductsCreate(ProductsBase):
    pass

class ProductHistoryResponse(BaseModel):
    id: int
    product_id: Optional[int]
    user_id: int
    action: str
    changed_fields: Dict[str, Any]
    timestamp: datetime

    @field_validator('changed_fields', mode='before')
    def parse_changed_fields(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return {}
        return v
    
    class Config:
        orm_mode = True

class ProductsResponse(BaseModel):
    id: int
    description: str
    price: float
    barcode: str
    section: str
    initial_stock: int
    expiration_date: Optional[date] = None

    images: List[Images] = [] 
    
    class Config:
        orm_mode = True
