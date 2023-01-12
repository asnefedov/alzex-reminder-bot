from environs import Env
from dataclasses import dataclass


@dataclass
class BotConfig:
    token: str


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int


@dataclass
class Config:
    bot: BotConfig
    db: DbConfig


def load_config():
    env = Env()
    env.read_env('.env')
    return Config(
        bot=BotConfig(
            token=env.str('BOT_TOKEN')
        ),
        db=DbConfig(
            host=env.str('POSTGRES_HOST'),
            user=env.str('POSTGRES_USER'),
            password=env.str('POSTGRES_PASSWORD'),
            database=env.str('POSTGRES_DB'),
            port=env.int('POSTGRES_PORT')
        )
    )
