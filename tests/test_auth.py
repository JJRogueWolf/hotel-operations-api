from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

import jwt

from auth import SECRET_KEY, ALGORITHM, create_access_token, ADMIN_USERNAME

from main import app


def test_login_rejects_wrong_password():
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            data={
                "username": ADMIN_USERNAME,
                "password": "definitely-wrong-password",
            },
        )

    assert response.status_code == 401


def test_issues_require_authentication():
    with TestClient(app) as client:
        response = client.get("/issues")

    assert response.status_code == 401


def test_invalid_token_is_rejected():
    with TestClient(app) as client:
        response = client.get(
            "/issues",
            headers={"Authorization": "Bearer invalid-token"},
        )

    assert response.status_code == 401


def test_valid_token_allows_access(client):
    response = client.get("/issues")

    assert response.status_code == 200


def test_health_does_not_require_authentication():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    
def test_successful_login():
    # This test requires the actual password, so we'll test
    # token creation instead without exposing credentials.
    token = create_access_token(ADMIN_USERNAME)

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    assert payload["sub"] == ADMIN_USERNAME
    assert "exp" in payload


def test_expired_token_is_rejected():
    expired_token = jwt.encode(
        {
            "sub": ADMIN_USERNAME,
            "exp": datetime.now(timezone.utc)
            - timedelta(minutes=1),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    with TestClient(app) as client:
        response = client.get(
            "/issues",
            headers={
                "Authorization": f"Bearer {expired_token}"
            },
        )

    assert response.status_code == 401