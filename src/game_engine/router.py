from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.authentication.models import user
from src.api.matches.models import match
from src.database import get_async_session


router = APIRouter(
    prefix="/matches",
    tags=["Game_engine"]
)


@router.post('/update_user_rate')
async def update_user_rate(user_id: int, mode_id: int, curr_rate: int, rate_diff: int,
                           session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(mode_id, int):
            raise TypeError("Mode ID should be int")
        if mode_id not in range(0, 9):
            raise ValueError("Invalid mode name")
        update_query = None
        new_rate = curr_rate + rate_diff
        if mode_id in (0, 1, 2):
            update_query = user.update().where(user.c.id == user_id).values(rate_blitz=new_rate)
        elif mode_id in (3, 4, 5):
            update_query = user.update().where(user.c.id == user_id).values(rate_rapid=new_rate)
        elif mode_id == (6, 7, 8):
            update_query = user.update().where(user.c.id == user_id).values(rate_classical=new_rate)

        await session.execute(update_query)
        await session.commit()

        return {"status": "success"}
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


@router.post('/add_new_match')
async def add_new_match(mode_id: int, played_at: datetime, game_length: int, player_winner_id: int,
                        player_loser_id: int, rate_change_winner: int, rate_change_loser: int,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(mode_id, int):
            raise TypeError("Mode ID should be int")
        if not isinstance(played_at, datetime):
            raise TypeError("Played_at should be datetime")
        if not isinstance(game_length, int):
            raise TypeError("Game length should be int")
        if not isinstance(player_winner_id, int) or not isinstance(player_loser_id, int):
            raise TypeError("Player ID should be int")
        if not isinstance(rate_change_winner, int) or not isinstance(rate_change_loser, int):
            raise TypeError("Rate_change should be int")

        new_match = {
            "id": 0,
            "mode_id": mode_id,
            "played_at": played_at,
            "game_length_sec": game_length,
            "player_1_id": player_winner_id,
            "player_2_id": player_loser_id,
            "rate_change_player_1": rate_change_winner,
            "rate_change_player_2": rate_change_loser
        }
        stmt = insert(match).values(**new_match)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": new_match,
            "details": None
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
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