from db.repository.users import create_new_user
from db.repository.users import get_user_by_email
from schemas.users import UserCreate
from sqlalchemy.orm import Session
from starlette.testclient import TestClient


def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {
        "username": email,
        "password": password,
    }

    r = client.post("/login/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    password = "random-password"
    user = get_user_by_email(email, db)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        create_new_user(user=user_in_create, db=db)

    return user_authentication_headers(client=client, email=email, password=password)
