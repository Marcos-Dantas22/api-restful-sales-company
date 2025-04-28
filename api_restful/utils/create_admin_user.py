# create_admin_user.py

from sqlalchemy.orm import Session
from api_restful.database import SessionLocal  # ajuste se o caminho for diferente
from api_restful.models import SystemUser

def main():
    db = SessionLocal()

    admin_username = "admin"
    admin_password = "admin123"  # Troque para uma senha segura no futuro

    existing_admin = db.query(SystemUser).filter_by(username=admin_username).first()

    if not existing_admin:
        SystemUser.create(db=db, username=admin_username, password=admin_password)
        print("✅ Usuário admin criado com sucesso!")
    else:
        print("ℹ️ Usuário admin já existe, não será recriado.")

if __name__ == "__main__":
    main()
