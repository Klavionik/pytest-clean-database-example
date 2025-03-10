from pydantic import BaseModel


class Config(BaseModel):
    DB_DSN: str = "postgresql://postgres:password@0.0.0.0:5432/postgres"


def get_config() -> Config:
    return Config()
