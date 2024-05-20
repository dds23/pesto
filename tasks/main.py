from fastapi import FastAPI, HTTPException
from routes import router as tasks_router
from config import settings
from database import engine
from models import Base
from starlette.responses import JSONResponse
from starlette.requests import Request


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(tasks_router, prefix="/api/tasks")

if __name__ == "__main__":
    import os
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT,
                reload=True, reload_dirs=[os.path.dirname(__file__)])
