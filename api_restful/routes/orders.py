from fastapi import APIRouter, Depends, status, Query, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from api_restful.database import get_db
from api_restful.auth.dependencies import get_current_user
from api_restful.models import Orders, Products, Clients, OrdersProducts
from api_restful.schemas.orders import OrdersCreate, OrdersResponse, OrdersUpdate
from api_restful.docs.orders_docs import (
    get_orders_description,
    get_orders_responses,
    create_orders_description,
    create_orders_responses,
    get_order_description,
    get_order_responses,
    update_orders_description,
    update_orders_responses,
    delete_order_description,
    delete_order_responses
)
from api_restful.utils.enums import OrderStatus
from datetime import datetime

router = APIRouter()

@router.get(
    "/orders", 
    response_model=List[OrdersResponse],
    summary="Listar pedidos",
    status_code=status.HTTP_200_OK,
    description=get_orders_description,
    responses=get_orders_responses,
    tags=["Pedidos"]
)
def get_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    section: Optional[str] = Query(None),
    order_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    client_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    # Validação de datas
    date_format = "%Y-%m-%d"
    if start_date:
        try:
            datetime.strptime(start_date, date_format)
        except ValueError:
            raise HTTPException(
                status_code=400, detail="start_date deve estar no formato YYYY-MM-DD"
            )
    if end_date:
        try:
            datetime.strptime(end_date, date_format)
        except ValueError:
            raise HTTPException(
                status_code=400, detail="end_date deve estar no formato YYYY-MM-DD"
            )

    # Validação de section
    if section is not None and not section.strip():
        raise HTTPException(
            status_code=400, detail="section não pode ser uma string vazia"
        )

   # Validação de status
    if status is not None:
        valid_statuses = {s.value for s in OrderStatus}
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"status inválido. Valores permitidos: {', '.join(valid_statuses)}"
            )

    # Validação de IDs
    if order_id is not None and order_id < 1:
        raise HTTPException(
            status_code=400, detail="order_id deve ser maior que 0"
        )
    if client_id is not None and client_id < 1:
        raise HTTPException(
            status_code=400, detail="client_id deve ser maior que 0"
        )
    
    query = Orders.get_orders(
        db, 
        start_date, 
        end_date,
        section, 
        order_id,
        status,
        client_id,
    )

    orders = query.offset(skip).limit(limit).all()

    return orders

@router.post(
    "/orders", 
    response_model=OrdersResponse,
    summary="Criar pedido",
    status_code=status.HTTP_201_CREATED,
    description=create_orders_description,
    responses=create_orders_responses,
    tags=["Pedidos"]
)
def create_orders(
    order: OrdersCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user) 
):     

    client_found = Clients.get_client(db, order.client_id)

    if not client_found: 
        raise HTTPException(status_code=400, detail="Cliente não encontrado")
   
    order_created = Orders.create(
        db, 
        order,
    )

    return order_created

@router.get(
    "/orders/{id}", 
    response_model=OrdersResponse,
    summary="Buscar pedido por ID",
    status_code=status.HTTP_200_OK,
    description=get_order_description,
    responses=get_order_responses,
    tags=["Pedidos"]
)
def get_order(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    order_found = Orders.get_order(db, id)

    if not order_found: 
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    return order_found

@router.put(
    "/orders/{id}", 
    response_model=OrdersResponse, 
    status_code=status.HTTP_200_OK,
    summary="Atualizer pedido",
    description=update_orders_description,
    responses=update_orders_responses,
    tags=["Pedidos"]
)
def update_orders(
    id: int,
    order: OrdersUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  
):
    order_to_update = db.query(Orders).filter(Orders.id == id).first()

    if not order_to_update:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
    order_to_update = Orders.update(
        db, 
        id,
        order,
    )
    
    return order_to_update

@router.delete(
    "/orders/{id}", 
    response_model=OrdersResponse, 
    status_code=status.HTTP_200_OK,
    summary="Deletar pedido",
    description=delete_order_description,
    responses=delete_order_responses,
    tags=["Pedidos"]
)
def delete_order(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  
):
    order_to_delete = db.query(Orders).filter(Orders.id == id).first()

    if not order_to_delete:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
   
    order_to_delete = Orders.delete(
        db, 
        id,
    )
    
    return order_to_delete