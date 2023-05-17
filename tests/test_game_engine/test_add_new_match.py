from datetime import datetime

from httpx import AsyncClient


async def test_add_new_match_1(ac: AsyncClient):
    response = await ac.post("/game_engine/add_new_match", params={
        "mode_id": 3,
        "played_at": str(datetime.utcnow()),
        "game_length": 100,
        "player_winner_id": 1,
        "player_loser_id": 2,
        "rate_change_winner": -40,
        "rate_change_loser": 40
    })

    # print(response.json())
    assert response.json()["status"] == "success"
    assert response.json()["data"]["mode_id"] == 3
    assert response.json()["data"]["game_length_sec"] == 100
    assert response.status_code == 200


async def test_add_new_match_2(ac: AsyncClient):
    response = await ac.post("/game_engine/add_new_match", params={
        "mode_id": 99,
        "played_at": str(datetime.utcnow()),
        "game_length": 100,
        "player_winner_id": 1,
        "player_loser_id": 2,
        "rate_change_winner": -40,
        "rate_change_loser": 40
    })

    assert response.json()["status"] == "error"
    assert response.json()["data"] == "ValueError"
    assert response.status_code == 200


async def test_add_new_match_3(ac: AsyncClient):
    response = await ac.post("/game_engine/add_new_match", params={
        "mode_id": 4,
        "played_at": str(datetime.utcnow()),
        "game_length": "str",
        "player_winner_id": list(),
        "player_loser_id": 2,
        "rate_change_winner": -56,
        "rate_change_loser": 40
    })

    assert response.status_code == 422


