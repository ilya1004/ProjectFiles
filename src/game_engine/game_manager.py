from fastapi import FastAPI, WebSocket, APIRouter
from src.game_engine.chess_logic import Game


router = APIRouter(
    prefix="/game_engine",
    tags=["Game"]
)

games_list = {}

players_queue = []


def get_game_for_player(websocket):
    for game in games_list:
        if game.player1 == websocket or game.player2 == websocket:
            return game
    return None


@router.websocket("/game_request")
async def websocket_endpoint(websocket: WebSocket, id: int):
    await websocket.accept()

    request_json = await websocket.receive_json()

    if request_json == "join queue":
        players_queue.append(websocket)
        await websocket.send_text("joined queue")
        if len(players_queue) >= 2:

            player1 = players_queue.pop(0)
            player2 = players_queue.pop(0)

            game = Game(player1, player2)
            games_list[game] = True

            await player1.send_json(game.to_json())
            await player2.send_json(game.to_json())

    elif request_json == "make_a_move":
        game = get_game_for_player(websocket)
        game.update(request_json)

        await game.player1.send_json(game.to_json())
        await game.player2.send_json(game.to_json())

    elif request_json == "surrender":
        pass

    else:
        await websocket.send_text("error")


# Тут написан тот же код но с комментариями от чат гпт

'''
# jsons

# {
#  request: join_queue
# }

# {
#  request: make_a_move,
#  spot_from: a1,
#  spot_to: a1,
# }

# {
#  request: surrender,
#  player_who_surrender: id,
#  player_who_surrender: id,
# }

games_list = {}  # Словарь для хранения созданных игр

players_queue = []  # Очередь игроков


def get_game_for_player(websocket):
    for game in games_list:
        if game.player1 == websocket or game.player2 == websocket:
            return game
    return None


@router.websocket("/game_request")
async def websocket_endpoint(websocket: WebSocket):
    # Обработчик WebSocket соединения

    await websocket.accept()

    # Получаем запрос от игрока
    # request_str = await websocket.receive_text()
    request_json = await websocket.receive_json()

    # Проверяем тип запроса

    if request_json == "join queue":
        # Если игрок хочет присоединиться к очереди, добавляем его в очередь
        players_queue.append(websocket)
        await websocket.send_text("joined queue")

        # Если в очереди есть уже два игрока, создаем новую игру
        if len(players_queue) >= 2:
            # Создаем новую игру и удаляем игроков из очереди
            player1 = players_queue.pop(0)
            player2 = players_queue.pop(0)

            game = Game(player1, player2)
            games_list[game] = True  # Добавляем новую игру в словарь с играми

            # Отправляем игрокам сообщение с информацией о текущей игре
            await player1.send_json(game.to_json())
            await player2.send_json(game.to_json())

    elif request_json == "make_a_move":
        # Если игрок хочет сделать ход, обновляем состояние игры и отправляем его
        game = get_game_for_player(websocket)  # Получаем объект игры, в которой участвует игрок
        game.update(request_json)  # Обновляем состояние игры на основе хода игрока

        # Отправляем обновленное состояние игры обоим игрокам
        await game.player1.send_json(game.to_json())
        await game.player2.send_json(game.to_json())

    elif request_json == "surrender":  # когда игрок сдается

        pass



    else:
        await websocket.send_text("error")
'''
