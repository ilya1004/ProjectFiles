from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.authentication.base_config import current_user
from src.api.authentication.models import User
from src.api.authentication.utils import ExceptionUnauthorized, ExceptionNoUser
from src.database import get_async_session
from src.api.matches.models import match, mode
from src.api.matches.schemas import MatchCreate, ModeCreate
from src.api.authentication.router import is_user_in_database_by_id

router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)


# вернет последние n матчей (если n == -1, то вернет все матчи), начиная с матча с номером offset
@router.get("/get_matches_by_user_id")
async def get_matches_by_user_id(user_id: int, number_of_matches: int = -1, offset: int = 0,
                                 session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(user_id, int):
            raise TypeError("User ID should be int")
        if not isinstance(number_of_matches, int):
            raise TypeError("Number of matches should be int")
        if not isinstance(offset, int):
            raise TypeError("Offset should be int")
        if number_of_matches <= 0:
            raise ValueError("Number of matches should be > 0")
        if is_user_in_database_by_id(user_id) == 0:
            raise ExceptionNoUser("Error")

        if number_of_matches == -1:
            query = select(match).where((match.c.player_1_id == user_id) | (match.c.player_2_id == user_id))
        else:
            query = select(match).where((match.c.player_1_id == user_id) | (match.c.player_2_id == user_id)) \
                .order_by(match.c.id.desc()).offset(offset).limit(number_of_matches)
        result = await session.execute(query)
        lst = ["id", "mode_id", "played_at", "game_length_sec",
               "player_1_id", "player_2_id", "rate_change_1", "rate_change_2"]
        list_res = list()
        for tup in result:
            list_res.append(dict(zip(lst, tup)))
        return {
            "status": "success",
            "data": list_res,
            "details": None
        }
    except ExceptionNoUser:
        return {
            "status": "error",
            "data": "ExceptionNoUser",
            "details": f"No user in database with ID = {user_id}"
        }
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


# вернет последние n матчей (если n == -1, то вернет все матчи), начиная с матча с номером offset
@router.get("/get_matches_of_current_user")
async def get_matches_of_current_user(number_of_matches: int = -1, offset: int = 0,
                                      user: User = Depends(current_user),
                                      session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(number_of_matches, int):
            raise TypeError("Number of matches should be int")
        if not isinstance(offset, int):
            raise TypeError("Offset should be int")
        if number_of_matches <= 0:
            raise ValueError("Number of matches should be > 0")
        if offset < 0:
            raise ValueError("Offset should be >= 0")
        if isinstance(user, int) and user == 401:
            raise ExceptionUnauthorized("Error")

        if number_of_matches == -1:
            query = select(match).where((match.c.player_1_id == user.id) | (match.c.player_2_id == user.id))
        else:
            query = select(match).where((match.c.player_1_id == user.id) | (match.c.player_2_id == user.id)) \
                .order_by(match.c.id.desc()).offset(offset).limit(number_of_matches)
        result = await session.execute(query)
        lst = ["id", "mode_id", "played_at", "game_length_sec",
               "player_1_id", "player_2_id", "rate_change_1", "rate_change_2"]
        list_res = list()
        for tup in result:
            list_res.append(dict(zip(lst, tup)))
        return {
            "status": "success",
            "data": list_res,
            "details": None
        }
    except ExceptionUnauthorized:
        return {
            "status": "error",
            "data": "ExceptionUnauthorized",
            "details": "User is unauthorized"
        }
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


# вернет последние n матчей (если n == -1, то вернет все матчи), начиная с матча с номером offset
@router.get('/get_all_matches')
async def get_all_matches(number_of_matches: int = -1, offset: int = 0,
                          session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(number_of_matches, int):
            raise TypeError("Number of matches should be int")
        if not isinstance(offset, int):
            raise TypeError("Offset should be int")
        if number_of_matches <= 0:
            raise ValueError("Number of matches should be > 0")
        if offset < 0:
            raise ValueError("Offset should be >= 0")

        query = select(match)
        result = await session.execute(query)
        lst = ["id", "mode_id", "played_at", "game_length_sec",
               "player_1_id", "player_2_id", "rate_change_1", "rate_change_2"]
        list_res = list()
        for tup in result:
            list_res.append(dict(zip(lst, tup)))
        return {
            "status": "success",
            "data": list_res,
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


@router.get('/get_all_modes')
async def get_all_modes(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(mode)
        result = await session.execute(query)
        lst = ["id", "name", "mode_length_sec"]
        list_res = list()
        for tup in result:
            list_res.append(dict(zip(lst, tup)))
        return {
            "status": "success",
            "data": list_res,
            "details": None
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }


@router.post('/add_new_match')
async def add_new_match(mode_id: int, played_at: datetime, game_length: int, player_winner_id: int,
                        player_loser_id: int, rate_change_1: int, rate_change_2: int,
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
        if not isinstance(rate_change_1, int) or not isinstance(rate_change_2, int):
            raise TypeError("Rate_change should be int")

        new_match = {
            "id": 0,
            "mode_id": mode_id,
            "played_at": played_at,
            "game_length_sec": game_length,
            "player_1_id": player_winner_id,
            "player_2_id": player_loser_id,
            "rate_change_player_1": rate_change_1,
            "rate_change_player_2": rate_change_2
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


@router.post('/add_mode')
async def add_mode(new_mode: ModeCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(mode).values(**new_mode.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": new_mode.dict(),
            "details": None
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }