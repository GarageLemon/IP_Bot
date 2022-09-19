from aiogram import types, Dispatcher
from create_bot import dp, bot


async def process_start_command(message: types.Message):
    await message.reply(f"Hello, send me something")


async def process_help_command(message: types.Message):
    await message.reply(f"Send me something and i send it back in reverse")


async def echo_message(msg: types.Message):
    print(msg)
    msg_backwards = msg.text[::-1]
    await bot.send_message(msg.from_user.id, msg_backwards)


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(echo_message)
