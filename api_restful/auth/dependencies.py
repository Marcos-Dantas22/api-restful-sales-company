from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload  
