from httpx import AsyncClient
from tests.conftest import client


async def test_is_user_in_database_by_id_1(ac: AsyncClient):
    response = await ac.get("/user/is_user_in_database_by_id", params={
        "user_id": 2
    })

    assert response.json()["status"] == "success"
    assert response.json()["data"] == 1
    assert response.status_code == 200


async def test_is_user_in_database_by_id_2(ac: AsyncClient):
    response = await ac.get("/user/is_user_in_database_by_id", params={
        "user_id": 9999
    })

    assert response.json()["status"] == "success"
    assert response.json()["data"] == 0
    assert response.status_code == 200


async def test_is_user_in_database_by_id_3(ac: AsyncClient):
    response = await ac.get("/user/is_user_in_database_by_id", params={
        "user_id": -1234
    })

    assert response.json()["status"] == "success"
    assert response.json()["data"] == 0
    assert response.status_code == 200


async def test_is_user_in_database_by_id_4(ac: AsyncClient):
    response = await ac.get("/user/is_user_in_database_by_id", params={
        "user_id": "str"
    })

    # print(response.json())
    assert response.status_code == 422


async def test_is_user_in_database_by_id_5(ac: AsyncClient):
    response = await ac.get("/user/is_user_in_database_by_id", params={
        "user_id": dict()
    })

    # print(response.json())
    assert response.status_code == 422
