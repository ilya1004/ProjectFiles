from fastapi import FastAPI

from src.authentication.base_config import auth_backend, fastapi_users
from src.authentication.schemas import UserRead, UserCreate
from src.matches.router import router as router_matches

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

app.include_router(router_matches)
