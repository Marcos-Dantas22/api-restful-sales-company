from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class ClientBase(BaseModel):
    full_name: str
    cpf: str
    gender: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int

    class Config:
        orm_mode = True
