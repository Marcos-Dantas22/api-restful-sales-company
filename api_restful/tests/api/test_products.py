import pytest
from fastapi.testclient import TestClient
from api_restful.main import app
from api_restful.models import Products, SystemUser, ProductHistory
from api_restful.schemas.products import ProductsCreate

client = TestClient(app)

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

def test_get_products(client, token_pair):
    response = client.get(
        "api/v1/products",
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product(client, token_pair_admin):
    product_data = {
        "description": "Produto Teste 2",
        "barcode": "3216549870000",
        "price": 59.99,
        "section": "Livros",
        "initial_stock": 10
    }
    response = client.post(
        "api/v1/products",
        json=product_data,
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    assert response.status_code == 201
    assert response.json()["description"] == product_data["description"]

def test_get_product_by_id(client, token_pair, create_product):
    response = client.get(
        f"api/v1/products/{create_product.id}",
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == create_product.id

def test_update_product(client, token_pair_admin, create_product):
    update_data = {
        "description": "Produto Atualizado",
        "barcode": "9998887776661",
        "price": 49.99,
        "section": "Games",
        "initial_stock": 12
    }
    response = client.put(
        f"api/v1/products/{create_product.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Produto Atualizado"

def test_delete_product(client, token_pair_admin, create_product):
    response = client.delete(
        f"api/v1/products/{create_product.id}",
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == create_product.id

def test_get_product_history(client, db_session, admin_user, token_pair_admin, create_product):
    import json
    created_product_info =  {
        "id": create_product.id,
        "description": create_product.description,
        "price": create_product.price,
        "section": create_product.section,
        "barcode": create_product.barcode,
        "initial_stock": create_product.initial_stock,
        "expiration_date": create_product.expiration_date,
    }
    # Convertendo o dicionário para uma string JSON
    created_product_info_json = json.dumps(created_product_info, default=str) 
    
    # Cria um histórico manualmente
    history = ProductHistory(
        product_id=create_product.id,
        user_id=admin_user.id,
        action="created",
        changed_fields=created_product_info_json,
    )
    db_session.add(history)
    db_session.commit()

    response = client.get(
        f"api/v1/products/{create_product.id}/history",
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)