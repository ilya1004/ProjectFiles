from fastapi import WebSocket


class Player:
    def __init__(self, websocket: WebSocket, player_id: int, player_nickname,
                 rate_blitz: int, rate_rapid: int, rate_classical: int, mode_id: int, is_rate: bool):
        self.websocket = websocket
        self.player_id = player_id
        self.player_nickname = player_nickname
        self.rate_blitz = rate_blitz
        self.rate_rapid = rate_rapid
        self.rate_classical = rate_classical
        self.mode_id = mode_id
        self.is_rated_mode = is_rate

    async def send_game_state(self, game: dict):
        await self.websocket.send_json(game)

    async def send_message(self, message: str):
        await self.websocket.send_text(message)

    async def get_json(self) -> dict:
        return await self.websocket.receive_json(mode="text")
