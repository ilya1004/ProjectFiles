from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.authentication.base_config import current_user
from src.api.authentication.models import User, user
from src.custom_errors import ExceptionUnauthorized, ExceptionNoUser
from src.database import get_async_session
from src.api.matches.models import match, mode
from src.api.matches.schemas import ModeCreate
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
        if number_of_matches <= 0 and number_of_matches != -1:
            raise ValueError("Number of matches should be > 0")
        is_user_in_db = await is_user_in_database_by_id(user_id, session)
        if is_user_in_db["data"] == 0:
            raise ExceptionNoUser("Error")

        if number_of_matches == -1:
            query = select(match).where((match.c.player_1_id == user_id) | (match.c.player_2_id == user_id))
        else:
            query = select(match).where((match.c.player_1_id == user_id) | (match.c.player_2_id == user_id)) \
                .order_by(match.c.id.desc()).offset(offset).limit(number_of_matches)
        result = await session.execute(query)
        lst = ["id", "mode_id", "played_at", "game_length_sec", "player_1_nickname", "player_2_nickname",
               "player_1_id", "player_2_id", "rate_change_1", "rate_change_2"]
        list_res = [dict(zip(lst, row)) for row in result.all()]
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
        if number_of_matches <= 0 and number_of_matches != -1:
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
        lst = ["id", "mode_id", "played_at", "game_length_sec", "player_1_id", "player_2_id",
               "player_1_nickname", "player_2_nickname", "rate_change_player_1", "rate_change_player_2"]
        list_res = [dict(zip(lst, row)) for row in result.all()]
        return {
            "status": "success",
            "data": list_res,
            "details": None
        }
    except ExceptionUnauthorized:
        return {
            "status": "error",
            "data": "ExceptionUnauthorized",
            "details": "User is not authorized"
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
@router.get("/get_all_matches")
async def get_all_matches(number_of_matches: int = -1, offset: int = 0,
                          session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(number_of_matches, int):
            raise TypeError("Number of matches should be int")
        if not isinstance(offset, int):
            raise TypeError("Offset should be int")
        if number_of_matches <= 0 and number_of_matches != -1:
            raise ValueError("Number of matches should be > 0")
        if offset < 0:
            raise ValueError("Offset should be >= 0")

        if number_of_matches == -1:
            query = select(match)
        else:
            query = select(match).order_by(match.c.id.desc()).offset(offset).limit(number_of_matches)
        result = await session.execute(query)
        lst = ["id", "mode_id", "played_at", "game_length_sec", "player_1_nickname", "player_2_nickname",
               "player_1_id", "player_2_id", "rate_change_1", "rate_change_2"]
        list_res = [dict(zip(lst, row)) for row in result.all()]
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


@router.get("/get_all_modes")
async def get_all_modes(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(mode)
        result = await session.execute(query)
        lst = ["id", "name", "mode_length_sec"]
        list_res = [dict(zip(lst, row)) for row in result.all()]
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


@router.post("/add_mode")
async def add_mode(new_mode: ModeCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(mode).values(**new_mode.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": new_mode.id,
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


@router.get("/update_winrate_by_user_id")
async def update_winrate_by_user_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(user_id, int):
            raise TypeError("User ID should be int")
        is_user_in_db = await is_user_in_database_by_id(user_id, session)
        if is_user_in_db["data"] == 0:
            raise ExceptionNoUser("error")

        query0 = select(user.c.id, user.c.number_matches_blitz, user.c.number_matches_rapid,
                        user.c.number_matches_classical).where(user.c.id == user_id)
        result0 = await session.execute(query0)
        lst0 = ["id", "number_matches_blitz", "number_matches_rapid", "number_matches_classical"]
        list_res_temp = [dict(zip(lst0, row)) for row in result0.all()]
        dict_res_counts = list_res_temp[0]

        lst = ["id"]
        query1 = select(match.c.id).where((match.c.player_1_id == user_id)  # находим победные матчи в blitz
                                          & ((match.c.mode_id == 1) | (match.c.mode_id == 2) | (match.c.mode_id == 3) |
                                             (match.c.mode_id == 11) | (match.c.mode_id == 12) | (
                                                         match.c.mode_id == 13)))
        result1 = await session.execute(query1)
        list_res_blitz = [dict(zip(lst, row)) for row in result1.all()]
        number_matches_blitz = len(list_res_blitz)

        query2 = select(match.c.id).where((match.c.player_1_id == user_id)  # находим победные матчи в rapid
                                          & ((match.c.mode_id == 4) | (match.c.mode_id == 5) | (match.c.mode_id == 6) |
                                             (match.c.mode_id == 14) | (match.c.mode_id == 15) | (
                                                         match.c.mode_id == 16)))
        result2 = await session.execute(query2)
        list_res_rapid = [dict(zip(lst, row)) for row in result2.all()]
        number_matches_rapid = len(list_res_rapid)

        query3 = select(match.c.id).where((match.c.player_1_id == user_id)  # находим победные матчи в classical
                                          & ((match.c.mode_id == 7) | (match.c.mode_id == 8) | (match.c.mode_id == 9) |
                                             (match.c.mode_id == 17) | (match.c.mode_id == 18) | (
                                                         match.c.mode_id == 19)))
        result3 = await session.execute(query3)
        list_res_classical = [dict(zip(lst, row)) for row in result3.all()]
        number_matches_classical = len(list_res_classical)

        winrate_blitz, winrate_rapid, winrate_classical = 0, 0, 0
        if dict_res_counts["number_matches_blitz"] > 0:
            winrate_blitz = int((number_matches_blitz / dict_res_counts["number_matches_blitz"]) * 100)
        if dict_res_counts["number_matches_rapid"] > 0:
            winrate_rapid = int((number_matches_rapid / dict_res_counts["number_matches_rapid"]) * 100)
        if dict_res_counts["number_matches_classical"] > 0:
            winrate_classical = int((number_matches_classical / dict_res_counts["number_matches_classical"]) * 100)

        stmt = user.update().where(user.c.id == user_id) \
            .values(winrate_blitz=winrate_blitz, winrate_rapid=winrate_rapid, winrate_classical=winrate_classical)
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "success",
            "data": winrate_blitz + winrate_rapid + winrate_classical,
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
