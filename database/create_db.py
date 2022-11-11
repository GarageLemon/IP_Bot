from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from database.engine import engine


DeclarativeBase = declarative_base()
session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
# session = Session()


class User(DeclarativeBase):
    __tablename__ = 'user'

    id_user = Column(Integer, primary_key=True)
    user_id = Column('user_id', BigInteger, nullable=False, unique=True)
    user_settings = Column('user_settings', Boolean, nullable=False, default=False)
    # settings = relationship("Settings")

    __mapper_args__ = {"eager_defaults": True}


class Settings(DeclarativeBase):
    __tablename__ = 'settings'

    id_settings = Column(Integer, primary_key=True)
    user_id = Column('user_id', BigInteger, ForeignKey("user.user_id"))
    status = Column('status', Boolean, nullable=False, default=True)
    message = Column('message', Boolean, nullable=False, default=True)
    country = Column('country', Boolean, nullable=False, default=True)
    countryCode = Column('countryCode', Boolean, nullable=False, default=True)
    city = Column('city', Boolean, nullable=False, default=True)
    zip_code = Column('zip_code', Boolean, nullable=False, default=True)
    lat = Column('lat', Boolean, nullable=False, default=True)
    lon = Column('lon', Boolean, nullable=False, default=True)
    timezone = Column('timezone', Boolean, nullable=False, default=True)
    query = Column('query', Boolean, nullable=False, default=True)
    continent = Column('continent', Boolean, nullable=False, default=False)
    continentCode = Column('continentCode', Boolean, nullable=False, default=False)
    region = Column('region', Boolean, nullable=False, default=False)
    regionName = Column('regionName', Boolean, nullable=False, default=False)
    district = Column('district', Boolean, nullable=False, default=False)
    offset = Column('offset', Boolean, nullable=False, default=False)
    currency = Column('currency', Boolean, nullable=False, default=False)
    isp = Column('isp', Boolean, nullable=False, default=False)
    org = Column('org', Boolean, nullable=False, default=False)
    as_org_number_rir = Column('as_org_number_rir', Boolean, nullable=False, default=False)
    asname_rir = Column('asname_rir', Boolean, nullable=False, default=False)
    reverse = Column('reverse', Boolean, nullable=False, default=False)
    mobile = Column('mobile', Boolean, nullable=False, default=False)
    proxy = Column('proxy', Boolean, nullable=False, default=False)
    hosting = Column('hosting', Boolean, nullable=False, default=False)
    # user = relationship("User")

    __mapper_args__ = {"eager_defaults": True}


async def make_db(base=DeclarativeBase, engine=engine):
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)

