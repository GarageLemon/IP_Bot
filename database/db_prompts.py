from database.create_db import session, User, Settings
from aiogram.types import Message
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy import update


async def register_user(msg: Message, async_session=session):
    async with async_session() as s:
        async with s.begin():
            s.add(User(user_id=msg.from_user.id))
            result = await s.execute(select(User.user_id).where(User.user_id == msg.from_user.id))
            primary_id = result.scalars().first()
            s.add(Settings(user_id=primary_id))
        await s.commit()


async def check_user_registration(msg: Message, async_session=session) -> User:
    async with async_session() as s:
        async with s.begin():
            result = await s.execute(select(User.user_id).where(User.user_id == msg.from_user.id))
            user = result.scalars().first()
    return user


async def set_new_settings(msg: Message, new_settings: dict, is_default: bool, async_session=session):
    async with async_session() as s:
        async with s.begin():
            settings_result = await s.execute(update(Settings).where(Settings.user_id == msg.from_user.id)
                                              .values(new_settings))
            user_result = await s.execute(update(User).where(User.user_id == msg.from_user.id)
                                          .values(user_settings=not is_default))


async def get_client_settings(msg: Message, async_session=session) -> dict:
    async with async_session() as s:
        async with s.begin():
            result: AsyncResult = await s.execute(select(Settings).where(Settings.user_id == msg.from_user.id))
            settings_data_object = result.mappings().one()
            for row in settings_data_object.values():
                settings_data = dict(sorted({x: y for x, y in row.__dict__.items() if type(y) is bool}.items(),
                                            key=lambda x: x[1] is True, reverse=True))
    return settings_data


async def check_settings_set_up(msg: Message) -> bool:


