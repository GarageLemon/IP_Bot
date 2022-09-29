from aiogram import types, Dispatcher
from aiogram.types import ContentTypes, Message
from create_bot import dp, bot
from os import path
from config import DOCUMENT_DIR
from ip_parsers import ip_parser as ip_get


async def process_start_command(message: types.Message):
    await message.reply(f"Hello, send me something")


async def process_help_command(message: types.Message):
    await message.reply(f"Send me something and i send it back in reverse")


async def parse_message(msg: types.Message):
    parsed_ips = await ip_get.message_text_parse(msg.text)
    print(parsed_ips)
    await bot.send_message(msg.from_user.id, msg.text)


async def parse_document(msg: Message):
    if document := msg.document:
        file_name, file_extension = path.splitext(document.file_name)
        if file_extension == '.txt':
            document_path = await document.download(
                destination_dir=DOCUMENT_DIR
            )
            abs_path_for_document = document_path.name
            parsed_ips = await ip_get.file_text_parse(abs_path_for_document)
            print(parsed_ips)
        else:
            await msg.reply(f"IP bot can only parse '.txt' files, please provide one")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(parse_message, content_types=ContentTypes.TEXT)
    dp.register_message_handler(parse_document, content_types=ContentTypes.DOCUMENT)
