from aiogram import types, Dispatcher
from aiogram.types import ContentTypes, Message
from create_bot import dp, bot
from os import path
from config import DOCUMENT_DIR


async def process_start_command(message: types.Message):
    await message.reply(f"Hello, send me something")


async def process_help_command(message: types.Message):
    await message.reply(f"Send me something and i send it back in reverse")


async def echo_message(msg: types.Message):
    print(msg)
    msg_backwards = msg.text[::-1]
    await bot.send_message(msg.from_user.id, msg_backwards)


async def check_if_file(msg: Message):
    if document := msg.document:
        print(document.file_name)
        document_path = await document.download(
            destination_dir=DOCUMENT_DIR
        )
        abs_path_for_document = document_path.name
        print(abs_path_for_document)



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(echo_message, content_types=ContentTypes.TEXT)
    dp.register_message_handler(check_if_file, content_types=ContentTypes.DOCUMENT)
