from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    

def test_create_and_retrieve_issue(client):
    create_response = client.post(
        "/issues",
        json={
            "room": 101,
            "description": "Air conditioning not working",
        },
    )

    assert create_response.status_code == 201

    created_issue = create_response.json()

    assert created_issue["room"] == 101
    assert created_issue["description"] == "Air conditioning not working"
    assert created_issue["status"] == "Open"
    assert "created_at" in created_issue

    issue_id = created_issue["id"]

    get_response = client.get(f"/issues/{issue_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == issue_id
    
def test_list_issues(client):
    response = client.post(
        "/issues",
        json={"room": 202, "description": "Broken television"},
    )

    assert response.status_code == 201
    issue_id = response.json()["id"]

    response = client.get("/issues")

    assert response.status_code == 200
    assert any(
        issue["id"] == issue_id
        for issue in response.json()["issues"]
    )


def test_close_issue(client):
    response = client.post(
        "/issues",
        json={"room": 203, "description": "Leaking shower"},
    )

    assert response.status_code == 201
    issue_id = response.json()["id"]

    response = client.patch(f"/issues/{issue_id}")

    assert response.status_code == 200

    response = client.get(f"/issues/{issue_id}")

    assert response.status_code == 200
    assert response.json()["status"] == "Closed"


def test_delete_issue(client):
    response = client.post(
        "/issues",
        json={"room": 204, "description": "Broken door lock"},
    )

    assert response.status_code == 201
    issue_id = response.json()["id"]

    response = client.delete(f"/issues/{issue_id}")

    assert response.status_code == 200

    response = client.get(f"/issues/{issue_id}")

    assert response.status_code == 404


def test_issue_not_found(client):
    response = client.get("/issues/999999999")

    assert response.status_code == 404


def test_invalid_issue_data(client):
    response = client.post(
        "/issues",
        json={
            "room": -5,
            "description": "Hi",
        },
    )

    assert response.status_code == 422
    
def test_rollback_isolation(client):
    response = client.post(
        "/issues",
        json={
            "room": 999,
            "description": "Rollback verification",
        },
    )

    assert response.status_code == 201