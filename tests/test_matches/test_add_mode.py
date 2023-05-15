from httpx import AsyncClient


async def test_add_mode_1(ac: AsyncClient):
    response = await ac.post("/matches/add_mode", json={
        "id": 1,
        "name": "test",
        "mode_length_sec": 123
    })

    assert response.json()["status"] == "success"
    assert response.json()["data"] == 1
    assert response.status_code == 200


async def test_add_mode_2(ac: AsyncClient):
    response = await ac.post("/matches/add_mode", json={
        "id": 2,
        "name": "test",
        "mode_length_sec": list()
    })

    assert response.status_code == 422


async def test_add_mode_3(ac: AsyncClient):
    response = await ac.post("/matches/add_mode", json={
        "name": "test",
        "mode_length_sec": 123
    })

    # print(response.json())
    assert response.status_code == 422
