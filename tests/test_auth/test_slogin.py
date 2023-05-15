from tests.conftest import client


def test_login_1():
    response = client.post("/auth/jwt/login", **{"data": {
        "username": "test",
        "password": "test"
    }})

    # print(response.json())
    assert response.status_code == 200


def test_login_2():
    response = client.post("/auth/jwt/login", **{"data": {
        "username": "no_test",
        "password": "no_test"
    }})

    # print(response.json())
    assert response.status_code == 400


def test_login_3():
    response = client.post("/auth/jwt/login", **{"data": {
        "username": None,
        "password": dict()
    }})

    # print(response.json())
    assert response.status_code == 422
