from pydantic import BaseModel, EmailStr, model_validator, field_validator
from typing import Optional
from datetime import date
from api_restful.utils.enums import GenderStatus

# Função para formatar o telefone
def format_phone(phone: Optional[str]) -> Optional[str]:
    if phone:
        phone = ''.join(filter(str.isdigit, phone)) 
        if len(phone) == 11:
            return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
        else:
            raise ValueError("Telefone inválido. Deve ter 11 dígitos.")
    return phone 

def format_cpf(cpf: Optional[str]) -> Optional[str]:
    if cpf:
        cpf = ''.join(filter(str.isdigit, cpf)) 
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        else:
            raise ValueError("CPF inválido. Deve ter 11 dígitos.")
    return cpf

class ClientBase(BaseModel):
    full_name: str
    cpf: str
    gender: Optional[GenderStatus] = None
    email: EmailStr
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    
    @field_validator('cpf')
    def validate_cpf(cls, v):
        if v:
            # Chama a função para formatar e validar o CPF
            return format_cpf(v)
        raise ValueError("CPF é obrigatório")

    @field_validator('phone')
    def validate_phone(cls, v):
        if v:
            # Chama a função para formatar e validar o telefone
            return format_phone(v)
        return v  # Não obriga o telefone, mas valida se fornecido

    @field_validator('email')
    def validate_email(cls, v):
        if not v:
            raise ValueError("Email é obrigatório")
        return v

class ClientCreate(ClientBase):
    pass

class ClientResponse(BaseModel):
    id: int
    full_name: str
    cpf: str
    gender: Optional[str] = "Não informado"
    email: EmailStr
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

    @model_validator(mode='before')
    def set_default_values(cls, values):
        # # Definir valores padrão para campos opcionais
        if values.phone is None:
            values.phone = "Não informado"
        if values.address is None:
            values.address = "Não informado"
        if values.city is None:
            values.city = "Não informado"
        if values.state is None:
            values.state = "Não informado"

        else:
            gender_translation = {
                "male": "Masculino",
                "female": "Feminino",
                "other": "Outro"
            }
            values.gender = gender_translation[values.gender]
        
        return values
    
    class Config:
        orm_mode = True

