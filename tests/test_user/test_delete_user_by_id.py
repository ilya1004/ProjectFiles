from httpx import AsyncClient


async def test_delete_user_by_id_1(ac: AsyncClient):
    response = await ac.post("/user/delete_user_by_id", params={
        "user_id": 1
    })

    assert response.json()["status"] == "success"
    assert response.json()["data"] == 1
    assert response.status_code == 200


async def test_delete_user_by_id_2(ac: AsyncClient):
    response = await ac.post("/user/delete_user_by_id", params={
        "user_id": 9999
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ExceptionNoUser"
    assert response.status_code == 200


async def test_delete_user_by_id_3(ac: AsyncClient):
    response = await ac.post("/user/delete_user_by_id", params={
        "user_id": -1234
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ExceptionNoUser"
    assert response.status_code == 200


async def test_delete_user_by_id_4(ac: AsyncClient):
    response = await ac.post("/user/delete_user_by_id", params={
        "user_id": "str"
    })

    assert response.status_code == 422


async def test_delete_user_by_id_5(ac: AsyncClient):
    response = await ac.post("/user/delete_user_by_id", params={
        "user_id": list()
    })

    # print(response.json())
    assert response.status_code == 422
