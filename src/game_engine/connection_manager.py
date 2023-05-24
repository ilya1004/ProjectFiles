from datetime import datetime
from src.game_engine.chess_engine import Game
from src.game_engine.player import Player
from src.game_engine.router import update_user_rate, add_new_match
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.rate_diff = 100
        self.active_connections: list[WebSocket] = []
        self.games_list_rate: dict[Game, bool] = {}
        self.games_list_unrate: dict[Game, bool] = {}

        self.queue_blitz_rate: list[list[Player], list[Player], list[Player]] = [[], [], []]
        self.queue_rapid_rate: list[list[Player], list[Player], list[Player]] = [[], [], []]
        self.queue_classical_rate: list[list[Player], list[Player], list[Player]] = [[], [], []]

        self.queue_blitz_unrate: list[list[Player], list[Player], list[Player]] = [[], [], []]
        self.queue_rapid_unrate: list[list[Player], list[Player], list[Player]] = [[], [], []]
        self.queue_classical_unrate: list[list[Player], list[Player], list[Player]] = [[], [], []]

    async def add_player_to_queue(self, player: Player):
        if player.mode_id in (1, 2, 3):
            self.queue_blitz_rate[player.mode_id - 1].append(player)
        elif player.mode_id in (4, 5, 6):
            self.queue_rapid_rate[(player.mode_id - 1) % 3].append(player)
        elif player.mode_id in (7, 8, 9):
            self.queue_classical_rate[(player.mode_id - 1) % 3].append(player)
        elif player.mode_id in (11, 12, 13):
            self.queue_blitz_unrate[(player.mode_id - 2) % 3].append(player)
        elif player.mode_id in (14, 15, 16):
            self.queue_rapid_unrate[(player.mode_id - 2) % 3].append(player)
        elif player.mode_id in (17, 18, 19):
            self.queue_classical_unrate[(player.mode_id - 2) % 3].append(player)

    async def add_game_to_list(self, game: Game):
        if game.is_rated:
            self.games_list_rate[game] = True
        else:
            self.games_list_unrate[game] = True

    async def set_game_end_to_list(self, game: Game):
        if game.is_rated:
            self.games_list_rate[game] = False
        else:
            self.games_list_unrate[game] = False

    async def find_new_game(self, mode_id_db: int) -> (Player, Player):
        # await self.queue_blitz_unrate[0][0].websocket.send_text("find_new_game")
        print(mode_id_db)
        if mode_id_db in (1, 2, 3):
            mode_id = mode_id_db - 1
            if len(self.queue_blitz_rate[mode_id]) <= 1:
                return None, None
            self.queue_blitz_rate[mode_id].sort(key=lambda x: x.rate_blitz)
            for i in range(len(self.queue_blitz_rate[mode_id]) - 1):
                if abs(self.queue_blitz_rate[mode_id][i].rate_blitz -
                       self.queue_blitz_rate[mode_id][i + 1].rate_blitz) <= self.rate_diff:
                    await self.queue_blitz_rate[mode_id][i].websocket.send_json({
                        "status": "success",
                        "data": "Game has founded (blitz rate). Your opponent is:",
                        "details": self.queue_rapid_rate[mode_id][i + 1].player_id
                    })
                    await self.queue_blitz_rate[mode_id][i + 1].websocket.send_json({
                        "status": "success",
                        "data": "Game has founded (blitz rate). Your opponent is:",
                        "details": self.queue_rapid_rate[mode_id][i].player_id
                    })
                    return self.queue_blitz_rate[mode_id][i], self.queue_blitz_rate[mode_id][i + 1]
        elif mode_id_db in (4, 5, 6):
            mode_id = (mode_id_db - 1) % 3
            if len(self.queue_rapid_rate[mode_id]) <= 1:
                return None, None
            self.queue_rapid_rate[mode_id].sort(key=lambda x: x.rate_rapid)
            for i in range(len(self.queue_rapid_rate[mode_id]) - 1):
                if abs(self.queue_rapid_rate[mode_id][i].rate_rapid -
                       self.queue_rapid_rate[mode_id][i + 1].rate_rapid) <= self.rate_diff:
                    await self.queue_rapid_rate[mode_id][i].websocket.send_json({
                        "status": "success",
                        "data": "Game has founded (rapid rate). Your opponent is:",
                        "details": self.queue_rapid_rate[mode_id][i + 1].player_id
                    })
                    await self.queue_rapid_rate[mode_id][i + 1].websocket.send_json({
                        "status": "success",
                        "data": "Game has founded (rapid rate). Your opponent is:",
                        "details": self.queue_rapid_rate[mode_id][i].player_id
                    })
                    return self.queue_rapid_rate[mode_id][i], self.queue_rapid_rate[mode_id][i + 1]
        elif mode_id_db in (7, 8, 9):
            mode_id = (mode_id_db - 1) % 3
            if len(self.queue_classical_rate[mode_id]) <= 1:
                return None, None
            self.queue_classical_rate[mode_id].sort(key=lambda x: x.rate_classical)
            for i in range(len(self.queue_classical_rate[mode_id]) - 1):
                if abs(self.queue_classical_rate[mode_id][i].rate_classical -
                       self.queue_classical_rate[mode_id][i + 1].rate_classical) <= self.rate_diff:
                    await self.queue_classical_rate[mode_id][i].websocket.send_json({
                        "status": "success",
                        "data": "Game has founded (classical rate). Your opponent is:",
                        "details": self.queue_classical_rate[mode_id][i + 1].player_id
                    })
                    await self.queue_classical_rate[mode_id][i + 1].websocket.send_json({
                        "status": "success",
                        "data": "Game has founded (classical rate). Your opponent is:",
                        "details": self.queue_classical_rate[mode_id][i].player_id
                    })
                    return self.queue_classical_rate[mode_id][i], self.queue_classical_rate[mode_id][i + 1]
        elif mode_id_db in (11, 12, 13):
            mode_id = (mode_id_db - 2) % 3
            if len(self.queue_blitz_unrate[mode_id]) <= 1:
                return None, None
            else:
                await self.queue_blitz_unrate[mode_id][0].websocket.send_json({
                    "status": "success",
                    "data": "Game has founded (blitz unrate). Your opponent is:",
                    "details": self.queue_blitz_unrate[mode_id][1].player_id
                })
                await self.queue_blitz_unrate[mode_id][1].websocket.send_json({
                    "status": "success",
                    "data": "Game has founded (blitz unrate). Your opponent is:",
                    "details": self.queue_blitz_unrate[mode_id][0].player_id
                })
                return self.queue_blitz_unrate[mode_id][0], self.queue_blitz_unrate[mode_id][1]
        elif mode_id_db in (14, 15, 16):
            mode_id = (mode_id_db - 2) % 3
            if len(self.queue_rapid_unrate[mode_id]) <= 1:
                return None, None
            else:
                await self.queue_rapid_unrate[mode_id][0].websocket.send_json({
                    "status": "success",
                    "data": "Game has founded (rapid unrate). Your opponent is:",
                    "details": self.queue_rapid_unrate[mode_id][1].player_id
                })
                await self.queue_rapid_unrate[mode_id][1].websocket.send_json({
                    "status": "success",
                    "data": "Game has founded (rapid unrate). Your opponent is:",
                    "details": self.queue_rapid_unrate[mode_id][0].player_id
                })
                return self.queue_rapid_unrate[mode_id][0], self.queue_rapid_unrate[mode_id][1]
        elif mode_id_db in (17, 18, 19):
            mode_id = (mode_id_db - 2) % 3
            if len(self.queue_classical_unrate[mode_id]) <= 1:
                return None, None
            else:
                await self.queue_classical_unrate[mode_id][0].websocket.send_json({
                    "status": "success",
                    "data": "Game has founded (classical unrate). Your opponent is:",
                    "details": self.queue_classical_unrate[mode_id][1].player_id
                })
                await self.queue_classical_unrate[mode_id][1].websocket.send_json({
                    "status": "success",
                    "data": "Game has founded (classical unrate). Your opponent is:",
                    "details": self.queue_classical_unrate[mode_id][0].player_id
                })
                return self.queue_classical_unrate[mode_id][0], self.queue_classical_unrate[mode_id][1]

    async def connect_user(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("player is successfully connected")
        await websocket.send_json({
            "status": "success",
            "data": "player is successfully connected",
            "details": None
        })

    async def disconnect_user(self, websocket: WebSocket):
        print("player is disconnected")
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            await websocket.send_json({
                "status": "success",
                "data": "player is disconnected",
                "details": None
            })
            await websocket.close()

    async def remove_player_from_queues(self, player: Player):
        if player.mode_id in (1, 2, 3) and player in self.queue_blitz_rate[player.mode_id - 1]:
            self.queue_blitz_rate[player.mode_id - 1].remove(player)

        elif player.mode_id in (4, 5, 6) and player in self.queue_rapid_rate[(player.mode_id - 1) % 3]:
            self.queue_rapid_rate[(player.mode_id - 1) % 3].remove(player)

        elif player.mode_id in (7, 8, 9) and player in self.queue_classical_rate[(player.mode_id - 1) % 3]:
            self.queue_rapid_rate[(player.mode_id - 1) % 3].remove(player)

        elif player.mode_id in (11, 12, 13) and player in self.queue_blitz_unrate[(player.mode_id - 2) % 3]:
            self.queue_blitz_unrate[(player.mode_id - 2) % 3].remove(player)

        elif player.mode_id in (14, 15, 16) and player in self.queue_rapid_unrate[(player.mode_id - 2) % 3]:
            self.queue_rapid_unrate[(player.mode_id - 2) % 3].remove(player)

        elif player.mode_id in (17, 18, 19) and player in self.queue_classical_unrate[(player.mode_id - 2) % 3]:
            self.queue_rapid_unrate[(player.mode_id - 2) % 3].remove(player)

    async def delete_game_from_list(self, game: Game):
        if game.is_rated:
            if game in self.games_list_rate.keys():
                del self.games_list_rate[game]
        else:
            if game in self.games_list_unrate.keys():
                del self.games_list_unrate[game]

    async def clear_ended_games(self):
        for key, value in self.games_list_rate.items():
            if value is False:
                del self.games_list_rate[key]
        for key, value in self.games_list_unrate.items():
            if value is False:
                del self.games_list_unrate[key]

    async def find_curr_game(self, player: Player) -> Game | None:
        if player.is_rated_mode:
            for game in self.games_list_rate.keys():
                if game.player1 == player.websocket or game.player2 == player.websocket:
                    return game
        else:
            for game in self.games_list_unrate.keys():
                if game.player1 == player.websocket or game.player2 == player.websocket:
                    return game
        return None

    @staticmethod
    async def add_match_to_db(mode_id: int, played_at: datetime, game_length: int,
                              player_winner_nickname: str, player_loser_nickname: str,
                              player_winner_id: int, player_loser_id: int,
                              rate_change_winner: int, rate_change_loser: int):
        await add_new_match(mode_id, played_at, game_length,
                            player_winner_nickname, player_loser_nickname,
                            player_winner_id, player_loser_id,
                            rate_change_winner, rate_change_loser)


    @staticmethod
    async def count_rate_change(player_winner: Player, player_loser: Player) -> (int, int):
        # изменение рейтинга победителя, рейтинга проигравшего
        base_change = 20
        coef_change = 0.2
        if player_winner.mode_id in (1, 2, 3):
            rate_change = int(base_change + coef_change*abs(player_winner.rate_blitz - player_loser.rate_blitz))
            return rate_change, -rate_change
        elif player_winner.mode_id in (4, 5, 6):
            rate_change = int(base_change + coef_change*abs(player_winner.rate_rapid - player_loser.rate_rapid))
            return rate_change, -rate_change
        elif player_winner.mode_id in (7, 8, 9):
            rate_change = int(base_change + coef_change*abs(player_winner.rate_blitz - player_loser.rate_blitz))
            return rate_change, -rate_change

    @staticmethod
    async def update_users_rate_in_db(mode_id: int, player_winner: Player, player_loser: Player,
                                      rate_change_winner: int, rate_change_loser: int):
        if mode_id in (1, 2, 3):
            await update_user_rate(player_winner.player_id, mode_id, player_winner.rate_blitz, rate_change_winner)
            await update_user_rate(player_loser.player_id, mode_id, player_loser.rate_blitz, rate_change_loser)
        elif mode_id in (4, 5, 6):
            await update_user_rate(player_winner.player_id, mode_id, player_winner.rate_rapid, rate_change_winner)
            await update_user_rate(player_loser.player_id, mode_id, player_loser.rate_rapid, rate_change_loser)
        elif mode_id in (7, 8, 9):
            await update_user_rate(player_winner.player_id, mode_id, player_winner.rate_classical, rate_change_winner)
            await update_user_rate(player_loser.player_id, mode_id, player_loser.rate_classical, rate_change_loser)


class ConnectionManagerNew:
    def __init__(self):
        self.active_connections: dict[WebSocket, int] = dict()

    async def connect(self, websocket: WebSocket, user_id):
        await websocket.accept()
        # dct = {websocket: user_id}
        self.active_connections[websocket] = user_id

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, websocket: WebSocket, data: dict):
        for connection in self.active_connections.keys():
            if connection != websocket:
                await connection.send_json(data)

