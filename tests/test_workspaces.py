
def test_create_workspace(auth_client):
    response = auth_client.post("/workspaces/", json={"name": "My Workspace"})
    assert response.status_code == 201
    assert response.json()["name"] == "My Workspace"


def test_get_workspace(auth_client):
    created = auth_client.post("/workspaces/", json={"name": "My Workspace"})
    workspace_id = created.json()["id"]
    response = auth_client.get(f"/workspaces/{workspace_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "My Workspace"


def test_get_workspaces(auth_client):
    auth_client.post("/workspaces/", json={"name": "My Workspace"})
    response = auth_client.get("/workspaces/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "My Workspace"


def test_update_workspace(auth_client):
    created = auth_client.post("/workspaces/", json={"name": "My Workspace"})
    workspace_id = created.json()["id"]

    response = auth_client.patch(f"/workspaces/{workspace_id}", json={"name": "Updated Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_delete_workspace(auth_client):
    created = auth_client.post("/workspaces/", json={"name": "My Workspace"})
    workspace_id = created.json()["id"]
    response = auth_client.delete(f"/workspaces/{workspace_id}")
    assert response.status_code == 204

def test_get_workspace_not_found(auth_client):
    response = auth_client.get("/workspaces/999")
    assert response.status_code == 404


