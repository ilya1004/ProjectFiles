from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.authentication.models import user
from src.api.authentication.router import is_user_in_database_by_id
from src.api.matches.models import match
from src.custom_errors import ExceptionNoUser
from src.database import get_async_session


router = APIRouter(
    prefix="/game_engine",
    tags=["Game_engine"]
)


@router.post("/update_user_rate")
async def update_user_rate(user_id: int, mode_id: int, curr_rate: int, rate_diff: int,
                           session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(user_id, int):
            raise TypeError("User ID should be int")
        if not isinstance(mode_id, int):
            raise TypeError("Mode ID should be int")
        if not isinstance(curr_rate, int) or not isinstance(rate_diff, int):
            raise TypeError("Rate should be int")
        if mode_id not in range(1, 10):
            raise ValueError("Invalid mode id")
        is_user_in_db = await is_user_in_database_by_id(user_id, session)
        if is_user_in_db["data"] == 0:
            raise ExceptionNoUser("error")
        update_query = None
        new_rate = curr_rate + rate_diff
        if mode_id in (1, 2, 3):
            update_query = user.update().where(user.c.id == user_id).values(rate_blitz=new_rate)
        elif mode_id in (4, 5, 6):
            update_query = user.update().where(user.c.id == user_id).values(rate_rapid=new_rate)
        elif mode_id == (7, 8, 9):
            update_query = user.update().where(user.c.id == user_id).values(rate_classical=new_rate)

        await session.execute(update_query)
        await session.commit()

        return {
            "status": "success",
            "data": new_rate,
            "details": None
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except ExceptionNoUser:
        return {
            "status": "error",
            "data": "ExceptionNoUser",
            "details": "No user in database with given id"
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


@router.post("/update_number_matches")
async def update_number_matches(user_id: int, mode_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(user_id, int):
            raise TypeError("User ID should be int")
        if not isinstance(mode_id, int):
            raise TypeError("Mode ID should be int")
        if mode_id not in range(1, 20):
            raise ValueError("Invalid mode id")
        is_user_in_db = await is_user_in_database_by_id(user_id, session)
        if is_user_in_db["data"] == 0:
            raise ExceptionNoUser("error")
        update_query = None
        if mode_id in (1, 2, 3, 11, 12, 13):
            update_query = user.update().where(user.c.id == user_id)\
                .values(number_matches_blitz=user.c.number_matches_blitz + 1)
        elif mode_id in (4, 5, 6, 14, 15, 16):
            update_query = user.update().where(user.c.id == user_id) \
                .values(number_matches_rapid=user.c.number_matches_rapid + 1)
        elif mode_id == (7, 8, 9, 17, 18, 19):
            update_query = user.update().where(user.c.id == user_id) \
                .values(number_matches_classical=user.c.number_matches_classical + 1)

        await session.execute(update_query)
        await session.commit()

        return {
            "status": "success",
            "data": user_id,
            "details": None
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except ExceptionNoUser:
        return {
            "status": "error",
            "data": "ExceptionNoUser",
            "details": "No user in database with given id"
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
    except Exception as e:
        return {
            "status": "error",
            "data": "Exception",
            "details": str(e)
        }


@router.post('/add_new_match')
async def add_new_match(mode_id: int, played_at: datetime, game_length: int,
                        player_winner_nickname: str, player_loser_nickname: str,
                        player_winner_id: int, player_loser_id: int,
                        rate_change_winner: int, rate_change_loser: int,
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
        if mode_id not in range(1, 20):
            raise ValueError("Mode ID should be in range(0, 19)")
        new_match = {
            "id": 0,
            "mode_id": mode_id,
            "played_at": played_at,
            "game_length_sec": game_length,
            "player_1_id": player_winner_id,
            "player_2_id": player_loser_id,
            "player_1_nickname": player_winner_nickname,
            "player_2_nickname": player_loser_nickname,
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
    except ValueError as e:
        return {
            "status": "error",
            "data": "ValueError",
            "details": str(e)
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }

