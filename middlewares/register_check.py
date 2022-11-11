from typing import Dict, Any
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update
from database.db_prompts import check_user_registration, register_user


class RegisterCheck(BaseMiddleware):
    async def on_pre_process_update(self,
                       update: Update,
                       data: Dict[str, Any]
                       ) -> Any:
        if update.message:
            user = await check_user_registration(update.message)
            if not user:
                await register_user(update.message)
