from fastapi import FastAPI, Depends
from src.api.authentication.base_config import auth_backend, fastapi_users, current_user
from src.api.authentication.models import User
from src.api.authentication.schemas import UserRead, UserCreate
from src.api.matches.router import router as router_matches
from src.api.authentication.router import router as router_user
from src.game_engine.game_manager import router as router_game_engine

app = FastAPI(
    title="Сайт для секса"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_user)
app.include_router(router_matches)
app.include_router(router_game_engine)
