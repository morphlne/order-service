from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.db import SessionLocal
from services.user_service import update_emails


@asynccontextmanager
async def lifespan(app: FastAPI):
    with SessionLocal() as db:
        update_emails(db)

    yield
