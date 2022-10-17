import logging
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from create_bot import dp
from handlers.client import register_handlers_client


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('IP BOT IS ONLINE')


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=shutdown)
