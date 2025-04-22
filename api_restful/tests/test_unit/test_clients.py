from fastapi import status
from api_restful.tests.factories.clients import ClientsFactory

# Teste GET /clients
def test_get_clients(client, token_pair_admin):
    response = client.get(
        "/api/v1/clients?limit=2&skip=0",
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

# Teste POST /clients (criação de cliente)
def test_create_client(client, db_session, token_pair, normal_user):
    new_client = ClientsFactory.build()  
    client_data = {
        "full_name": new_client.full_name,
        "email": new_client.email,
        "cpf": new_client.cpf,
    }

    response = client.post(
        "/api/v1/clients",
        json=client_data,
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["full_name"] == new_client.full_name
    assert response_data["email"] == new_client.email


# Teste GET /clients/{id}
def test_get_client_by_id(client, admin_user, token_pair_admin, db_session):
    client_db = ClientsFactory(user_id=admin_user.id)

    response = client.get(
        f"/api/v1/clients/{client_db.id}",
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == client_db.id


# Teste PUT /clients/{id}
def test_update_client(client, normal_user, token_pair, db_session):
    client_db = ClientsFactory(user_id=normal_user.id)

    update_data = {
        "full_name": "Cliente Atualizado",
        "email": "cliente@novoemail.com",
        "cpf": client_db.cpf, 
    }

    response = client.put(
        f"/api/v1/clients/{client_db.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )

    assert response.status_code == status.HTTP_200_OK
    updated_client = response.json()
    assert updated_client["email"] == update_data["email"]
    assert updated_client["full_name"] == update_data["full_name"]


# Teste DELETE /clients/{id}
def test_delete_client(client, admin_user, token_pair_admin, db_session):
    client_db = ClientsFactory(user_id=admin_user.id)

    response = client.delete(
        f"/api/v1/clients/{client_db.id}",
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == client_db.id

    # Tenta buscar o cliente deletado
    response = client.get(
        f"/api/v1/clients/{client_db.id}",
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Cliente não encontrado"