from aiogram import types, Dispatcher
from aiogram.types import ContentTypes, Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from os import path, remove
from config import DOCUMENT_DIR, ip_info_config
from ip_parsers import ip_parser as ip_get
from ip_parsers.ip_parser import ParsedIPs
from keyboards import kb_client_ip_number_wait, kb_client_json
from get_ip.get_ip import get_all_ip_info, OneIpInfo
from json_maker.info_to_json import make_json_info, json_document_maker


class FSMParsed(StatesGroup):
    ip_number_wait = State()
    make_json_info = State()


async def process_start_command(message: types.Message):
    await message.reply(f"Hello, send me something")


async def process_help_command(message: types.Message):
    await message.reply(f"Send me something and i send it back in reverse")


async def parse_message(msg: types.Message, state: FSMContext):
    parsed_ips = await ip_get.message_text_parse(msg.text)
    async with state.proxy() as data:
        data["ip_lst"] = parsed_ips
    await show_parsed_ips(msg, parsed_ips)


async def parse_document(msg: Message, state: FSMContext):
    if document := msg.document:
        file_name, file_extension = path.splitext(document.file_name)
        if file_extension == '.txt':
            document_path = await document.download(
                destination_dir=DOCUMENT_DIR
            )
            abs_path_for_document = document_path.name
            parsed_ips = await ip_get.file_text_parse(abs_path_for_document)
            async with state.proxy() as data:
                data["ip_lst"] = parsed_ips
            await show_parsed_ips(msg, parsed_ips)
            remove(abs_path_for_document)
        else:
            await msg.reply(f"IP bot can only parse '.txt' files, please provide one")


async def show_parsed_ips(msg: types.Message, parsed_ips: ParsedIPs):
    if parsed_ips.ip_count:
        ip_for_show = [f"{ind + 1}: {x}" for ind, x in enumerate(parsed_ips.ip_lst)]
        ip_for_show.insert(0, "Found next IPs:")
        await bot.send_message(msg.from_user.id, '\n'.join(ip_for_show))
        await FSMParsed.ip_number_wait.set()
        await bot.send_message(msg.from_user.id, f"Choose a number to get info about this IP, type 'exit' to exit",
                               reply_markup=kb_client_ip_number_wait)
    else:
        await bot.send_message(msg.from_user.id, f"Don't find any valid IPs in your message or document")


async def process_ip_number_invalid(msg: types.Message):
    return await msg.reply("You need to provide a proper IP number from the list below, digits only",
                           reply_markup=kb_client_ip_number_wait)


async def process_ip_number(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        parsed_ips = data["ip_lst"]
        if int(msg.text) > parsed_ips.ip_count or int(msg.text) < 1:
            await msg.reply(f"Number is not valid, please provide valid number", reply_markup=kb_client_ip_number_wait)
        else:
            data["ip_number"] = int(msg.text)
            chosen_ip = await take_ip_by_number(parsed_ips.ip_lst, data["ip_number"])
            ip_info = await get_all_ip_info(chosen_ip)
            await show_ip_info(msg, ip_info)


async def make_json_info_handler(msg: types.Message):
    await FSMParsed.make_json_info.set()
    await msg.reply(f"What type of JSON IP info you prefer to make?", reply_markup=kb_client_json)


async def back_handler(msg: types.Message):
    await FSMParsed.ip_number_wait.set()
    await msg.reply(f"Choose number of IP to get info about it or choose different options",
                    reply_markup=kb_client_ip_number_wait)


async def json_message_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        parsed_ips = data["ip_lst"]
    json_data = await json_handler(msg, parsed_ips)
    await state.finish()
    await msg.reply(json_data)
    await msg.reply("Waiting for next text or document to parse for IP", reply_markup=ReplyKeyboardRemove())


async def json_document_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        parsed_ips = data["ip_lst"]
    json_data = await json_handler(msg, parsed_ips)
    json_file = await json_document_maker(json_data)
    await state.finish()
    await bot.send_document(msg.from_user.id, json_file)
    await msg.reply("Waiting for next text or document to parse for IP", reply_markup=ReplyKeyboardRemove())


async def json_handler(msg: types.Message, parsed_ips: ParsedIPs):
    ip_info = await get_all_ip_info(parsed_ips.ip_lst)
    return await make_json_info(msg, ip_info)


async def get_all_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        parsed_ips = data["ip_lst"]
        ip_info = await get_all_ip_info(parsed_ips.ip_lst)
        await show_ip_info(msg, ip_info)
        await state.finish()
        await msg.reply("Waiting for next text or document to parse for IP", reply_markup=ReplyKeyboardRemove())


async def show_ip_info(msg: types.Message, ip_info: list[OneIpInfo]):
    #TODO add settings that will be unique for client and loads from db. \
    # If settings not set up, then show default info
    for ip in ip_info:
        ip_info_msg = []
        for info in sorted(ip, key=lambda x: x[0] == 'query', reverse=True):
            #TODO settings check
            base_ip_info_config = await make_prefered_info_lst(msg)
            if info[0] in base_ip_info_config:
                one_ip_info = f"{ip_info_config[info[0]]}: {info[1]}"
                ip_info_msg.append(one_ip_info)
        await msg.reply('\n'.join(ip_info_msg), reply_markup=kb_client_ip_number_wait)


async def make_prefered_info_lst(msg: types.Message) -> list[str]:
    # if not settings:
    base_ip_info_config = [info for ind, info in enumerate(ip_info_config.keys()) if ind < 10]
    return base_ip_info_config


async def take_ip_by_number(ip_lst: list, ip_number: int) -> list:
    ip_lst_to_get_info = [ip_lst[ip_number - 1]]
    return ip_lst_to_get_info


async def cancel_handler(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        return
    await state.finish()
    await msg.reply("Waiting for next text or document to parse for IP", reply_markup=ReplyKeyboardRemove())


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(parse_message, content_types=ContentTypes.TEXT)
    dp.register_message_handler(parse_document, content_types=ContentTypes.DOCUMENT)
    dp.register_message_handler(show_parsed_ips, state=None)
    dp.register_message_handler(cancel_handler, state='*', commands="Exit")
    dp.register_message_handler(cancel_handler, Text(equals="Exit", ignore_case=True), state='*')
    dp.register_message_handler(get_all_handler, Text(equals='Get All', ignore_case=True), state='*')
    dp.register_message_handler(make_json_info_handler, Text(equals='JSON', ignore_case=True), state=FSMParsed.ip_number_wait)
    dp.register_message_handler(json_message_handler, Text(equals='Message', ignore_case=True), state=FSMParsed.make_json_info)
    dp.register_message_handler(json_document_handler, Text(equals='Document', ignore_case=True), state=FSMParsed.make_json_info)
    dp.register_message_handler(back_handler, Text(equals='Back', ignore_case=True), state=FSMParsed.make_json_info)
    dp.register_message_handler(process_ip_number_invalid, lambda msg: not msg.text.isdigit(),
                                state=FSMParsed.ip_number_wait)
    dp.register_message_handler(process_ip_number, lambda msg: msg.text.isdigit(), state=FSMParsed.ip_number_wait)