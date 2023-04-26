from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends

from src.api.authentication.base_config import current_user
from src.game_engine.chess_logic import Game

router = APIRouter(
    prefix="/game_engine",
    tags=["Game"]
)


class Player:
    def __init__(self, websocket: WebSocket, player_id: int,
                 rate_blitz: int, rate_rapid: int, rate_classical: int, mode_id: int):
        self.websocket = websocket
        self.player_id = player_id
        self.rate_blitz = rate_blitz
        self.rate_rapid = rate_rapid
        self.rate_classical = rate_classical
        self.mode_id = mode_id

    async def send_game_state(self, game):
        await self.websocket.send_json(game)


class ConnectionManager:
    def __init__(self):
        self.rate_diff = 100
        self.active_connections: list[WebSocket] = []
        self.games_list: dict[Game, bool] = {}
        self.queue_blitz_0: list[Player] = []
        self.queue_blitz_1: list[Player] = []
        self.queue_blitz_2: list[Player] = []

    def add_player_to_queue(self, player: Player):
        try:
            match player.mode_id:
                case 0:
                    self.queue_blitz_0.append(player)
                case 1:
                    self.queue_blitz_1.append(player)
                case 2:
                    self.queue_blitz_2.append(player)
        except WebSocketDisconnect:
            match player.mode_id:
                case 0:
                    if player in self.queue_blitz_0:
                        self.queue_blitz_0.remove(player)
                case 1:
                    if player in self.queue_blitz_1:
                        self.queue_blitz_1.remove(player)
                case 2:
                    if player in self.queue_blitz_2:
                        self.queue_blitz_2.remove(player)

    def add_game_to_list(self, game: Game):
        self.games_list[game] = True

    async def find_new_game(self, mode_id: int) -> (Player, Player):
        match mode_id:
            case 0:
                self.queue_blitz_0.sort(key=self.rate_compare)
                if len(self.queue_blitz_0) <= 1:
                    return None, None
                for i in range(len(self.queue_blitz_0) - 1):
                    if abs(self.queue_blitz_0[i].rate_blitz - self.queue_blitz_0[i + 1].rate_blitz) <= self.rate_diff:
                        await self.send_personal_message(self.queue_blitz_0[i].websocket, f"You will play with player #{self.queue_blitz_0[i + 1].player_id}")
                        await self.send_personal_message(self.queue_blitz_0[i + 1].websocket, f"You will play with player #{self.queue_blitz_0[i].player_id}")
                        return self.queue_blitz_0[i], self.queue_blitz_0[i + 1]
                return None, None

            case 1:
                self.queue_blitz_1.sort(key=self.rate_compare)
            case 2:
                self.queue_blitz_2.sort(key=self.rate_compare)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    #
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def remove_from_queues(self, mode_id, user):
        match mode_id:
            case 0:
                for curr_user in self.queue_blitz_0:
                    if curr_user.player_id == user.id:
                        self.queue_blitz_0.remove(curr_user)
            case 1:
                for curr_user in self.queue_blitz_1:
                    if curr_user.player_id == user.id:
                        self.queue_blitz_1.remove(curr_user)
            case 2:
                for curr_user in self.queue_blitz_2:
                    if curr_user.player_id == user.id:
                        self.queue_blitz_2.remove(curr_user)

    @staticmethod
    def rate_compare(player: Player):
        return player.rate_blitz

    @staticmethod
    async def get_json(websocket: WebSocket) -> dict:
        return await websocket.receive_json(mode="text")

    @staticmethod
    async def get_str(websocket: WebSocket) -> str:
        return await websocket.receive_text()

    def find_curr_game(self, websocket: WebSocket) -> Game or None:
        for game in self.games_list:
            if game.player1 == websocket or game.player2 == websocket:
                return game
        return None


manager = ConnectionManager()


def get_game_for_player(websocket):
    for game in manager.games_list:
        if game.player1 == websocket or game.player2 == websocket:
            return game
    return None


