# tests/api/api_v1/test_auth.py
from fastapi import status

def test_register_user_success(client):
    response = client.post("api/v1/auth/register", json={
        "username": "test_user",
        "password": "normal_user12345"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "system_user_id" in data

def test_register_user_conflict(client, normal_user):
    response = client.post("api/v1/auth/register", json={
        "username": normal_user.username,
        "password": "normal_user12345"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username já cadastrado"

def test_login_success(client, normal_user):
    response = client.post("api/v1/auth/login", json={
        "username": normal_user.username,
        "password": "normal_user12345"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

def test_login_wrong_password(client, normal_user):
    response = client.post("api/v1/auth/login", json={
        "username": normal_user.username,
        "password": "wrongpass"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_refresh_token_success(client, normal_user, token_pair):
    response = client.post("api/v1/auth/refresh-token", json={
        "refresh_token": token_pair["refresh_token"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
