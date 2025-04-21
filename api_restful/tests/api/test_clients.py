import pytest
from fastapi import status
from api_restful.models import Clients, SystemUser
from api_restful.schemas.clients import ClientCreate

@pytest.fixture
def client_data():
    return {
        "full_name": "Cliente Teste",
        "email": "teste@cliente.com",
        "cpf": "12345678900",
    }

@pytest.fixture
def new_client(client_data):
    return ClientCreate(**client_data)

# Teste GET /clients
def test_get_clients(client, token_pair_admin):
    response = client.get(
        "/api/v1/clients?limit=2&skip=0", 
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Espera uma lista de clientes

# Teste POST /clients (criação de cliente)
def test_create_client(client, new_client, token_pair):
    response = client.post(
        "/api/v1/clients", 
        json=new_client.dict(), 
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    client_data = response.json()
    assert client_data["full_name"] == new_client.full_name
    assert client_data["email"] == new_client.email
    assert client_data["cpf"] == new_client.cpf

# Teste GET /clients/{id} (buscar cliente por ID)
def test_get_client_by_id(client, admin_user, token_pair_admin, db_session):
    response = client.post("/api/v1/auth/login", json={
        "username": admin_user.username,
        "password": 'adminadmin'
    })
    token_pair_admin = response.json()

    # Cria cliente para o teste
    client_data = ClientCreate(full_name="Teste", email="teste@cliente.com", cpf="12345678901")
    client_db = Clients.create(db_session, admin_user.id, client_data)

    # Faz requisição autenticada
    response = client.get(
        f"api/v1/clients/{client_db.id}", 
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == client_db.id

# Teste PUT /clients/{id} (atualizar cliente)
def test_update_client(client, normal_user, token_pair, db_session):
    # Criando cliente para atualizar
    client_data = ClientCreate(full_name="Cliente", email="cliente@gmail.com", cpf="12345678901")
    client_db = Clients.create(db_session, normal_user.id, client_data)
    
    update_data = {"full_name": "Cliente Atualizado", "email": "cliente@novoemail.com", "cpf": "12345678901"}
    response = client.put(
        f"/api/v1/clients/{client_db.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    updated_client = response.json()
    assert updated_client["email"] == update_data["email"]
    assert updated_client["full_name"] == update_data["full_name"]

# Teste DELETE /clients/{id} (deletar cliente)
def test_delete_client(client, admin_user, token_pair_admin, db_session):
    # Criando cliente para deletar
    client_data = ClientCreate(full_name="Cliente Para Deletar", email="delete@cliente.com", cpf="12345678902")
    client_db = Clients.create(db_session, admin_user.id, client_data)
    
    response = client.delete(
        f"/api/v1/clients/{client_db.id}",
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    deleted_client = response.json()
    assert deleted_client["id"] == client_db.id
    
    # Verifica se o cliente foi realmente deletado
    response = client.get(
        f"/api/v1/clients/{client_db.id}",
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST  # Cliente não encontrado
    assert response.json()["detail"] == "Cliente não encontrado"
