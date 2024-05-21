from fastapi import FastAPI, HTTPException, Response, status
from orders.routes import router as order_router
from orders.database import engine
from orders.models import Base
from orders.config import settings
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from starlette.requests import Request
from math import ceil


Base.metadata.create_all(bind=engine)

# Redis integration to keep track of the requests to enable rate limiting
REDIS_URL = "redis://localhost"

# this function will indentify different services based on which rate limiting will be applied on each of them
async def service_name_identifier(request: Request):
    service = request.headers.get("Service-Name")
    return service


async def custom_callback(request: Request, response: Response, pexpire: int):
    """
    default callback when too many requests
    :param request:
    :param pexpire: The remaining seconds
    :param response:
    :return:
    """
    expire = ceil(pexpire / 1000)

    raise HTTPException(
        status.HTTP_429_TOO_MANY_REQUESTS,
        f"Too Many Requests. Retry after {expire} seconds.",
        headers={"Retry-After": str(expire)},
    )

# lifespan function to pass to the fastapi instance to enable rate limiting logic
@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url(REDIS_URL, encoding="utf8")
    await FastAPILimiter.init(
        redis=redis_connection,
        identifier=service_name_identifier,
        http_callback=custom_callback,
    )
    yield
    await FastAPILimiter.close()

app = FastAPI(lifespan=lifespan)
app.include_router(order_router, prefix="/api/orders")

if __name__ == "__main__":
    import os
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT,
                reload=True, reload_dirs=[os.path.dirname(__file__)])
