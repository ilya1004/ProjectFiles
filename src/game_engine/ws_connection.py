from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends
from src.api.authentication.base_config import current_user
from src.game_engine.chess_engine import Game
from src.game_engine.connection_manager import ConnectionManager
from src.game_engine.player import Player


router = APIRouter(
    prefix="/game_engine_ws",
    tags=["Game_ws"]
)


manager = ConnectionManager()

'''
blitz_rate = 1, 2, 3
rapid_rate = 4, 5, 6
classical_rate = 7, 8, 9

blitz_unrate = 11, 12, 13
rapid_unrate = 14, 15, 16
classical_unrate = 17, 18, 19
'''


@router.websocket("/ws/{mode_id}/{user_id}")
async def add_to_queue_ws(websocket: WebSocket, mode_id: int, user_id: int):
    try:
        if not isinstance(mode_id, int):
            raise TypeError("Mode ID should be int")
        if mode_id not in range(1, 20):
            raise ValueError("Mode ID should be in range(1, 20)")

        if mode_id in range(1, 10):
            is_rate = True
        else:
            is_rate = False
        await manager.connect_user(websocket)
        player = Player(websocket, user.id, user.nickname,
                        user.rate_blitz, user.rate_rapid, user.rate_classical, mode_id, is_rate)
        manager.add_player_to_queue(player)
        player1, player2 = manager.find_new_game(mode_id)

        if player1 is not None and player2 is not None:
            manager.remove_player_from_queues(player1)
            manager.remove_player_from_queues(player2)
            time_start = datetime.utcnow()
            game = Game(player1, player2, mode_id, time_start, player1.is_rated_mode)
            manager.add_game_to_list(game)
            await player1.send_message("game_is_starting")
            await player2.send_message("game_is_starting")
            await game.player1.send_game_state(game.to_json())
            await game.player2.send_game_state(game.to_json())
            while True:
                request_json = None
                if game.get_id_player_to_move() == 1:
                    request_json = await player1.get_json()
                elif game.get_id_player_to_move() == 2:
                    request_json = await player2.get_json()
                if request_json["operation"] == "make_a_move":
                    if request_json["number_player"] == 1:
                        game = manager.find_curr_game(player1)
                    elif request_json["number_player"] == 2:
                        game = manager.find_curr_game(player2)
                    game.make_a_move(request_json)
                    if game.is_game_end():
                        player_winner = game.get_winner()
                        player_loser = game.get_loser()
                        await player_winner.send_message("you_win")
                        await player_loser.send_message("you_lose")
                        break
                    await game.player1.send_game_state(game.to_json())
                    await game.player2.send_game_state(game.to_json())
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
            manager.set_game_end_to_list(game)
            time_end = datetime.utcnow()
            time_length = time_end - time_start
            game_length = time_length.seconds
            rate_change_winner, rate_change_loser = 0, 0
            if game.is_rated:
                rate_change_winner, rate_change_loser = manager.count_rate_change(player_winner, player_loser)
                await manager.update_users_rate_in_db(mode_id, player_winner, player_loser,
                                                      rate_change_winner, rate_change_loser)
            await manager.add_match_to_db(mode_id, time_start, game_length,
                                          player_winner.nickname,
                                          player_winner.player_id, player_loser.player_id,
                                          rate_change_winner, rate_change_loser)
            manager.delete_game_from_list(game)
            await player1.send_message("disconnecting")
            await player2.send_message("disconnecting")
            await manager.disconnect_user(player1)
            await manager.disconnect_user(player2)

    except WebSocketDisconnect as e:
        await manager.disconnect_user(websocket)
        manager.remove_player_from_queues(user)
        manager.clear_ended_games()
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
    except ValueError as e:
        return {
            "status": "error",
            "data": "ValueError",
            "details": str(e)
        }
    except TypeError as e:
        return {
            "status": "error",
            "data": "TypeError",
            "details": str(e)
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }

'''
JSON файлы для партии:

{
    "operation": "make_a_move",
    "number_player": 1/2
    "data": "какая-то информация для выполнения хода"    
}

{
    "operation": "surrender"/"time_over",
    "number_player": 1/2
    "data": None    
}

'''
