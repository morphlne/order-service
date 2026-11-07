from fastapi import FastAPI
from redis_fastapi import FastAPIRedis

from config.startup import lifespan
from controllers.order_controller import router as order_router
from controllers.user_controller import router as user_router

app = FastAPI(
    title="Order-service",
    lifespan=lifespan
)

FastAPIRedis(app).lifespan()

app.include_router(
    user_router,
    tags=["Users"]
)
app.include_router(
    order_router,
    tags=["Orders"]
)
