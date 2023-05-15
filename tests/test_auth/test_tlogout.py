from tests.conftest import client


def test_logot_1():
    response = client.post("/auth/jwt/logout")

    assert response.status_code == 200


def test_logout_2():
    response = client.post("/auth/jwt/logout")

    assert response.json() == "User is not active"
    assert response.status_code == 200
