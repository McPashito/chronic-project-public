from app.api.routes import auth_routes
from tests.helpers import get_auth_headers, login_user, register_user


def test_register_user_returns_created_user(client):
    response = register_user(client)

    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["name"] == "Demo"
    assert data["surname"] == "User"
    assert data["date_of_birth"] == "1990-01-01"
    assert data["subscription_type"] == "standard"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_can_be_disabled_by_environment(client, monkeypatch):
    monkeypatch.setenv("ALLOW_PUBLIC_REGISTRATION", "false")

    response = register_user(client)

    assert response.status_code == 403
    assert (
        response.json()["detail"]
        == "El registro publico esta deshabilitado en esta demo"
    )


def test_register_rejects_short_password(client):
    response = register_user(client, password="Short1!")

    assert response.status_code == 422


def test_register_rejects_password_longer_than_72_characters(client):
    response = register_user(client, password="A" * 73)

    assert response.status_code == 422


def test_login_returns_access_token(client):
    register_user(client)

    response = login_user(client)

    assert response.status_code == 200

    data = response.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert data["access_token"]


def test_login_with_wrong_password_returns_error(client):
    register_user(client)

    response = login_user(client, password="WrongPassword123!")

    assert response.status_code == 400
    assert response.json()["detail"] == "Credenciales incorrectas"


def test_login_rate_limit_blocks_for_one_minute_after_too_many_attempts(
    client, monkeypatch
):
    current_time = 1000.0
    monkeypatch.setattr(auth_routes, "monotonic", lambda: current_time)

    register_user(client)

    for _ in range(10):
        response = login_user(client, password="WrongPassword123!")
        assert response.status_code == 400

    response = login_user(client, password="WrongPassword123!")

    assert response.status_code == 429
    assert (
        response.json()["detail"]
        == "Demasiados intentos de login. Intentalo de nuevo en un minuto"
    )

    response = login_user(client)

    assert response.status_code == 429

    current_time += auth_routes.LOGIN_BLOCK_SECONDS + 1

    response = login_user(client)

    assert response.status_code == 200


def test_protected_route_without_token_returns_401(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_protected_route_with_token_returns_current_user(client):
    register_user(client)
    headers = get_auth_headers(client)

    response = client.get("/users/me", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["name"] == "Demo"
    assert data["surname"] == "User"
