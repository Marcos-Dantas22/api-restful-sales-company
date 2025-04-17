from fastapi import FastAPI, APIRouter, Depends, status, Form, HTTPException
from .models import SystemUser
from sqlalchemy.orm import Session
from .database import get_db
from .auth.dependencies import get_current_user
from .auth.auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from .utils.security import verify_password

router = APIRouter()

@router.post("/auth/login")
def auth_login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db), 
    status_code=status.HTTP_200_OK
):
    db_user = SystemUser.get_user_by_username(db,form_data.username)

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=404, detail="Senha incorreta")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

    

@router.post("/auth/register")
def auth_register(
    username: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db), 
    status_code=status.HTTP_201_CREATED
):
    system_user = SystemUser.create_user(db=db, username=username, password=password)
    return {"message": "Usuario criado com sucesso", "system_user_id": system_user.id}

@router.post("/auth/refresh-token")
def auth_refresh_token(
    username: str = Form(...), 
    db: Session = Depends(get_db), 
    status_code=status.HTTP_201_CREATED
):
    user = SystemUser.get_user_by_username(db, username)
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    access_token = create_access_token(data={"sub": user.username})
    
    return {"message": "Token gerado com sucesso", "access_token": access_token}

# @router.get("/test")
# def protected_route(user: dict = Depends(get_current_user)):
#     return {"message": "Você está autenticado!", "user": user}

app = FastAPI()
app.include_router(router, prefix="/api/v1")