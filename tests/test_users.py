
def test_get_me(auth_client):
    response = auth_client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["email"] == "test@test.com"

def test_update_me(auth_client):
    response = auth_client.patch("/users/me", json={
        "username": "updateduser"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"

def test_delete_me(auth_client):
    response = auth_client.delete("/users/me")
    assert response.status_code == 204



