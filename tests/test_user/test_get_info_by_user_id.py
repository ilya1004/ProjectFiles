from httpx import AsyncClient
from tests.conftest import client


async def test_get_info_by_user_id_1(ac: AsyncClient):
    response = await ac.get("/user/get_info_by_user_id", params={
        "user_id": 2
    })

    assert response.json()["status"] == "success"
    assert response.json()["data"]["id"] == 2
    assert response.status_code == 200


async def test_get_info_by_user_id_2(ac: AsyncClient):
    response = await ac.get("/user/get_info_by_user_id", params={
        "user_id": 9999
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ExceptionNoUser"
    assert response.status_code == 200


async def test_get_info_by_user_id_3(ac: AsyncClient):
    response = await ac.get("/user/get_info_by_user_id", params={
        "user_id": -1234
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ExceptionNoUser"
    assert response.status_code == 200


async def test_get_info_by_user_id_4(ac: AsyncClient):
    response = await ac.get("/user/is_user_in_database_by_id", params={
        "user_id": "str"
    })

    assert response.status_code == 422


async def test_get_info_by_user_id_5(ac: AsyncClient):
    response = await ac.get("/user/is_user_in_database_by_id", params={
        "user_id": list()
    })

    assert response.status_code == 422
