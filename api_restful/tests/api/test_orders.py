import pytest
from fastapi.testclient import TestClient
from api_restful.main import app
from api_restful.models import Orders, Clients, Products
from api_restful.schemas.orders import OrdersCreate, OrdersProductData
from datetime import datetime
from api_restful.schemas.products import ProductsCreate
from api_restful.schemas.clients import ClientCreate

client = TestClient(app)

@pytest.fixture
def create_client(db_session, admin_user):
    # Cria cliente para o teste
    client_data = ClientCreate(full_name="Cliente Teste", email="cliente@teste.com", cpf="12345678900")
    client_db = Clients.create(db_session, admin_user.id, client_data)
    return client_db

@pytest.fixture
def create_product(db_session, admin_user):
    product_data = ProductsCreate(
        description="Produto Teste",
        barcode="1234567890123",
        price=99.99,
        section="Eletrônicos",
        initial_stock=10
    )
    product = Products.create(db_session, admin_user.id, product_data)
    return product

@pytest.fixture
def create_order(db_session, create_client, create_product):
    order_data = OrdersCreate(
        client_id=create_client.id,
        products=[
            OrdersProductData(product_id=create_product.id, quantity=2),
            OrdersProductData(product_id=create_product.id, quantity=5)
        ]
    )
    order = Orders.create(db_session, order_data)
    return order

def test_get_orders(client, token_pair):
    response = client.get(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_order(client, token_pair, create_client, create_product):
    order_data = {
        "client_id": create_client.id,
        "products": [
            {
                "product_id": create_product.id,
                "quantity": 2,
            },
            {
                "product_id": create_product.id,
                "quantity": 5,
            }
        ]
    }
    response = client.post(
        "/api/v1/orders",
        json=order_data,
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 201
    assert response.json()["client_id"] == create_client.id
    assert create_product.initial_stock == 3

def test_get_order_by_id(client, token_pair, create_order):
    response = client.get(
        f"/api/v1/orders/{create_order.id}",
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == create_order.id

def test_update_order(client, token_pair, create_order):
    update_data = {
        "client_id": 1,
        "status": "completed",
        "products": [
        ]
    }
    response = client.put(
        f"/api/v1/orders/{create_order.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

def test_delete_order(client, token_pair, create_order):
    response = client.delete(
        f"/api/v1/orders/{create_order.id}",
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == create_order.id
