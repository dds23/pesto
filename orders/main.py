from fastapi import FastAPI
from routes import router as order_router
from database import engine
from models import Base
from config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(order_router, prefix="/api/orders")

if __name__ == "__main__":
    import os
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT,
                reload=True, reload_dirs=[os.path.dirname(__file__)])
