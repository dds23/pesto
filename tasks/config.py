from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8003
    DATABASE_URL: str
    SECRET_KEY: str = '099c3f0276df115c20d86e573e34bea74c331ca876a78efcdf3da7baf3cb12d0'

    class Config:
        env_file = ".env"

settings = Settings()
