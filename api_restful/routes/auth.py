from fastapi import APIRouter, Depends, status, Form, HTTPException, Body
from api_restful.models import SystemUser
from sqlalchemy.orm import Session
from api_restful.database import get_db
from api_restful.auth.auth import create_access_token, decode_token, create_refresh_token
from api_restful.utils.security import verify_password
from api_restful.docs.auth_docs import (
    login_description,
    login_responses,
    register_description,
    register_responses,
    refresh_token_description,
    refresh_token_responses,
    register_admin_description,
    register_admin_responses,
)
from api_restful.schemas.auth import (
    TokenResponse, LoginRequest, 
    RegisterResponse, RegisterCreate,
    RefreshTokenRequest, RefreshTokenResponse
)
from jose import JWTError
from api_restful.auth.dependencies import admin_required

router = APIRouter()

@router.post(
    "/auth/login", 
    summary="Login de usuário",
    response_model=TokenResponse,
    description=login_description,
    status_code=status.HTTP_200_OK,
    responses=login_responses,
    tags=["Autenticação"]
)
def auth_login(
    credentials: LoginRequest = Body(...),
    db: Session = Depends(get_db), 
):
    db_user = SystemUser.get_user_by_username(db,credentials.username)

    if not db_user:
        raise HTTPException(
            status_code=404, detail="Usuário não encontrado"
        )

    if not verify_password(credentials.password, db_user.password):
        raise HTTPException(
            status_code=404, detail="Senha incorreta"
        )
    
    
    access_token = create_access_token(data={"sub": credentials.username})
    refresh_token = create_refresh_token(data={"sub": credentials.username})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    

@router.post(
    "/auth/register", 
    summary="Registro de usuário",
    response_model=RegisterResponse,
    description=register_description,
    status_code=status.HTTP_200_OK,
    responses=register_responses,
    tags=["Autenticação"]
)
def auth_register(
    register: RegisterCreate = Body(...),
    db: Session = Depends(get_db), 
):
    db_user = db.query(SystemUser).filter(SystemUser.username == register.username).first()
    
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username já cadastrado"
        )

    system_user = SystemUser.create(db=db, username=register.username, password=register.password)
    return {"message": "Usuario criado com sucesso", "system_user_id": system_user.id}

@router.post(
    "/auth/refresh-token" , 
    summary="Gerar novo token de acesso",
    description=refresh_token_description,
    responses=refresh_token_responses,
    response_model=RefreshTokenResponse,
    tags=["Autenticação"]
)
def auth_refresh_access_token(payload: RefreshTokenRequest):
    try:
        payload_data = decode_token(payload.refresh_token)
        username = payload_data.get("sub")
        if not username:
            raise HTTPException(
                status_code=401, detail="Token inválido"
            )
            

        new_token = create_access_token(data={"sub": username})
        return {
            "message": "Novo token gerado com sucesso",
            "access_token": new_token
        }

    except JWTError:
        raise HTTPException(
            status_code=401, detail="Refresh token inválido ou expirado"
        )
    

@router.post(
    "/auth/register-admin", 
    summary="Registro de usuário admin",
    response_model=RegisterResponse,
    description=register_admin_description,
    status_code=status.HTTP_200_OK,
    responses=register_admin_responses,
    tags=["Autenticação"]
)
def auth_register_admin(
    register: RegisterCreate = Body(...),
    db: Session = Depends(get_db), 
    user: dict = Depends(admin_required),  
):
    db_user = db.query(SystemUser).filter(SystemUser.username == register.username).first()
    
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username já cadastrado"
        )

    system_user = SystemUser.create_admin(db=db, username=register.username, password=register.password)
    return {"message": "Usuario Admin criado com sucesso", "system_user_id": system_user.id}