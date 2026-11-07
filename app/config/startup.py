from contextlib import asynccontextmanager
from types import SimpleNamespace

from fastapi import FastAPI
from redis_fastapi import get_async_redis
from redis_fastapi.deps import AsyncClient

from config.redis import set_redis_client
from services.email_cache_service import update_emails


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis: AsyncClient = await get_async_redis(SimpleNamespace(app=app))
    set_redis_client(redis)
    await update_emails()

    yield
