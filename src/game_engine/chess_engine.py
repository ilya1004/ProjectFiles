from datetime import datetime
from src.game_engine.player import Player


# тут будет логика игры в шахматы которую написал Захар


class Game:
    def __init__(self, player1: Player, player2: Player, mode_id: int, time_start: datetime, is_rated: bool):
        self.player1 = player1
        self.player2 = player2
        self.mode_id = mode_id
        self.time_start = time_start
        self.is_rated = is_rated
        # Инициализация шахматной доски и других параметров игры

    def make_a_move(self, request: dict):
        pass
    def is_game_end(self):
        # возвращает True если последний ход привел к завершению партии
        pass
    def get_winner(self):
        # возвращает объект Player того кто выйграл
        pass
    def get_loser(self):
        # возвращает объект Player того кто проиграл
        pass
    def to_json(self):
        # Преобразование объекта игры в JSON (словарь)
        pass
    def get_id_player_to_move(self):
        # Вовзращает 1 или 2 в зависимости от того, чей ход (1го игрока или 2го)
        pass
