from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from keyboards import make_settings_keyboard, kb_client_on_start
from config import ip_info_config
from services import setting_data_to_str
from database.db_prompts import set_new_settings


class FSMSettings(StatesGroup):
    set_up_data_settings = State()


async def change_ip_info_shown(msg: Message, state: FSMContext, ip_config=ip_info_config):
    chosen_setting = list(ip_config.keys())[list(ip_config.values()).index(msg.text)]
    async with state.proxy() as data:
        data["client_ip_config"][chosen_setting] = not data["client_ip_config"][chosen_setting]
        reply_line = f"{msg.text} is set to {await setting_data_to_str(data['client_ip_config'], chosen_setting)}"
    await msg.reply(reply_line, reply_markup=await make_settings_keyboard())


async def set_settings(msg: Message, state: FSMContext, ip_config=ip_info_config):
    if 'accept' in msg.text.lower():
        is_default = False
        async with state.proxy() as data:
            new_settings = data["client_ip_config"]
    else:
        is_default = True
        new_settings = {key: (True if ind < 10 else False) for ind, key in enumerate(ip_config.keys())}
    await set_new_settings(msg, new_settings, is_default)
    await state.finish()
    await msg.reply("New settings has been set, waiting for text or document to parse for IP",
                    reply_markup=kb_client_on_start)


def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(change_ip_info_shown, Text(equals=tuple(value for value in ip_info_config.values()
                                                                        if value not in
                                                                        ('IP', 'IP Check status', 'IP Check message')),
                                                           ignore_case=True), state=FSMSettings.set_up_data_settings)
    dp.register_message_handler(set_settings, Text(equals=('Accept Settings', 'Set Settings to Default'),
                                                   ignore_case=True), state=FSMSettings.set_up_data_settings)
