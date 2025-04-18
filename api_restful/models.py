from .utils.security import hash_password

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from api_restful.schemas.clients import ClientCreate

class BaseModel(Base):
    __abstract__ = True  
    id         = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active  = Column(Boolean, default=True)

class SystemUser(BaseModel):
    __tablename__ = "system_users"    
    username = Column(String)
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
    gender = Column(String(1)) # F or M
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    birth_date = Column(Date)
    address = Column(String)
    city = Column(String)
    state = Column(String)

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
        if full_name and email:
            return db.query(Clients).filter(
                Clients.full_name == full_name,
                Clients.email == email
            )
        
        if full_name:
            return db.query(Clients).filter(
                Clients.full_name == full_name,
            )
        
        if email:
            return db.query(Clients).filter(
                Clients.email == email,
            )
        
        return db.query(Clients)
    
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