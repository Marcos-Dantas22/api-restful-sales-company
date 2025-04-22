# tests/routes/test_orders.py
from api_restful.tests.factories.clients import ClientsFactory
from api_restful.tests.factories.products import ProductsFactory
from api_restful.tests.factories.orders import OrdersFactory


def test_get_orders(client, token_pair):
    response = client.get(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_order(client, token_pair, db_session):
    create_client = ClientsFactory()
    create_product = ProductsFactory(initial_stock=10)
    
    order_data = {
        "client_id": create_client.id,
        "products": [
            {"product_id": create_product.id, "quantity": 2},
            {"product_id": create_product.id, "quantity": 5}
        ]
    }

    response = client.post(
        "/api/v1/orders",
        json=order_data,
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["client_id"] == create_client.id

    db_session.refresh(create_product)
    assert create_product.initial_stock == 3  

def test_get_order_by_id(client, token_pair):
    order = OrdersFactory()
    
    response = client.get(
        f"/api/v1/orders/{order.id}",
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == order.id

def test_update_order(client, token_pair):
    order = OrdersFactory()
    
    update_data = {
        "client_id": order.client_id,
        "status": "completed",
        "products": []
    }
    
    response = client.put(
        f"/api/v1/orders/{order.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

def test_delete_order(client, token_pair):
    order = OrdersFactory()
    
    response = client.delete(
        f"/api/v1/orders/{order.id}",
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == order.id
