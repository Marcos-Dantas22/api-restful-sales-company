from fastapi import APIRouter, Depends, status, Query, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from api_restful.database import get_db
from api_restful.auth.dependencies import get_current_user
from api_restful.models import Products
from api_restful.schemas.products import ProductsCreate, ProductsResponse
from api_restful.docs.products_docs import (
    get_products_description,
    get_products_responses,
    create_product_description,
    create_product_responses,
    get_product_description,
    get_product_responses,
    update_product_description,
    update_product_responses,
    delete_product_description,
    delete_product_responses
)
router = APIRouter()

@router.get(
    "/products", 
    response_model=List[ProductsResponse],
    summary="Listar produtos",
    status_code=status.HTTP_200_OK,
    description=get_products_description,
    responses=get_products_responses,
    tags=["Produtos"]
)
def get_products(
    category: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    price: Optional[float] = Query(None),
    availability: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    
    if price and (price_min or price_max):
        raise HTTPException(status_code=400, detail="Não é permitido usar o filtro 'price' junto com 'price_min' ou 'price_max'. Escolha apenas um conjunto de filtros de preço.")

    query = Products.get_products(
        db, 
        category, 
        price_min,
        price_max, 
        price,
        availability,
    )

    products = query.offset(skip).limit(limit).all()

    return products

@router.post(
    "/products", 
    response_model=ProductsResponse,
    summary="Criar produto",
    status_code=status.HTTP_201_CREATED,
    description=create_product_description,
    responses=create_product_responses,
    tags=["Produtos"]
)
def create_products(
    product: ProductsCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  
):
    
    existing_barcode = db.query(Products).filter(Products.barcode == product.barcode).first()
    if existing_barcode:
        raise HTTPException(status_code=400, detail="Codigo de barra já esta sendo utilizado")
    
    product_created = Products.create(
        db, 
        product,
    )

    return product_created

@router.get(
    "/products/{id}", 
    response_model=ProductsResponse,
    summary="Buscar produto por ID",
    status_code=status.HTTP_200_OK,
    description=get_product_description,
    responses=get_product_responses,
    tags=["Produtos"]
)
def get_product(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    product_found = Products.get_product(db, id)

    if not product_found: 
        raise HTTPException(status_code=400, detail="Produto não encontrado")

    return product_found

@router.put(
    "/products/{id}", 
    response_model=ProductsResponse, 
    status_code=status.HTTP_200_OK,
    summary="Atualizar produto",
    description=update_product_description,
    responses=update_product_responses,
    tags=["Produtos"],
)
def update_product(
    id: int,
    product: ProductsCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  
):
    product_to_update = db.query(Products).filter(Products.id == id).first()

    if not product_to_update:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    existing_barcode = db.query(Products).filter(
        Products.barcode == product.barcode, Products.id != id).first()
    
    if existing_barcode:
        raise HTTPException(status_code=400, detail="Codigo de barra já esta sendo utilizado")
   
    product_to_update = Products.update(
        db, 
        id,
        product,
    )
    
    return product_to_update

@router.delete(
    "/products/{id}", 
    response_model=ProductsResponse, 
    status_code=status.HTTP_200_OK,
    summary="Deletar produto",
    description=delete_product_description,
    responses=delete_product_responses,
    tags=["Produtos"],
)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  
):
    product_to_delete = db.query(Products).filter(Products.id == id).first()

    if not product_to_delete:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
   
    product_to_delete = Products.delete(
        db, 
        id,
    )
    
    return product_to_delete