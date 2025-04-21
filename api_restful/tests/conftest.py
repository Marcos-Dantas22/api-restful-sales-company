import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api_restful.models import Base  
import os
from fastapi.testclient import TestClient
from api_restful.main import app
from api_restful.auth.dependencies import get_db
from api_restful.tests.factories.system_user import SystemUserFactory 
from dotenv import load_dotenv
import os
from api_restful.auth.auth import create_access_token

load_dotenv()

# Usar a variável de ambiente DATABASE_URL, se estiver configurada
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# Criar o engine com a URL configurada
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if TEST_DATABASE_URL.startswith("sqlite") else {}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_db_engine():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_db_engine):
    connection = test_db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # Injeta a sessão nas factories
    SystemUserFactory._meta.sqlalchemy_session = session
    
    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# Token se quiser testar endpoints protegidos
@pytest.fixture
def token_pair(client, normal_user):
    response = client.post("api/v1/auth/login", json={
        "username": normal_user.username,
        "password": "normal_user12345"
    })
    return response.json()

@pytest.fixture
def token_pair_admin(client, admin_user):
    response = client.post("/api/v1/auth/login", json={
        "username": admin_user.username,
        "password": 'adminadmin'
    })
    return response.json()

@pytest.fixture
def normal_user(db_session):
    user = SystemUserFactory(username="user1", password="normal_user12345", is_admin=False)
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def admin_user(db_session):
    user = SystemUserFactory(username="useradmin", is_admin=True, password="adminadmin")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def auth_headers(normal_user):
    token = create_access_token({"sub": normal_user.username})
    return {"Authorization": f"Bearer {token}"}
