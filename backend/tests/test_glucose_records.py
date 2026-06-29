from datetime import date, timedelta

from tests.helpers import get_auth_headers, register_user


def glucose_payload(**overrides):
    payload = {
        "date": date.today().isoformat(),
        "time": "08:30:00",
        "glucose_value": 110,
        "notes": "Before breakfast",
        "moment_of_day": "fasting",
    }
    payload.update(overrides)
    return payload


def create_glucose_record(client, headers, **overrides):
    return client.post(
        "/glucose-records/",
        headers=headers,
        json=glucose_payload(**overrides),
    )


def test_create_and_list_glucose_records(client):
    register_user(client)
    headers = get_auth_headers(client)

    create_response = create_glucose_record(client, headers)

    assert create_response.status_code == 200

    created_record = create_response.json()
    assert created_record["glucose_value"] == 110
    assert created_record["notes"] == "Before breakfast"
    assert created_record["moment_of_day"] == "fasting"

    list_response = client.get("/glucose-records/", headers=headers)

    assert list_response.status_code == 200

    records = list_response.json()
    assert len(records) == 1
    assert records[0]["id"] == created_record["id"]
    assert records[0]["glucose_value"] == 110


def test_edit_and_delete_own_glucose_record(client):
    register_user(client)
    headers = get_auth_headers(client)
    created_record = create_glucose_record(client, headers).json()

    edit_response = client.put(
        f"/glucose-records/{created_record['id']}",
        headers=headers,
        json=glucose_payload(
            time="22:15:00",
            glucose_value=145,
            notes="After dinner",
            moment_of_day="night",
        ),
    )

    assert edit_response.status_code == 200

    edited_record = edit_response.json()
    assert edited_record["id"] == created_record["id"]
    assert edited_record["time"] == "22:15:00"
    assert edited_record["glucose_value"] == 145
    assert edited_record["notes"] == "After dinner"
    assert edited_record["moment_of_day"] == "night"

    delete_response = client.delete(
        f"/glucose-records/{created_record['id']}",
        headers=headers,
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Registro eliminado correctamente"

    list_response = client.get("/glucose-records/", headers=headers)

    assert list_response.status_code == 200
    assert list_response.json() == []


def test_glucose_record_filters_by_moment_and_date(client):
    register_user(client)
    headers = get_auth_headers(client)
    today = date.today()
    yesterday = today - timedelta(days=1)

    create_glucose_record(
        client,
        headers,
        date=yesterday.isoformat(),
        glucose_value=95,
        moment_of_day="fasting",
    )
    create_glucose_record(
        client,
        headers,
        date=today.isoformat(),
        glucose_value=150,
        moment_of_day="after_meal",
    )

    response = client.get(
        "/glucose-records/",
        headers=headers,
        params={
            "moment_of_day": "after_meal",
            "start_date": today.isoformat(),
            "end_date": today.isoformat(),
        },
    )

    assert response.status_code == 200

    records = response.json()
    assert len(records) == 1
    assert records[0]["glucose_value"] == 150
    assert records[0]["moment_of_day"] == "after_meal"


def test_glucose_record_validation_rejects_invalid_values(client):
    register_user(client)
    headers = get_auth_headers(client)

    invalid_value_response = create_glucose_record(
        client,
        headers,
        glucose_value=601,
    )
    future_date_response = create_glucose_record(
        client,
        headers,
        date=(date.today() + timedelta(days=1)).isoformat(),
    )

    assert invalid_value_response.status_code == 422
    assert future_date_response.status_code == 422


def test_user_cannot_access_another_users_glucose_records(client):
    register_user(client, email="owner@example.com")
    owner_headers = get_auth_headers(client, email="owner@example.com")
    owner_record = create_glucose_record(client, owner_headers).json()

    register_user(client, email="other@example.com")
    other_headers = get_auth_headers(client, email="other@example.com")

    list_response = client.get("/glucose-records/", headers=other_headers)
    detail_response = client.get(
        f"/glucose-records/{owner_record['id']}",
        headers=other_headers,
    )
    edit_response = client.put(
        f"/glucose-records/{owner_record['id']}",
        headers=other_headers,
        json=glucose_payload(glucose_value=180),
    )
    delete_response = client.delete(
        f"/glucose-records/{owner_record['id']}",
        headers=other_headers,
    )

    assert list_response.status_code == 200
    assert list_response.json() == []
    assert detail_response.status_code == 404
    assert edit_response.status_code == 404
    assert delete_response.status_code == 404


def test_glucose_summary_returns_empty_values_without_records(client):
    register_user(client)
    headers = get_auth_headers(client)

    response = client.get("/glucose-records/summary", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert data["total_records"] == 0
    assert data["min_glucemia"] is None
    assert data["max_glucemia"] is None
    assert data["average_glucemia"] is None
    assert data["last_glucemia"] is None


def test_glucose_summary_calculates_total_min_max_and_average(client):
    register_user(client)
    headers = get_auth_headers(client)

    create_glucose_record(client, headers, glucose_value=90)
    create_glucose_record(client, headers, glucose_value=120)
    create_glucose_record(client, headers, glucose_value=150)

    response = client.get("/glucose-records/summary", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert data["total_records"] == 3
    assert data["min_glucemia"]["glucose_value"] == 90
    assert data["max_glucemia"]["glucose_value"] == 150
    assert data["average_glucemia"] == 120


def test_glucose_summary_does_not_use_another_users_records(client):
    register_user(client, email="owner@example.com")
    owner_headers = get_auth_headers(client, email="owner@example.com")
    create_glucose_record(client, owner_headers, glucose_value=90)

    register_user(client, email="other@example.com")
    other_headers = get_auth_headers(client, email="other@example.com")
    create_glucose_record(client, other_headers, glucose_value=180)

    response = client.get("/glucose-records/summary", headers=owner_headers)

    assert response.status_code == 200

    data = response.json()
    assert data["total_records"] == 1
    assert data["min_glucemia"]["glucose_value"] == 90
    assert data["max_glucemia"]["glucose_value"] == 90
    assert data["average_glucemia"] == 90


def test_glucose_summary_uses_measurement_date_and_time_for_last_record(client):
    register_user(client)
    headers = get_auth_headers(client)
    today = date.today()
    yesterday = today - timedelta(days=1)

    create_glucose_record(
        client,
        headers,
        date=today.isoformat(),
        time="09:00:00",
        glucose_value=100,
    )
    create_glucose_record(
        client,
        headers,
        date=yesterday.isoformat(),
        time="23:00:00",
        glucose_value=160,
    )

    response = client.get("/glucose-records/summary", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert data["last_glucemia"]["date"] == today.isoformat()
    assert data["last_glucemia"]["time"] == "09:00:00"
    assert data["last_glucemia"]["glucose_value"] == 100
