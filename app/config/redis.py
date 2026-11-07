from redis_fastapi.deps import AsyncClient

_redis_client: AsyncClient | None = None


def set_redis_client(client: AsyncClient) -> None:
    global _redis_client
    _redis_client = client


def get_redis_client() -> AsyncClient:
    if _redis_client is None:
        raise RuntimeError("Redis client is not initialized. Ensure lifespan has started.")
    return _redis_client
