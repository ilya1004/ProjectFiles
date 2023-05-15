from httpx import AsyncClient


async def test_get_all_matches_1(ac: AsyncClient):
    response = await ac.get("/matches/get_all_matches", params={
        "number_of_matches": 10,
        "offset": 5
    })

    assert response.json()["status"] == "success"
    assert response.status_code == 200


async def test_get_all_matches_2(ac: AsyncClient):
    response = await ac.get("/matches/get_all_matches", params={
        "number_of_matches": -789,
        "offset": -1024
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ValueError"
    assert response.status_code == 200


async def test_get_all_matches_3(ac: AsyncClient):
    response = await ac.get("/matches/get_all_matches", params={
        "number_of_matches": list(),
        "offset": "str"
    })

    assert response.status_code == 422
