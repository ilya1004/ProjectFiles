from httpx import AsyncClient


async def test_get_matches_of_current_user_1(ac: AsyncClient):
    response = await ac.get("/matches/get_matches_of_current_user", params={
        "number_of_matches": -1,
        "offset": 0
    })

    assert response.json()["status"] == "success"
    assert response.status_code == 200


async def test_get_matches_of_current_user_2(ac: AsyncClient):
    response = await ac.get("/matches/get_matches_of_current_user", params={
        "number_of_matches": -1,
        "offset": 0
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ExceptionUnauthorized"
    assert response.status_code == 200


async def test_get_matches_of_current_user_3(ac: AsyncClient):
    response = await ac.get("/matches/get_matches_of_current_user", params={
        "number_of_matches": -567,
        "offset": -888
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ValueError"
    assert response.status_code == 200


async def test_get_matches_of_current_user_4(ac: AsyncClient):
    response = await ac.get("/matches/get_matches_of_current_user", params={
        "number_of_matches": dict(),
        "offset": set()
    })

    assert response.status_code == 422