@router.websocket("/add_to_queue/{mode_id}")
async def add_to_queue(websocket: WebSocket, mode_id: int, user=Depends(current_user)):
    try:
        await manager.connect(websocket)
        player = Player(websocket, user.id, user.rate_blitz, user.rate_rapid, user.rate_classical, mode_id)
        manager.add_player_to_queue(player)
        player1, player2 = manager.find_new_game(mode_id)
        if player1 is not None and player2 is not None:
            game = Game(player1, player2)
            manager.add_game_to_list(game)

            await manager.send_personal_message(player1, "game_is_starting")
            await manager.send_personal_message(player2, "game_is_starting")

            await player1.send_game(game)
            await player2.send_game(game)

            while True:
                request_json = await manager.get_json(websocket)
                if request_json["operation"] == "make_a_move":
                    game = manager.find_curr_game(player.websocket)
                    game.make_a_move(request_json)
                    await game.player1.send_game_state(game.to_json())
                    await game.player2.send_game_state(game.to_json())



    except WebSocketDisconnect:
        manager.disconnect(websocket)
        manager.remove_from_queues(mode_id, user)
        await manager.broadcast(f"Client #{user.id} disconnected")


@router.post("/leave_queue")
def leave_queue(mode_id: int, user=Depends(current_user)):
    manager.remove_from_queues(mode_id, user)


'''
@router.websocket("/game_request")
async def websocket_endpoint(websocket: WebSocket):
    # await manager.connect(websocket)

    qw = manager.get_str(websocket)
    user_id_1, user_id_2 = qw.split("|")
    try:
        while True:
            request_json = await manager.get_json(websocket)
            if request_json["request"] == "start_game":
                # player1 = manager.players_queue.pop(0)
                # player2 = manager.players_queue.pop(0)

                game = Game(player1, player2)
                manager.games_list[game] = True

                await player1.websocket.send_json(game.to_json())
                await player2.websocket.send_json(game.to_json())

            elif request_json["request"] == "make_a_move":
                game = get_game_for_player(websocket)
                game.update(request_json)

                await game.player1.send_json(game.to_json())
                await game.player2.send_json(game.to_json())

            elif request_json["request"] == "surrender":
                pass

            else:
                await websocket.send_text("error")

    except WebSocketDisconnect:
        # manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{user_id} disconnected")

'''

'''
queue = list()


@app.post("/queue")
async def add_to_queue(user_info: dict):
    queue.append(user_info)
    return {"message": "User added to queue"}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    try:
        while True:
            if len(queue) >= 2:
                # Найдена пара игроков, начинаем игру
                player1 = queue.pop(0)
                player2 = queue.pop(0)
                await start_game(player1, player2, websocket)
            else:
                # Ждем новых игроков
                await asyncio.sleep(1)
    except WebSocketDisconnect:
        # Обработка отключения игрока
        pass

async def start_game(player1, player2, websocket):
    # Создаем новое WebSocket соединение для каждого игрока
    ws1 = await create_ws(player1["user_id"])
    ws2 = await create_ws(player2["user_id"])
    # Отправляем игрокам информацию о начале игры
    await ws1.send_text(json.dumps({"message": "Game started", "opponent": player2}))
    await ws2.send_text(json.dumps({"message": "Game started", "opponent": player1}))
    # Обрабатываем игру
    while True:
        # Получаем ход от игрока 1
        move1 = await ws1.receive_text()
        # Отправляем ход игроку 2
        await ws2.send_text(move1)
        # Получаем ход от игрока 2
        move2 = await ws2.receive_text()
        # Отправляем ход игроку 1
        await ws1.send_text(move2)

async def create_ws(user_id):
    # Создаем новое WebSocket соединение для пользователя
    ws = WebSocketResponse()
    await ws.prepare(Request(scope={'type': 'websocket', 'path': f'/ws/{user_id}'}))
    return ws



'''

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
#  player_whom_surrender: id,
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
