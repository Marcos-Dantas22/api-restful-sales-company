from api_restful.tests.factories.products import ProductsFactory

def test_user_flow(client):
    # 1. Cadastro de novo usuário
    response = client.post("/api/v1/auth/register", json={
        "username": "flowuser",
        "password": "testpassword123"
    })
    assert response.status_code == 200

    # 2. Login
    response = client.post("/api/v1/auth/login", json={
        "username": "flowuser",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Criar cliente
    response = client.post("/api/v1/clients/", json={
        "full_name": "Cliente Fluxo",
        "email": "cliente@fluxo.com",
        "cpf": "99999999999"
    }, headers=headers)
    assert response.status_code == 201
    print(response.json())
    client_id = response.json()["id"]

    # 4. Criar produtos de exemplo usando a factory e o admin
    product = ProductsFactory.create(description="Descrição teste", price=150.0, initial_stock=10)
    
    # Como o admin cria o produto, o ID do produto é recuperado diretamente da factory
    product_id = product.id

    # 5. Criar pedido com o cliente e produto criados
    response = client.post("/api/v1/orders/", json={
        "client_id": client_id,
        "products": [
            {
                "product_id": product_id,
                "quantity": 2
            }
        ]
    }, headers=headers)
    assert response.status_code == 201
    assert response.json()["status"] in ["created", "success"]  
