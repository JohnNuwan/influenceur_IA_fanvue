import os
import httpx


def get_base_url() -> str:
    return os.getenv("API_BASE_URL", "http://localhost:8000")


def test_health():
    base = get_base_url()
    r = httpx.get(f"{base}/health", timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "healthy"


def test_auth_register_login_me():
    base = get_base_url()
    # Register (idempotent for existing user)
    httpx.post(
        f"{base}/api/v1/auth/register",
        json={
            "email": "dev@example.com",
            "username": "devuser",
            "password": "DevPass123!",
            "full_name": "Dev User",
        },
        timeout=15,
    )

    # Login
    r = httpx.post(
        f"{base}/api/v1/auth/login",
        data={"username": "dev@example.com", "password": "DevPass123!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )
    assert r.status_code == 200
    token = r.json().get("access_token")
    assert token

    # Me
    me = httpx.get(
        f"{base}/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    assert me.status_code == 200
    me_data = me.json()
    assert me_data.get("email") == "dev@example.com"


