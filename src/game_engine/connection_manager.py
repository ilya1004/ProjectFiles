from datetime import datetime
from src.game_engine.chess_logic import Game
from src.game_engine.player import Player
from src.game_engine.router import update_user_rate, add_new_match
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.rate_diff = 100
        self.active_connections: list[WebSocket] = []
        self.games_list_rate: dict[Game, bool] = {}
        self.games_list_unrate: dict[Game, bool] = {}

        self.queue_blitz_rate: list[list[Player], list[Player], list[Player]] = []
        self.queue_rapid_rate: list[list[Player], list[Player], list[Player]] = []
        self.queue_classical_rate: list[list[Player], list[Player], list[Player]] = []

        self.queue_blitz_unrate: list[list[Player], list[Player], list[Player]] = []
        self.queue_rapid_unrate: list[list[Player], list[Player], list[Player]] = []
        self.queue_classical_unrate: list[list[Player], list[Player], list[Player]] = []

    def add_player_to_queue(self, player: Player):
        if player.mode_id in (0, 1, 2):
            self.queue_blitz_rate[player.mode_id].append(player)
        elif player.mode_id in (3, 4, 5):
            self.queue_rapid_rate[player.mode_id % 3].append(player)
        elif player.mode_id in (6, 7, 8):
            self.queue_classical_rate[player.mode_id % 3].append(player)
        elif player.mode_id in (10, 11, 12):
            self.queue_blitz_unrate[(player.mode_id - 1) % 3].append(player)
        elif player.mode_id in (13, 14, 15):
            self.queue_rapid_unrate[(player.mode_id - 1) % 3].append(player)
        elif player.mode_id in (16, 17, 18):
            self.queue_classical_unrate[(player.mode_id - 1) % 3].append(player)

    def add_game_to_list(self, game: Game):
        if game.is_rated:
            self.games_list_rate[game] = True
        else:
            self.games_list_unrate[game] = True

    def set_game_end_to_list(self, game: Game):
        if game.is_rated:
            self.games_list_rate[game] = False
        else:
            self.games_list_unrate[game] = False

    async def find_new_game(self, mode_id: int) -> (Player, Player):
        if mode_id in (0, 1, 2):
            if len(self.queue_blitz_rate[mode_id]) <= 1:
                return None, None
            self.queue_blitz_rate[mode_id].sort(key=self.rate_compare_blitz)
            for i in range(len(self.queue_blitz_rate[mode_id]) - 1):
                if abs(self.queue_blitz_rate[mode_id][i].rate_blitz -
                       self.queue_blitz_rate[mode_id][i + 1].rate_blitz) <= self.rate_diff:
                    await self.queue_blitz_rate[mode_id][i].send_message(
                        f"You will play with player #{self.queue_blitz_rate[mode_id][i + 1].player_id}")
                    await self.queue_blitz_rate[mode_id][i + 1].send_message(
                        f"You will play with player #{self.queue_blitz_rate[mode_id][i].player_id}")
                    return self.queue_blitz_rate[mode_id][i], self.queue_blitz_rate[mode_id][i + 1]
        elif mode_id in (3, 4, 5):
            mode_id %= 3
            if len(self.queue_rapid_rate[mode_id]) <= 1:
                return None, None
            self.queue_rapid_rate[mode_id].sort(key=self.rate_compare_rapid)
            for i in range(len(self.queue_rapid_rate[mode_id]) - 1):
                if abs(self.queue_rapid_rate[mode_id][i].rate_rapid -
                       self.queue_rapid_rate[mode_id][i + 1].rate_rapid) <= self.rate_diff:
                    await self.queue_rapid_rate[mode_id][i].send_message(
                        f"You will play with player #{self.queue_rapid_rate[mode_id][i + 1].player_id}")
                    await self.queue_rapid_rate[mode_id][i + 1].send_message(
                        f"You will play with player #{self.queue_rapid_rate[mode_id][i].player_id}")
                    return self.queue_rapid_rate[mode_id][i], self.queue_rapid_rate[mode_id][i + 1]
        elif mode_id in (6, 7, 8):
            mode_id %= 3
            if len(self.queue_classical_rate[mode_id]) <= 1:
                return None, None
            self.queue_classical_rate[mode_id].sort(key=self.rate_compare_classical)
            for i in range(len(self.queue_classical_rate[mode_id]) - 1):
                if abs(self.queue_classical_rate[mode_id][i].rate_classical -
                       self.queue_classical_rate[mode_id][i + 1].rate_classical) <= self.rate_diff:
                    await self.queue_classical_rate[mode_id][i].send_message(
                        f"You will play with player #{self.queue_classical_rate[mode_id][i + 1].player_id}")
                    await self.queue_classical_rate[mode_id][i + 1].send_message(
                        f"You will play with player #{self.queue_classical_rate[mode_id][i].player_id}")
                    return self.queue_classical_rate[mode_id][i], self.queue_classical_rate[mode_id][i + 1]
        elif mode_id in (10, 11, 12):
            mode_id = (mode_id - 1) % 3
            if len(self.queue_blitz_unrate[mode_id]) <= 1:
                return None, None
            else:
                await self.queue_blitz_unrate[mode_id][0].send_message(
                    f"You will play with player #{self.queue_blitz_unrate[mode_id][1].player_id}")
                await self.queue_blitz_unrate[mode_id][1].send_message(
                    f"You will play with player #{self.queue_blitz_unrate[mode_id][0].player_id}")
                return self.queue_blitz_unrate[mode_id][0], self.queue_blitz_unrate[mode_id][1]
        elif mode_id in (13, 14, 15):
            mode_id = (mode_id - 1) % 3
            if len(self.queue_rapid_unrate[mode_id]) <= 1:
                return None, None
            else:
                await self.queue_rapid_unrate[mode_id][0].send_message(
                    f"You will play with player #{self.queue_rapid_unrate[mode_id][1].player_id}")
                await self.queue_rapid_unrate[mode_id][1].send_message(
                    f"You will play with player #{self.queue_rapid_unrate[mode_id][0].player_id}")
                return self.queue_rapid_unrate[mode_id][0], self.queue_rapid_unrate[mode_id][1]
        elif mode_id in (16, 17, 18):
            mode_id = (mode_id - 1) % 3
            if len(self.queue_classical_unrate[mode_id]) <= 1:
                return None, None
            else:
                await self.queue_classical_unrate[mode_id][0].send_message(
                    f"You will play with player #{self.queue_classical_unrate[mode_id][1].player_id}")
                await self.queue_classical_unrate[mode_id][1].send_message(
                    f"You will play with player #{self.queue_classical_unrate[mode_id][0].player_id}")
                return self.queue_classical_unrate[mode_id][0], self.queue_classical_unrate[mode_id][1]

    async def connect_user(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect_user(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            await websocket.close()

    def remove_player_from_queues(self, player: Player):
        if player.mode_id in (0, 1, 2) and player in self.queue_blitz_rate[player.mode_id]:
            self.queue_blitz_rate[player.mode_id].remove(player)
        elif player.mode_id in (3, 4, 5) and player in self.queue_rapid_rate[player.mode_id % 3]:
            self.queue_rapid_rate[player.mode_id % 3].remove(player)
        elif player.mode_id in (6, 7, 8) and player in self.queue_classical_rate[player.mode_id % 3]:
            self.queue_rapid_rate[player.mode_id % 3].remove(player)
        elif player.mode_id in (10, 11, 12) and player in self.queue_blitz_unrate[(player.mode_id - 1) % 3]:
            self.queue_blitz_unrate[(player.mode_id - 1) % 3].remove(player)
        elif player.mode_id in (13, 14, 15) and player in self.queue_rapid_unrate[(player.mode_id - 1) % 3]:
            self.queue_rapid_unrate[(player.mode_id - 1) % 3].remove(player)
        elif player.mode_id in (16, 17, 18) and player in self.queue_classical_unrate[(player.mode_id - 1) % 3]:
            self.queue_rapid_unrate[(player.mode_id - 1) % 3].remove(player)

    def delete_game_from_list(self, game: Game):
        if game.is_rated:
            if game in self.games_list_rate.keys():
                del self.games_list_rate[game]
        else:
            if game in self.games_list_unrate.keys():
                del self.games_list_unrate[game]

    def clear_ended_games(self):
        for key, value in self.games_list_rate.items():
            if value is False:
                del self.games_list_rate[key]
        for key, value in self.games_list_unrate.items():
            if value is False:
                del self.games_list_unrate[key]

    def find_curr_game(self, player: Player) -> Game | None:
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
    async def add_match_to_db(mode_id: int, played_at: datetime, game_length: int, player_winner_id: int,
                              player_loser_id: int, rate_change_winner: int, rate_change_loser: int):
        await add_new_match(mode_id, played_at, game_length, player_winner_id,
                            player_loser_id, rate_change_winner, rate_change_loser)

    @staticmethod
    def rate_compare_blitz(player: Player):
        return player.rate_blitz

    @staticmethod
    def rate_compare_rapid(player: Player):
        return player.rate_rapid

    @staticmethod
    def rate_compare_classical(player: Player):
        return player.rate_classical

    @staticmethod
    def count_rate_change(player_winner: Player, player_loser: Player) -> (int, int):
        # изменение рейтинга победителя, рейтинга проигравшего
        base_change = 20
        coef_change = 0.2
        if player_winner.mode_id in (0, 1, 2):
            rate_change = int(base_change + coef_change*abs(player_winner.rate_blitz - player_loser.rate_blitz))
            return rate_change, -rate_change
        elif player_winner.mode_id in (3, 4, 5):
            rate_change = int(base_change + coef_change*abs(player_winner.rate_rapid - player_loser.rate_rapid))
            return rate_change, -rate_change
        elif player_winner.mode_id in (6, 7, 8):
            rate_change = int(base_change + coef_change*abs(player_winner.rate_blitz - player_loser.rate_blitz))
            return rate_change, -rate_change

    @staticmethod
    async def update_users_rate_in_db(mode_id: int, player_winner: Player, player_loser: Player,
                                      rate_change_winner: int, rate_change_loser: int):
        if mode_id in (0, 1, 2):
            await update_user_rate(player_winner.player_id, mode_id, player_winner.rate_blitz, rate_change_winner)
            await update_user_rate(player_loser.player_id, mode_id, player_loser.rate_blitz, rate_change_loser)
        elif mode_id in (3, 4, 5):
            await update_user_rate(player_winner.player_id, mode_id, player_winner.rate_rapid, rate_change_winner)
            await update_user_rate(player_loser.player_id, mode_id, player_loser.rate_rapid, rate_change_loser)
        elif mode_id in (6, 7, 8):
            await update_user_rate(player_winner.player_id, mode_id, player_winner.rate_classical, rate_change_winner)
            await update_user_rate(player_loser.player_id, mode_id, player_loser.rate_classical, rate_change_loser)
