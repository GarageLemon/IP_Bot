from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from os import getenv


bot = Bot(token=str(getenv('API_TOKEN')))
dp = Dispatcher(bot)


