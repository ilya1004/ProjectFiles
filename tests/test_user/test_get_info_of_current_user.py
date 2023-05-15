from tests.conftest import client


def test_get_info_of_current_user_1():
    response = client.get("user/get_info_of_current_user")

    # print(response.json())
    assert response.status_code == 200


def test_get_info_of_current_user_2():
    response = client.get("user/get_info_of_current_user")

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ExceptionUnauthorized"
    assert response.status_code == 200


def test_get_info_of_current_user_3():
    response = client.get("user/get_info_of_current_user")

    # print(response.json())
    assert response.status_code == 200
