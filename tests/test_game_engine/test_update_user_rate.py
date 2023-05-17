from httpx import AsyncClient


async def test_update_user_rate_1(ac: AsyncClient):
    response = await ac.post("/game_engine/update_user_rate", params={
        "user_id": 1,
        "mode_id": 3,
        "curr_rate": 1000,
        "rate_diff": 100
    })

    assert response.json()["status"] == "success"
    assert response.json()["data"] == 1100
    assert response.status_code == 200


async def test_update_user_rate_2(ac: AsyncClient):
    response = await ac.post("/game_engine/update_user_rate", params={
        "user_id": 9999,
        "mode_id": 3,
        "curr_rate": 1000,
        "rate_diff": -50
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ExceptionNoUser"
    assert response.status_code == 200


async def test_update_user_rate_3(ac: AsyncClient):
    response = await ac.post("/game_engine/update_user_rate", params={
        "user_id": "str",
        "mode_id": 3,
        "curr_rate": dict(),
        "rate_diff": 100
    })

    assert response.status_code == 422


async def test_update_user_rate_4(ac: AsyncClient):
    response = await ac.post("/game_engine/update_user_rate", params={
        "user_id": 1,
        "mode_id": 99,
        "curr_rate": 1000,
        "rate_diff": 100
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "TypeError"
    assert response.json()["details"] == "Invalid mode id"
    assert response.status_code == 200
