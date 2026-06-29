from tests.helpers import get_auth_headers, login_user, register_user


def test_edit_user_updates_profile(client):
    register_user(client)
    headers = get_auth_headers(client)

    response = client.put(
        "/users/edit_user",
        headers=headers,
        json={
            "name": "Updated",
            "surname": "Person",
            "date_of_birth": "1985-05-20",
            "subscription_type": "premium",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["name"] == "Updated"
    assert data["surname"] == "Person"
    assert data["date_of_birth"] == "1985-05-20"
    assert data["subscription_type"] == "premium"


def test_change_password_rejects_wrong_current_password(client):
    register_user(client)
    headers = get_auth_headers(client)

    response = client.put(
        "/users/change_password",
        headers=headers,
        json={
            "old_password": "WrongPassword123!",
            "new_password": "NewDemo1234!",
        },
    )

    assert response.status_code == 400
    assert "detail" in response.json()


def test_change_password_rejects_short_new_password(client):
    register_user(client)
    headers = get_auth_headers(client)

    response = client.put(
        "/users/change_password",
        headers=headers,
        json={
            "old_password": "Demo1234!",
            "new_password": "Short1!",
        },
    )

    assert response.status_code == 422


def test_change_password_rejects_new_password_longer_than_72_characters(client):
    register_user(client)
    headers = get_auth_headers(client)

    response = client.put(
        "/users/change_password",
        headers=headers,
        json={
            "old_password": "Demo1234!",
            "new_password": "A" * 73,
        },
    )

    assert response.status_code == 422


def test_change_password_allows_login_with_new_password(client):
    register_user(client)
    headers = get_auth_headers(client)

    response = client.put(
        "/users/change_password",
        headers=headers,
        json={
            "old_password": "Demo1234!",
            "new_password": "NewDemo1234!",
        },
    )

    assert response.status_code == 200

    old_login_response = login_user(client, password="Demo1234!")
    new_login_response = login_user(client, password="NewDemo1234!")

    assert old_login_response.status_code == 400
    assert new_login_response.status_code == 200
    assert new_login_response.json()["access_token"]
