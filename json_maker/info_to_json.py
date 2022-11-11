import json
import aiofiles
from get_ip.get_ip import OneIpInfo
from handlers import client
from aiogram import types
from aiogram.types import ContentTypes, Message, InputFile
from aiogram.types.input_file import InputFile
from config import JSON_DOCUMENT_FOR_UPLOAD_DIR
from datetime import datetime
from os import path, remove
from random import randint


async def make_json_info(msg: types.Message, ip_info: list[OneIpInfo]) -> str:
    base_ip_info_config = await client.__make_prefered_info_lst(msg)
    json_info = [await convert_tup_to_dict([info for info in ip if info[0] in base_ip_info_config]) for ip in ip_info]
    json_data = json.dumps(json_info, indent=4)
    return json_data


async def convert_tup_to_dict(tuple_list: list[tuple]) -> dict:
    info_dict = dict(tuple_list)
    return info_dict


async def json_document_maker(json_data: str) -> InputFile:
    filepath = path.join(JSON_DOCUMENT_FOR_UPLOAD_DIR, f"{str(datetime.now())}_{randint(0, 10000)}.txt")
    async with aiofiles.open(filepath, mode='w+', encoding='utf-8') as file:
        await file.write(json_data)
    json_file = InputFile(filepath)
    remove(filepath)
    return json_file

