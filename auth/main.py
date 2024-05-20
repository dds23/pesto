from fastapi import FastAPI
from routes import router as auth_router
from config import settings
from models import Base
from database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router, prefix="/api/auth")

if __name__ == "__main__":
    import os
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT,
                reload=True, reload_dirs=[os.path.dirname(__file__)])
