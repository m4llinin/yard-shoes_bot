import logging

from aiogram import Bot, Dispatcher
from dataclasses import dataclass
import betterlogging as bl
import pytz

from environs import Env


@dataclass
class Config:
    bot: Bot
    dp: Dispatcher
    logger: bl.Logger
    AmoCRM: str
    tz: pytz.utc


env = Env()
env.read_env("./config/.env")

logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)

config = Config(bot=Bot(token=env.str("TELEGRAM_TOKEN")),
                dp=Dispatcher(),
                logger=logger,
                AmoCRM=env.str("AMOCRM_TOKEN"),
                tz=pytz.timezone("Europe/Moscow"))
