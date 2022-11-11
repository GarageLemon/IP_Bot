from create_bot import dp
from .register_check import RegisterCheck

if __name__ == "middlewares":
    dp.middleware.setup(RegisterCheck())