import logging
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from create_bot import dp
from handlers.client import register_handlers_client
from handlers.settings_set_up import register_handlers_settings
from database.create_db import make_db, connect_create_if_not_exists
from database.engine import DATABASE
from middlewares.register_check import RegisterCheck


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('IP BOT IS ONLINE')
    await connect_create_if_not_exists(DATABASE)
    await make_db()


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

register_handlers_client(dp)
register_handlers_settings(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=shutdown)
