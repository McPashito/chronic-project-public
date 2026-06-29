DEFAULT_EMAIL = "user@example.com"
DEFAULT_PASSWORD = "Demo1234!"


def register_user(
    client,
    email=DEFAULT_EMAIL,
    password=DEFAULT_PASSWORD,
    name="Demo",
    surname="User",
    date_of_birth="1990-01-01",
    subscription_type=None,
):
    payload = {
        "email": email,
        "password": password,
        "name": name,
        "surname": surname,
        "date_of_birth": date_of_birth,
    }

    if subscription_type is not None:
        payload["subscription_type"] = subscription_type

    return client.post("/auth/register", json=payload)


def login_user(client, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD):
    return client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )


def get_auth_headers(client, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD):
    login_response = login_user(client, email=email, password=password)
    access_token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {access_token}"}
