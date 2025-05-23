from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from api_restful.auth.auth import decode_token 
from jose import JWTError
from fastapi import Request, HTTPException
from api_restful.models import SystemUser
from api_restful.database import get_db
from sqlalchemy.orm import Session
class CustomHTTPBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=False) 

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)

        if credentials is None:
            raise HTTPException(
                status_code=401,
                detail="Token de autenticação não fornecido",
            )

        if credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=403,
                detail="Esquema de autenticação inválido. Use 'Bearer'.",
            )

        return credentials
    
oauth2_scheme = CustomHTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


def admin_required(
    db: Session = Depends(get_db), 
    user: dict = Depends(get_current_user)
):
    system_user = db.query(SystemUser).filter(SystemUser.username == user["username"]).first()
    
    if not system_user or not system_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para administradores."
        )
    
    return user