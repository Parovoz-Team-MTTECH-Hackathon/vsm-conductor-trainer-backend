from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.config import ADMIN_EMAIL, ADMIN_PASSWORD
from app.routers import *
from app.database import engine, SessionLocal
from app.models import Base
from app.services.auth import AuthService
from fastapi.staticfiles import StaticFiles  # Импорт



@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:
        await AuthService(session).signup_admin(ADMIN_EMAIL, ADMIN_PASSWORD)
    yield


application = FastAPI(
    lifespan=lifespan,
    title="VSM Conductor Trainer",
    description="API Геймифицированной системы обучения проводников ВСМ от команды \"ПАРАВОЗ\" хакатона Московского Транспорта"
)

static_files = StaticFiles(directory="static")
application.mount("/static", static_files, name="static")


application.include_router(auth.router)
application.include_router(admin.router)
application.include_router(player.router)
application.include_router(manager.router)
application.include_router(integration.router)
application.include_router(scenario.router)

@application.get("/")
async def index():
    return RedirectResponse("/static/index.html")