from .utils.security import hash_password

from sqlalchemy import Column, Integer, String, Boolean
from .database import Base
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class SystemUser(Base):
    __tablename__ = "users"    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

    @staticmethod
    def create_user(db: Session, username: str, password: str):
        hashed_pw = hash_password(password)
        user = SystemUser(username=username, password=hashed_pw)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(SystemUser).filter(SystemUser.username == username).first()