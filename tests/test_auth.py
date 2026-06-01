
def test_register(client):
    response = client.post("/auth/register", json={
        "username": "tester",
        "email": "test@example.com",
        "password": "test1234"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "duplicate@example.com",
        "password": "test1234"
    })
    response = client.post("/auth/register", json={
        "username": "testuser2",
        "email": "duplicate@example.com",
        "password": "test1234"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_register_duplicate_username(client):
    client.post("/auth/register", json={
        "username": "tester",
        "email": "first@example.com",
        "password": "test1234"
    })
    response = client.post("/auth/register", json={
        "username": "tester",
        "email": "second@example.com",
        "password": "test1234"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"


def test_login(client):
    client.post("/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "test1234"
    })
    response = client.post("/auth/login", data={
        "username": "login@example.com",
        "password": "test1234"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    response = client.post("/auth/login", data={
        "username": "login@example.com",
        "password": "wrong password"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"