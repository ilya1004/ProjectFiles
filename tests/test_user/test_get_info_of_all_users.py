from httpx import AsyncClient


async def test_get_info_of_all_users_1(ac: AsyncClient):
    response = await ac.get("/user/get_info_of_all_users")

    assert response.json()["status"] == "success"
    assert response.status_code == 200


async def test_get_info_of_all_users_2(ac: AsyncClient):
    response = await ac.get("/user/get_info_of_all_users")

    assert response.json()["status"] != "error"
    assert response.json()["data"] != "ExceptionNoUser"
    assert response.status_code == 200
