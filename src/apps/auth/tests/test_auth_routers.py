from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert token["token_type"] == "bearer"
    assert "access_token" in token
