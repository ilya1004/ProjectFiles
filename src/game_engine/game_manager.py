from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends

from src.api.authentication.base_config import current_user
from src.game_engine.router import update_user_rate
from src.game_engine.chess_logic import Game
from src.api.matches.router import add_new_match

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

    async def send_personal_message(self, message: str):
        await self.websocket.send_text(message)

    async def get_json(self) -> dict:
        return await self.websocket.receive_json(mode="text")


class ConnectionManager:
    def __init__(self):
        self.rate_diff = 100
        self.active_connections: list[WebSocket] = []
        self.games_list: dict[Game, bool] = {}
        self.queue_blitz: list[list[Player], list[Player], list[Player]] = []
        self.queue_rapid: list[list[Player], list[Player], list[Player]] = []
        self.queue_classical: list[list[Player], list[Player], list[Player]] = []

    def add_player_to_queue(self, player: Player):
        if player.mode_id in (0, 1, 2):
            self.queue_blitz[player.mode_id].append(player)
        elif player.mode_id in (3, 4, 5):
            self.queue_rapid[player.mode_id % 3].append(player)
        elif player.mode_id in (6, 7, 8):
            self.queue_classical[player.mode_id % 3].append(player)

    def add_game_to_list(self, game: Game):
        self.games_list[game] = True

    def set_game_end_to_list(self, game: Game):
        self.games_list[game] = False

    async def find_new_game(self, mode_id: int) -> (Player, Player):
        if mode_id in (0, 1, 2):
            self.queue_blitz[mode_id].sort(key=self.rate_compare_blitz)
            if len(self.queue_blitz[mode_id]) <= 1:
                return None, None
            for i in range(len(self.queue_blitz[mode_id]) - 1):
                if abs(self.queue_blitz[mode_id][i].rate_blitz -
                       self.queue_blitz[mode_id][i + 1].rate_blitz) <= self.rate_diff:
                    await self.queue_blitz[mode_id][i].send_personal_message(
                        f"You will play with player #{self.queue_blitz[mode_id][i + 1].player_id}")
                    await self.queue_blitz[mode_id][i].send_personal_message(
                        f"You will play with player #{self.queue_blitz[mode_id][i].player_id}")
                    return self.queue_blitz[mode_id][i], self.queue_blitz[mode_id][i + 1]
        elif mode_id in (3, 4, 5):
            mode_id %= 3
            self.queue_rapid[mode_id].sort(key=self.rate_compare_rapid)
            if len(self.queue_rapid[mode_id]) <= 1:
                return None, None
            for i in range(len(self.queue_rapid[mode_id]) - 1):
                if abs(self.queue_rapid[mode_id][i].rate_rapid -
                       self.queue_rapid[mode_id][i + 1].rate_rapid) <= self.rate_diff:
                    await self.queue_rapid[mode_id][i].send_personal_message(
                        f"You will play with player #{self.queue_rapid[mode_id][i + 1].player_id}")
                    await self.queue_rapid[mode_id][i].send_personal_message(
                        f"You will play with player #{self.queue_rapid[mode_id][i].player_id}")
                    return self.queue_rapid[mode_id][i], self.queue_rapid[mode_id][i + 1]
        elif mode_id in (6, 7, 8):
            mode_id %= 3
            self.queue_classical[mode_id].sort(key=self.rate_compare_classical)
            if len(self.queue_classical[mode_id]) <= 1:
                return None, None
            for i in range(len(self.queue_classical[mode_id]) - 1):
                if abs(self.queue_classical[mode_id][i].rate_classical -
                       self.queue_classical[mode_id][i + 1].rate_classical) <= self.rate_diff:
                    await self.queue_classical[mode_id][i].send_personal_message(
                        f"You will play with player #{self.queue_classical[mode_id][i + 1].player_id}")
                    await self.queue_classical[mode_id][i].send_personal_message(
                        f"You will play with player #{self.queue_classical[mode_id][i].player_id}")
                    return self.queue_classical[mode_id][i], self.queue_classical[mode_id][i + 1]

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    #
    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            await websocket.close()

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def remove_from_queues(self, player: Player):
        if player.mode_id in (0, 1, 2) and player in self.queue_blitz[player.mode_id]:
            self.queue_blitz[player.mode_id].remove(player)
        elif player.mode_id in (3, 4, 5) and player in self.queue_rapid[player.mode_id % 3]:
            self.queue_rapid[player.mode_id % 3].remove(player)
        elif player.mode_id in (6, 7, 8) and player in self.queue_classical[player.mode_id % 3]:
            self.queue_rapid[player.mode_id % 3].remove(player)

    @staticmethod
    async def add_match_to_db(mode_id: int, played_at: datetime, game_length: int, player_winner_id: int,
                              player_loser_id: int, rate_change_1: int, rate_change_2: int):
        await add_new_match(mode_id, played_at, game_length, player_winner_id,
                            player_loser_id, rate_change_1, rate_change_2)

    @staticmethod
    def rate_compare_blitz(player: Player):
        return player.rate_blitz

    @staticmethod
    def rate_compare_rapid(player: Player):
        return player.rate_rapid

    @staticmethod
    def rate_compare_classical(player: Player):
        return player.rate_classical

    def find_curr_game(self, websocket: WebSocket) -> Game | None:
        for game in self.games_list:
            if game.player1 == websocket or game.player2 == websocket:
                return game
        return None

    @staticmethod
    def count_rate_change(mode_id: int, player_winner: Player, player_loser: Player) -> (int, int):
        # изменение рейтинга победителя, рейтинга проигравшего
        if mode_id in (0, 1, 2):
            return 25, -25
        elif mode_id in (3, 4, 5):
            return 25, -25
        elif mode_id in (6, 7, 8):
            return 25, -25

    @staticmethod
    async def update_users_rate_in_db(mode_id: int, player_winner: Player, player_loser: Player,
                                      rate_change_1: int, rate_change_2: int):
        if mode_id in (0, 1, 2):
            await update_user_rate(player_winner.player_id, "blitz", rate_change_1)
            await update_user_rate(player_loser.player_id, "blitz", rate_change_2)
        elif mode_id in (3, 4, 5):
            await update_user_rate(player_winner.player_id, "rapid", rate_change_1)
            await update_user_rate(player_loser.player_id, "rapid", rate_change_2)
        elif mode_id in (6, 7, 8):
            await update_user_rate(player_winner.player_id, "classical", rate_change_1)
            await update_user_rate(player_loser.player_id, "classical", rate_change_2)


