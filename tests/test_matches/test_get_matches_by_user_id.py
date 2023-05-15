from httpx import AsyncClient


async def test_get_matches_by_user_id_1(ac: AsyncClient):
    response = await ac.get("/matches/get_matches_by_user_id", params={
        "user_id": 2,
        "number_of_matches": -1,
        "offset": 0
    })

    assert response.json()["status"] == "success"
    assert response.status_code == 200


async def test_get_matches_by_user_id_2(ac: AsyncClient):
    response = await ac.get("/matches/get_matches_by_user_id", params={
        "user_id": 9999,
        "number_of_matches": -1,
        "offset": 0
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ExceptionNoUser"
    assert response.status_code == 200


async def test_get_matches_by_user_id_3(ac: AsyncClient):
    response = await ac.get("/matches/get_matches_by_user_id", params={
        "user_id": -1234,
        "number_of_matches": -1,
        "offset": 0
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ExceptionNoUser"
    assert response.status_code == 200


async def test_get_matches_by_user_id_4(ac: AsyncClient):
    response = await ac.get("/matches/get_matches_by_user_id", params={
        "user_id": 2,
        "number_of_matches": -999,
        "offset": -123
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ValueError"
    assert response.status_code == 200


async def test_get_matches_by_user_id_5(ac: AsyncClient):
    response = await ac.get("/matches/get_matches_by_user_id", params={
        "user_id": "str",
        "number_of_matches": list(),
        "offset": False
    })

    # print(response.json())
    assert response.status_code == 422
