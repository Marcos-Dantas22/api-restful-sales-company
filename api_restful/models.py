from .utils.security import hash_password
from sqlalchemy import (
    Column, Integer, String, 
    Date, DateTime, Boolean, 
    ForeignKey, Numeric, Text, Table, Enum
)
from api_restful.utils.enums import GenderStatus, OrderStatus
from api_restful.schemas.clients import ClientCreate, ClientResponse
from api_restful.schemas.products import ProductsCreate
from api_restful.schemas.orders import OrdersCreate, OrdersUpdate
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from unidecode import unidecode
from sqlalchemy import func
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from fastapi import HTTPException
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True  
    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active  = Column(Boolean, default=True)

class SystemUser(BaseModel):
    __tablename__ = "system_users"    
    username = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

    @staticmethod
    def create(db: Session, username: str, password: str):
        hashed_pw = hash_password(password)
        user = SystemUser(username=username, password=hashed_pw)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(SystemUser).filter(SystemUser.username == username).first()

class Clients(BaseModel):
    __tablename__ = "clients"    
    user_id = Column(Integer, ForeignKey("system_users.id"), nullable=False)
    user = relationship("SystemUser", backref="clients")
    full_name = Column(String, nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    gender = Column(Enum(GenderStatus, name="genderstatus"))
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    birth_date = Column(Date)
    address = Column(String)
    city = Column(String)
    state = Column(String)

    orders = relationship("Orders", back_populates="client")

    @staticmethod
    def create(
        db: Session, 
        user_id: int,
        client: ClientCreate, 
    ):
        client_created = Clients(
            user_id = user_id,
            full_name = client.full_name, 
            cpf = client.cpf,
            gender = client.gender,
            email = client.email,
            phone = client.phone,
            birth_date = client.birth_date,
            address = client.address,
            city = client.city,
            state = client.state,
        )
        db.add(client_created)
        db.commit()
        db.refresh(client_created)
        
        return client_created
    
    @staticmethod
    def get_clients(db: Session, full_name: str, email: str):
        conditions = []

        if full_name:
            normalized_full_name = unidecode(full_name.lower())
            conditions.append(Clients.full_name.ilike(f"%{normalized_full_name}%"))

        
        if email:
            normalized_email = unidecode(email.lower())
            conditions.append(Clients.email.ilike(f"%{normalized_email}%"))


        query = db.query(Clients).filter(and_(*conditions))  

        return query
    
    @staticmethod
    def get_client(db: Session, id: int):
        return db.query(Clients).filter(Clients.id == id).first()

    
    @staticmethod
    def update(
        db: Session, 
        id: int,
        client: ClientCreate, 
    ):
        client_to_update = db.query(Clients).filter(Clients.id == id).first()

        client_to_update.full_name = client.full_name
        client_to_update.cpf = client.cpf
        client_to_update.gender = client.gender
        client_to_update.email = client.email
        client_to_update.phone = client.phone
        client_to_update.birth_date = client.birth_date
        client_to_update.address = client.address
        client_to_update.city = client.city
        client_to_update.state = client.state

       
        db.commit()
        db.refresh(client_to_update)
        
        return client_to_update
    
    @staticmethod
    def delete(db: Session, id: int):
        client_to_delete = db.query(Clients).filter(Clients.id == id).first()

        db.delete(client_to_delete)
        db.commit()

        return client_to_delete
    

class Products(BaseModel):
    __tablename__ = "products"    
    description = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  
    barcode = Column(String(50), unique=True, nullable=False)
    section = Column(String(100), nullable=False)
    initial_stock = Column(Integer, nullable=False)
    expiration_date = Column(Date, nullable=True)

    images = relationship("Images", back_populates="product", cascade="all, delete-orphan")

    product_orders = relationship("OrdersProducts", back_populates="product")

    @staticmethod
    def create(
        db: Session, 
        product: ProductsCreate, 
    ):
        product_created = Products(
            description = product.description, 
            price = product.price,
            section = product.section,
            barcode = product.barcode,
            initial_stock = product.initial_stock,
            expiration_date = product.expiration_date,
        )
            
        db.add(product_created)
        db.commit()
        db.refresh(product_created)

        if product.images: 
            for img in product.images:
                image = Images(
                    base64=img,
                    product_id=product_created.id
                )
                db.add(image)

            db.commit() 
        
        return product_created

    @staticmethod
    def get_products(
        db: Session, 
        category: str, 
        price_min: float,
        price_max: float,
        price: float,
        availability: int,
    ):
        conditions = []

        if category:
            normalized_category = unidecode(category.lower())
            conditions.append(Products.section.ilike(f"%{normalized_category}%"))

        if price_min is not None:
            conditions.append(Products.price >= price_min)

        if price_max is not None:
            conditions.append(Products.price <= price_max)

        if availability is not None:
            if availability == 1:
                conditions.append(Products.initial_stock > 0) 
            elif availability == 0:
                conditions.append(Products.initial_stock == 0)  

        if price is not None:
            conditions.append(Products.price == price)

        query = db.query(Products).filter(and_(*conditions))  

        return query

    @staticmethod
    def get_product(db: Session, id: int):
        return db.query(Products).filter(Products.id == id).first()
    
    @staticmethod
    def update(
        db: Session, 
        id: int,
        product: ProductsCreate, 
    ):
        product_to_update = db.query(Products).filter(Products.id == id).first()

        # Atualiza os campos básicos do produto
        product_to_update.description = product.description
        product_to_update.price = product.price
        product_to_update.section = product.section
        product_to_update.barcode = product.barcode
        product_to_update.initial_stock = product.initial_stock
        product_to_update.expiration_date = product.expiration_date

        db.commit()
        db.refresh(product_to_update)
       
        # Adiciona imagens novas (sem remover as antigas)
        if product.images:
            # Coleta base64 das imagens já salvas para esse produto
            existing_images = db.query(Images.base64).filter(Images.product_id == id).all()
            existing_base64_list = [img.base64 for img in existing_images]

            for img_base64 in product.images:
                if img_base64 not in existing_base64_list:
                    image = Images(
                        base64=img_base64,
                        product_id=id
                    )
                    db.add(image)

            db.commit()
        
        return product_to_update
    
    @staticmethod
    def delete(db: Session, id: int):
        product_to_delete = db.query(Products).filter(Products.id == id).first()

        db.delete(product_to_delete)
        db.commit()

        return product_to_delete

class Images(BaseModel):
    __tablename__ = 'images'

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    base64 = Column(Text, nullable=False)  

    product = relationship("Products", back_populates="images")


# Tabela associativa    
class OrdersProducts(Base):
    __tablename__ = 'orders_products'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)

    product_description = Column(String, nullable=False)
    product_price = Column(Numeric(10, 2), nullable=False)  
    product_barcode = Column(String(50), nullable=False)
    section = Column(String(100), nullable=False)
    product_actual_stock = Column(Integer, nullable=False)
    order_quantity = Column(Integer, nullable=False)

    order = relationship("Orders", back_populates="order_products")
    product = relationship("Products", back_populates="product_orders")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Orders(BaseModel):
    __tablename__ = 'orders'

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Clients", back_populates="orders")

    order_products = relationship("OrdersProducts", back_populates="order", cascade="all, delete-orphan")

    status = Column(Enum(OrderStatus), default=OrderStatus.created)

    @staticmethod
    def create(db: Session, order: OrdersCreate):
        new_order = Orders(client_id=order.client_id)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        for item in order.products:
            product = db.query(Products).filter_by(id=item.product_id).first()
            
            order_product = OrdersProducts(
                order_id=new_order.id,
                product_id=product.id,
                product_description=product.description,
                product_price=product.price,
                product_barcode=product.barcode,
                section=product.section,
                product_actual_stock=product.initial_stock,
                order_quantity=item.quantity
            )
            
            db.add(order_product)

            # Atualiza o estoque
            product.initial_stock -= item.quantity

        db.commit()
        return new_order 
    
    @staticmethod
    def get_orders(
        db: Session, 
        start_date: str, 
        end_date: str, 
        section: str,
        order_id: int,
        status: str,
        client_id: int,
    ):
        conditions = []

        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            conditions.append(Orders.created_at >= start)

        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            conditions.append(Orders.created_at <= end)

        if section:
            normalized_section = unidecode(section.lower())
            conditions.append(
                Products.section.ilike(f"%{normalized_section}%")
            )

        if order_id is not None:
            conditions.append(Orders.id == order_id)

        if client_id is not None:
            conditions.append(Orders.client_id == client_id)

        if status is not None:
            conditions.append(Orders.status == status)

        query = (
            db.query(Orders)
            .join(Orders.products)  
            .filter(and_(*conditions))
            .options(joinedload(Orders.products))  
        )
        return query
    
    @staticmethod
    def get_order(db: Session, id: int):
        return db.query(Orders).filter(Orders.id == id).first()

    
    @staticmethod
    def update(db: Session, order_id: int, update_data: OrdersUpdate):
        order = db.query(Orders).filter_by(id=order_id).first()

        # Atualizar status, se fornecido
        if update_data.status:
            order.status = update_data.status

        if update_data.products:
            for item in update_data.products:
                product = db.query(Products).filter_by(id=item.product_id).first()
                if not product:
                    raise HTTPException(status_code=404, detail=f"Produto ID {item.product_id} não encontrado")

                # Verifica se o produto já está no pedido
                existing = db.query(OrdersProducts).filter_by(order_id=order.id, product_id=item.product_id).first()

                if existing:
                    diff = item.quantity - existing.order_quantity

                    if diff != 0:
                        if diff > 0:
                            # Está tentando aumentar a quantidade
                            if product.initial_stock < diff:
                                raise HTTPException(
                                    status_code=400,
                                    detail=f"Estoque insuficiente para o produto {product.description}. Faltam {diff} unidades."
                                )
                            product.initial_stock -= diff
                        else:
                            # Está reduzindo a quantidade — devolve ao estoque
                            product.initial_stock += abs(diff)

                        existing.order_quantity = item.quantity
                else:
                    # Novo produto — adicionar ao pedido
                    if item.quantity > product.initial_stock:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Estoque insuficiente para o produto {product.description}. Disponível: {product.initial_stock}, Solicitado: {item.quantity}"
                        )

                    new_link = OrdersProducts(
                        order_id=order.id,
                        product_id=product.id,
                        product_description=product.description,
                        product_price=product.price,
                        product_barcode=product.barcode,
                        section=product.section,
                        product_actual_stock=product.initial_stock,
                        order_quantity=item.quantity
                    )

                    db.add(new_link)
                    product.initial_stock -= item.quantity

        db.commit()
        db.refresh(order)

        return order
    
    @staticmethod
    def delete(db: Session, id: int):
        order_to_delete = db.query(Orders).filter(Orders.id == id).first()

        db.delete(order_to_delete)
        db.commit()

        return order_to_delete