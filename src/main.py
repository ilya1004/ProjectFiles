from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect
from src.api.authentication.base_config import auth_backend, fastapi_users
from src.api.authentication.router import router as router_user, get_info_by_user_id
from src.api.authentication.schemas import UserRead, UserCreate
from src.api.matches.router import router as router_matches
from src.database import get_async_session
from src.game_engine.chess_engine import Game
from src.game_engine.connection_manager import ConnectionManager, ConnectionManagerNew
from src.game_engine.player import Player
from src.game_engine.router import router as router_game_engine


app = FastAPI(
    title="Belchessmind.org"
)


origins = ["http://localhost",
           "http://localhost:3000",
           "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_user)
app.include_router(router_matches)
app.include_router(router_game_engine)

# manager = ConnectionManager()
manager = ConnectionManagerNew()


{"user_id": 1, "game_state": "qweqweqwe"}


@app.websocket('/wse/{user_id}')
async def add_to_queue_ws(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(websocket, {
                "user_id": manager.active_connections[websocket],
                "game_state": data["game_state"]
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} left the chat")


@app.websocket("/ws/{mode_id}/{user_id}")
async def add_to_queue_ws(websocket: WebSocket, mode_id: int, user_id: int,
                          session: AsyncSession = Depends(get_async_session)):
    player = None
    player1 = None
    player2 = None

    try:
        await manager.connect_user(websocket)
        while True:
            # request_json = await websocket.receive_json()
            qwe = await websocket.receive_text()
            print(qwe)
            if qwe == "q":
                if mode_id in range(1, 10):
                    is_rate = True
                else:
                    is_rate = False
                user_data = await get_info_by_user_id(user_id, session)

                await websocket.send_text(user_data["data"]["nickname"])

                player = Player(websocket, user_data["data"]['id'], user_data["data"]['nickname'],
                                user_data["data"]['rate_blitz'], user_data["data"]['rate_rapid'],
                                user_data["data"]['rate_rapid'], mode_id, is_rate)

                await manager.add_player_to_queue(player)
                player1, player2 = await manager.find_new_game(mode_id)

                if player1 is None and player2 is None:
                    await websocket.send_text("не пидарасы")

                if player1 is not None and player2 is not None:
                    await player1.websocket.send_text("пидарасы")
                    await player2.websocket.send_text("пидарасы")
                    await manager.remove_player_from_queues(player1)
                    await manager.remove_player_from_queues(player2)
                    time_start = datetime.utcnow()
                    game = Game(player1, player2, mode_id, time_start, player1.is_rated_mode)
                    await manager.add_game_to_list(game)
                    await game.player1.send_game_state(game.get_state())
                    await game.player2.send_game_state(game.get_state())

                    await player1.websocket.send_text("else1")
                    await player2.websocket.send_text("else2")
            elif qwe == "w":
                print("|||||||||qwe == w")
                print(player1)
                print(player2)
                resp1 = await player1.websocket.receive_json()
                resp2 = await player2.websocket.receive_json()
                print(resp1)
                print(resp2)
                await player1.websocket.send_text("else1_qwe")
                await player2.websocket.send_text("else2_qwe")
                # await player1.websocket.send_text(await game.get_id_player_to_move())
                # await player2.websocket.send_text(await game.get_id_player_to_move())
                while True:
                    print("qweqweqwe")
                    request_json = None
                    if game.get_id_player_to_move() == 1:
                        request_json = await player1.get_json()
                    elif game.get_id_player_to_move() == 2:
                        request_json = await player2.get_json()
                    else:
                        print("error validation")

                    if request_json["operation"] == "make_a_move":
                        if request_json["number_player"] == 1:
                            game = manager.find_curr_game(player1)
                        elif request_json["number_player"] == 2:
                            game = manager.find_curr_game(player2)
                        game.make_a_move(request_json["data"][0], request_json["data"][1],
                                         request_json["data"][2], request_json["data"][3])
                        if game.is_game_end():
                            player_winner = game.get_winner()
                            player_loser = game.get_loser()
                            await player_winner.send_message("you_win")
                            await player_loser.send_message("you_lose")
                            break
                        await game.player1.send_game_state(game.get_state())
                        await game.player2.send_game_state(game.get_state())
                    elif request_json['operation'] == "surrender" or request_json['operation'] == "time_over":
                        if request_json["number_player"] == 1:
                            game = manager.find_curr_game(player1)
                        elif request_json["number_player"] == 2:
                            game = manager.find_curr_game(player2)
                        if request_json["number_player"] == 1:
                            await player1.send_message("you_lose")
                            await player2.send_message("you_win")
                            player_winner = player2
                            player_loser = player1
                            break
                        elif request_json["number_player"] == 2:
                            await player1.send_message("you_win")
                            await player2.send_message("you_lose")
                            player_winner = player1
                            player_loser = player2
                            break
                    await manager.set_game_end_to_list(game)
                    time_end = datetime.utcnow()
                    time_length = time_end - time_start
                    game_length = time_length.seconds
                    rate_change_winner, rate_change_loser = 0, 0
                    if game.is_rated:
                        rate_change_winner, rate_change_loser = manager.count_rate_change(player_winner, player_loser)
                        await manager.update_users_rate_in_db(mode_id, player_winner, player_loser,
                                                              rate_change_winner, rate_change_loser)
                    await manager.add_match_to_db(mode_id, time_start, game_length,
                                                  player_winner.nickname, player_loser.nickname,
                                                  player_winner.player_id, player_loser.player_id,
                                                  rate_change_winner, rate_change_loser)
                    await manager.delete_game_from_list(game)
                    await player1.send_message("disconnecting")
                    await player2.send_message("disconnecting")
                    await manager.disconnect_user(player1)
                    await manager.disconnect_user(player2)
            else:
                await websocket.send_text("else")
            await websocket.send_text("else1234")
    except WebSocketDisconnect as e:
        await manager.disconnect_user(websocket)
        await manager.remove_player_from_queues(player)
        await manager.clear_ended_games()
        return {
            "status": "error",
            "data": "WebSocketDisconnect",
            "details": str(e)
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "data": "Exception",
            "details": str(e)
        }


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)

