from httpx import AsyncClient


async def test_get_all_modes_1(ac: AsyncClient):
    response = await ac.get("/matches/get_all_modes")

    assert response.json()["status"] == "success"
    assert response.status_code == 200

