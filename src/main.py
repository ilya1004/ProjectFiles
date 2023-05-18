import uvicorn
from fastapi import FastAPI
from src.api.authentication.base_config import auth_backend, fastapi_users
from src.api.authentication.schemas import UserRead, UserCreate
from src.api.matches.router import router as router_matches
from src.api.authentication.router import router as router_user
from src.game_engine.router import router as router_game_engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Belchessmind.org"
)

origins = ["http://localhost",
           "http://localhost:3000",
           "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
