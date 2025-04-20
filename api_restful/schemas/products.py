from pydantic import BaseModel
from typing import Optional
from datetime import date
from api_restful.schemas.images import Images
from typing import List

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
