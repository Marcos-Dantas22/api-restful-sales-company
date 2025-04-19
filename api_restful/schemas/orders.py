from pydantic import BaseModel, Field
from typing import List
from api_restful.schemas.clients import ClientResponse
from api_restful.schemas.products import ProductsResponse
from api_restful.utils.enums import OrderStatus
from typing import Optional

class OrdersProductData(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantidade deve ser maior que zero")

class OrdersCreate(BaseModel):
    client_id: int
    products: List[OrdersProductData]

class OrdersUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    products: Optional[List[OrdersProductData]] = None

class OrdersResponse(BaseModel):
    id: int
    client_id: int  
    products: List[ProductsResponse]
    status: OrderStatus

    class Config:
        orm_mode = True
        use_enum_values = True 