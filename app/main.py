from fastapi import FastAPI

from controllers.order_controller import router as order_router
from controllers.user_controller import router as user_router

app = FastAPI()

app.include_router(
    user_router,
    tags=["Users"]
)
app.include_router(
    order_router,
    tags=["Orders"]
)
