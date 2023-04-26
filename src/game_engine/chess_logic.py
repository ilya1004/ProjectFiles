from fastapi import WebSocket
# from src.game_engine.game_manager import Player


# тут будет логика игры в шахматы которую написал Захар


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        # Инициализация шахматной доски и других параметров игры

    async def update(self, request):
        # Обновление состояния игры на основе хода игрока
        pass

    def to_json(self):
        # Преобразование объекта игры в JSON
        pass