manager = ConnectionManager()


@router.websocket("/add_to_queue/{mode_id}")
async def add_to_queue(websocket: WebSocket, mode_id: int, user=Depends(current_user)):
    try:
        if not isinstance(mode_id, int):
            raise TypeError("Mode ID should be int")
        if mode_id not in (range(0, 8)):
            raise ValueError("Mode ID should be in (range(0, 8))")
        await manager.connect(websocket)
        player = Player(websocket, user.id, user.rate_blitz, user.rate_rapid, user.rate_classical, mode_id)
        manager.add_player_to_queue(player)
        player1, player2 = manager.find_new_game(mode_id)
        if player1 is not None and player2 is not None:
            manager.remove_from_queues(player1)
            manager.remove_from_queues(player2)
            game = Game(player1, player2)
            manager.add_game_to_list(game)

            await player1.send_personal_message("game_is_starting")
            await player2.send_personal_message("game_is_starting")

            await player1.send_game(game)
            await player2.send_game(game)
            time_start = datetime.utcnow()

            while True:
                request_json = await player.get_json()
                if request_json["operation"] == "make_a_move":
                    game = manager.find_curr_game(player.websocket)
                    game.make_a_move(request_json)
                    if game.is_game_end():
                        player_winner = game.get_winner()
                        player_loser = game.get_loser()
                        break
                    await game.player1.send_game_state(game.to_json())
                    await game.player2.send_game_state(game.to_json())
                elif request_json['operation'] == "surrender":
                    game = manager.find_curr_game(player.websocket)
                    if game.player1 == player:
                        await player1.send_personal_message("you_lose")
                        await player2.send_personal_message("you_win")
                        player_winner = player2
                        player_loser = player1
                        break
                    elif game.player2 == player:
                        await player1.send_personal_message("you_win")
                        await player2.send_personal_message("you_lose")
                        player_winner = player1
                        player_loser = player2
                        break
            manager.set_game_end_to_list(game)
            time_end = datetime.utcnow()
            time_length = time_end - time_start
            game_length = time_length.seconds
            rate_change_1, rate_change_2 = manager.count_rate_change(mode_id, player_winner, player_loser)
            await manager.update_users_rate_in_db(mode_id, player_winner, player_loser, rate_change_1, rate_change_2)
            await manager.add_match_to_db(mode_id, time_start, game_length, player_winner.player_id,
                                          player_loser.player_id,
                                          rate_change_1, rate_change_2)
            await manager.disconnect(player1)
            await manager.disconnect(player2)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        manager.remove_from_queues(user)
        # await manager.broadcast(f"Client #{user.id} disconnected")
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
