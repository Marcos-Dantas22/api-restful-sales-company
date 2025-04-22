from api_restful.tests.factories.products import ProductsFactory, ProductHistoryFactory

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

def test_get_product_by_id(client, token_pair, db_session):
    product = ProductsFactory()
    db_session.add(product)
    db_session.commit()

    response = client.get(
        f"api/v1/products/{product.id}",
        headers={"Authorization": f"Bearer {token_pair['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == product.id

def test_update_product(client, token_pair_admin, db_session):
    product = ProductsFactory()
    db_session.add(product)
    db_session.commit()

    update_data = {
        "description": "Produto Atualizado",
        "barcode": "9998887776661",
        "price": 49.99,
        "section": "Games",
        "initial_stock": 12
    }
    response = client.put(
        f"api/v1/products/{product.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Produto Atualizado"

def test_delete_product(client, token_pair_admin, db_session):
    product = ProductsFactory()
    db_session.add(product)
    db_session.commit()

    response = client.delete(
        f"api/v1/products/{product.id}",
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == product.id

def test_get_product_history(client, db_session, admin_user, token_pair_admin):
    import json

    product = ProductsFactory()
    db_session.add(product)
    db_session.commit()

    created_product_info = {
        "id": product.id,
        "description": product.description,
        "price": product.price,
        "section": product.section,
        "barcode": product.barcode,
        "initial_stock": product.initial_stock,
        "expiration_date": product.expiration_date,
    }

    created_product_info_json = json.dumps(created_product_info, default=str)

    ProductHistoryFactory(
        product_id=product.id,
        user_id=admin_user.id,
        action="created",
        changed_fields=created_product_info_json,
    )

    response = client.get(
        f"api/v1/products/{product.id}/history",
        headers={"Authorization": f"Bearer {token_pair_admin['access_token']}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
