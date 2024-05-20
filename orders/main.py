from fastapi import FastAPI
from orders.routes import router as order_router
from orders.database import engine
from orders.models import Base
from orders.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(order_router, prefix="/api/orders")

if __name__ == "__main__":
    import os
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT,
                reload=True, reload_dirs=[os.path.dirname(__file__)])
