from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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