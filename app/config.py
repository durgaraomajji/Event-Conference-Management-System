from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Event & Conference Management System"
    DATABASE_URL: str = "mysql+pymysql://root:Root123@localhost:3306/event_management"
    SECRET_KEY: str = "change-this-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()