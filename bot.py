from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(f"Hello, send me something")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(f"Send me something and i send it back in reverse")


@dp.message_handler()
async def echo_message(msg: types.Message):
    msg_backwards = msg.text[::-1]
    await bot.send_message(msg.from_user.id, msg_backwards)


if __name__ == '__main__':
    executor.start_polling(dp)