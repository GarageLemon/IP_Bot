from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import ip_info_config

button_all = KeyboardButton('Get All')
button_exit = KeyboardButton('Exit')
button_json = KeyboardButton('JSON')

kb_client_ip_number_wait = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_ip_number_wait.row(button_all, button_json, button_exit)

button_back = KeyboardButton('Back')
button_document = KeyboardButton('Document')
button_msg = KeyboardButton('Message')

kb_client_json = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_json.row(button_msg, button_document, button_back, button_exit)

button_settings = KeyboardButton('Settings')

kb_client_on_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_on_start.row(button_settings)


async def make_settings_keyboard(ip_config: dict = ip_info_config, exit_button: KeyboardButton = button_exit)\
        -> ReplyKeyboardMarkup:
    kb_settings = ReplyKeyboardMarkup(resize_keyboard=True)
    accept_button = KeyboardButton('Accept Settings')
    default_button = KeyboardButton('Set Settings to Default')
    for ip_data_name in ip_config.values():
        if ip_data_name in ('IP', 'IP Check status', 'IP Check message'):
            continue
        button = KeyboardButton(ip_data_name)
        kb_settings.insert(button)
    kb_settings.row(accept_button, default_button, exit_button)
    return kb_settings
