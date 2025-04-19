from fastapi import APIRouter, Depends, status, Query, Form, HTTPException
from api_restful.models import SystemUser
from typing import Optional, List
from sqlalchemy.orm import Session
from api_restful.database import get_db
from api_restful.auth.dependencies import get_current_user
from api_restful.models import Orders, Products, Clients
from api_restful.schemas.orders import OrdersCreate, OrdersResponse, OrdersUpdate

router = APIRouter()

@router.get("/orders", response_model=List[OrdersResponse])
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

@router.post("/orders", response_model=OrdersResponse)
def create_orders(
    order: OrdersCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  
):     

    client_found = Clients.get_client(db, order.client_id)

    if not client_found: 
        raise HTTPException(status_code=400, detail="Cliente não encontrado")

    for item in order.products:
        product_id = item.product_id
        quantity = item.quantity

        product = db.query(Products).filter_by(id=product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto com ID {product_id} não encontrado.")

        if product.initial_stock < quantity:
            raise HTTPException(status_code=404, detail=f"Estoque insuficiente para o produto '{product.description}'. Quantidade solicitada: {quantity}, disponível: {product.initial_stock}.")

    order_created = Orders.create(
        db, 
        order,
    )

    return order_created

@router.get("/orders/{id}", response_model=OrdersResponse)
def get_order(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    order_found = Orders.get_order(db, id)

    if not order_found: 
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    return order_found

@router.put("/orders/{id}", response_model=OrdersResponse, status_code=status.HTTP_200_OK)
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

@router.delete("/orders/{id}", response_model=OrdersResponse, status_code=status.HTTP_200_OK)
def delete_order(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  
):
    order_to_delete = db.query(Orders).filter(Orders.id == id).first()

    if not order_to_delete:
        raise HTTPException(status_code=404, detail="Orders não encontrado")
   
    order_to_delete = Orders.delete(
        db, 
        id,
    )
    
    return order_to_delete