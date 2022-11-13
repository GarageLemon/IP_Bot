from enum import Enum

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine.url import URL
from config import PsqlUserInfo
from dataclasses import dataclass


DATABASE = {
    'drivername': 'postgresql+asyncpg',
    'host': 'localhost',
    'port': str(PsqlUserInfo.PSQL_PORT),
    'username': PsqlUserInfo.PSQL_USER,
    'password': PsqlUserInfo.PSQL_PASSWORD,
    'database': PsqlUserInfo.PSQL_DB_NAME
}


engine = create_async_engine(URL.create(**DATABASE))
