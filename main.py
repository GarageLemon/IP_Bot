from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin


async def on_startup(_):
    print('IP BOT IS ONLINE')

client.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)