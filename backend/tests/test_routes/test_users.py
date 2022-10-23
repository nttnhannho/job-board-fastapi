import json

from fastapi import status


def test_create_user(client):
    data = {
        "username": "test_user",
        "email": "test_email@test.com",
        "password": "test_password",
    }

    response = client.post("/users", data=json.dumps(data))

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "test_email@test.com"
    assert response.json()["is_active"] is True
