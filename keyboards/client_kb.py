from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_all = KeyboardButton('Get All')
button_exit = KeyboardButton('Exit')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(button_all, button_exit)
