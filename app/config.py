from pydantic import BaseModel


class Config(BaseModel):
    DB_DSN: str = "mysql://root:password@0.0.0.0:3306/mysql"


def get_config() -> Config:
    return Config()
