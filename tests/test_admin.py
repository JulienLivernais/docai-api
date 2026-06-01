from fastapi.testclient import TestClient
from app.core.security import hash_password
from app.models.users import User
from tests.conftest import TestingSessionLocal


def register_and_login(client: TestClient, email: str, username: str) -> str:
    client.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": "test1234"
    })
    response = client.post("/auth/login", data={
        "username": email,
        "password": "test1234"
    })
    return response.json()["access_token"]


def create_admin(client: TestClient) -> str:
    db = TestingSessionLocal()
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hash_password("admin1234"),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    db.close()

    response = client.post("/auth/login", data={
        "username": "admin@example.com",
        "password": "admin1234"
    })
    return response.json()["access_token"]


def test_admin_list_users(client):
    admin_token = create_admin(client)
    register_and_login(client, "user@example.com", "regularuser")
    response = client.get("/admin/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_admin_get_user_by_id(client):
    admin_token = create_admin(client)
    client.post("/auth/register", json={
        "username": "findme",
        "email": "findme@example.com",
        "password": "test1234"
    })
    users = client.get("/admin/users", headers={"Authorization": f"Bearer {admin_token}"})
    user_id = users.json()[1]["id"]
    response = client.get(f"/admin/users/{user_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "findme@example.com"


def test_admin_get_user_by_email(client):
    admin_token = create_admin(client)
    client.post("/auth/register", json={
        "username": "byemail",
        "email": "byemail@example.com",
        "password": "test1234"
    })
    response = client.get("/admin/users/by-email", params={"email": "byemail@example.com"},
                          headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "byemail@example.com"


def test_admin_get_user_by_username(client):
    admin_token = create_admin(client)
    client.post("/auth/register", json={
        "username": "byusername",
        "email": "byusername@example.com",
        "password": "test1234"
    })
    response = client.get("/admin/users/by-username", params={"username": "byusername"},
                          headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "byusername"


def test_admin_delete_user(client):
    admin_token = create_admin(client)
    client.post("/auth/register", json={
        "username": "todelete",
        "email": "todelete@example.com",
        "password": "test1234"
    })
    users = client.get("/admin/users", headers={"Authorization": f"Bearer {admin_token}"})
    user_id = users.json()[1]["id"]
    response = client.delete(f"/admin/users/{user_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204


def test_regular_user_cannot_access_admin(client):
    token = register_and_login(client, "regular@example.com", "regularuser")
    response = client.get("/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

