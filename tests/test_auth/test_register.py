from tests.conftest import client


def test_register_1():
    response = client.post('/auth/register', json={
        "email": "test",
        "password": "test",
        "is_active": False,
        "is_superuser": False,
        "is_verified": False,
        "nickname": "test"
    })

    assert response.status_code == 201


def test_register_2():
    response = client.post('/auth/register', json={
        "email": "qwe",
        "password": "qwe",
        "is_active": False,
        "is_superuser": False,
        "is_verified": False,
        "nickname": "qwe"
    })

    # print(respose.json())
    assert response.status_code == 201


def test_register_3():
    response = client.post('/auth/register', json={
        "email": "qwe",
        "password": "qwe",
        "is_active": False,
        "is_superuser": False,
        "is_verified": False,
        "nickname": "qwe"
    })

    # print(respose.json())
    assert response.status_code == 400


def test_register_4():
    response = client.post('/auth/register', json={
        "email": list(),
        "is_active": False,
        "is_superuser": False,
        "is_verified": False,
        "nickname": dict()
    })

    # print(respose.json())
    assert response.status_code == 422


def test_register_5():
    response = client.post('/auth/register', json={
        "email": "qwe",
        "password": "q",
        "is_active": False,
        "is_superuser": False,
        "is_verified": False,
        "nickname": "qwe"
    })

    # print(respose.json())
    assert response.status_code == 400

