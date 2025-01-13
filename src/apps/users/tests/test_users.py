from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "username": "test",
            "email": "test@mail.com",
            "password": "testtest",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "test",
        "id": 1,
    }
