from fastapi import APIRouter, Depends, status, Query, HTTPException
from api_restful.models import SystemUser
from typing import Optional, List
from sqlalchemy.orm import Session
from api_restful.database import get_db
from api_restful.auth.dependencies import get_current_user
from api_restful.models import Clients
from api_restful.schemas.clients import ClientCreate, ClientResponse
from api_restful.docs.clients_docs import (
    get_clients_description,
    get_clients_responses,
    create_client_description,
    create_client_responses,
    get_client_description,
    get_client_responses,
    update_client_description,
    update_client_responses,
    delete_client_description,
    delete_client_responses
)
import re
router = APIRouter()

@router.get(
    "/clients", 
    response_model=List[ClientResponse],
    summary="Listar clientes",
    description=get_clients_description,
    status_code=status.HTTP_200_OK, 
    responses=get_clients_responses,
    tags=["Clientes"]
)
def get_clients(
    full_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    if email is not None:
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise HTTPException(
                status_code=400, detail="O campo email deve conter um e-mail válido"
            )
    
    query = Clients.get_clients(db, full_name, email)

    clients = query.offset(skip).limit(limit).all()

    return clients

@router.post(
    "/clients", 
    response_model=ClientResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Criar cliente",
    description=create_client_description,
    responses=create_client_responses,
    tags=["Clientes"]
)
def create_clients(
    client: ClientCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  
):
    existing_cpf = db.query(Clients).filter(Clients.cpf == client.cpf).first()
    if existing_cpf:
        raise HTTPException(status_code=400, detail="CPF já está em uso")

    existing_email = db.query(Clients).filter(Clients.email == client.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email  já está em uso")
    
    system_user = SystemUser.get_user_by_username(db, user['username'])

    client_created = Clients.create(
        db, 
        system_user.id,
        client,
    )

    return client_created

@router.get(
    "/clients/{id}", 
    response_model=ClientResponse,
    summary="Buscar cliente por ID",
    description=get_client_description,
    responses=get_client_responses,
    tags=["Clientes"]
)
def get_client(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    client_found = Clients.get_client(db, id)

    if not client_found: 
        raise HTTPException(status_code=400, detail="Cliente não encontrado")

    return client_found


@router.put(
    "/clients/{id}", 
    response_model=ClientResponse, 
    status_code=status.HTTP_200_OK,
    summary="Atualizar cliente",
    description=update_client_description,
    responses=update_client_responses,
    tags=["Clientes"]
)
def update_clients(
    id: int,
    client: ClientCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  
):
    client_to_update = db.query(Clients).filter(Clients.id == id).first()

    if not client_to_update:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    existing_cpf = db.query(Clients).filter(
        Clients.cpf == client.cpf, Clients.id != id).first()
    if existing_cpf:
        raise HTTPException(status_code=400, detail="CPF já está em uso")

    existing_email = db.query(Clients).filter(
        Clients.email == client.email, Clients.id != id).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email  já está em uso")
    
    client_to_update = Clients.update(
        db, 
        id,
        client,
    )
    
    return client_to_update


@router.delete(
    "/clients/{id}", 
    response_model=ClientResponse, 
    status_code=status.HTTP_200_OK,
    summary="Deletar cliente",
    description=delete_client_description,
    responses=delete_client_responses,
    tags=["Clientes"]
)
def delete_client(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  
):
    client_to_delete = db.query(Clients).filter(Clients.id == id).first()

    if not client_to_delete:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
   
    client_to_delete = Clients.delete(
        db, 
        id,
    )
    
    return client_to_delete