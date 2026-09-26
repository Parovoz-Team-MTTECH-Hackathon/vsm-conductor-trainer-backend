from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import ADMIN_EMAIL, ADMIN_PASSWORD
from app.routers import *
from app.database import engine, SessionLocal
from app.models import Base
from app.services.auth import AuthService


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

application.include_router(auth.router)