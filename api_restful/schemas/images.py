from pydantic import BaseModel

class Images(BaseModel):
    id: int
    base64: str

    class Config:
        orm_mode = True
