from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Token de renovação JWT")

class RefreshTokenResponse(BaseModel):
    message: str
    access_token: str

class RegisterCreate(BaseModel):
    username: str
    password: str

class RegisterResponse(BaseModel):
    message: str
    system_user_id: int