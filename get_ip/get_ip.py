import asyncio
from typing import Optional, Union
from httpx import AsyncClient
from pydantic import BaseModel as PydanticBaseModel, Field, validator


class BaseModel(PydanticBaseModel):
    @validator('*')
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v


class OneIpInfo(BaseModel):
    status: Union[None, str]
    message: Union[None, str]
    continent: Union[None, str]
    continentCode: Union[None, str]
    country: Union[None, str]
    countryCode: Union[None, str]
    region: Union[None, str]
    regionName: Union[None, str]
    city: Union[None, str]
    district: Union[None, str]
    zip_code: Union[None, str] = Field(alias="zip")
    lat: Optional[float]
    lon: Optional[float]
    timezone: Union[None, str]
    offset: Union[None, str]
    currency: Union[None, str]
    isp: Union[None, str]
    org: Union[None, str]
    as_org_number_rir: Union[None, str] = Field(alias="as")
    asname_rir: Union[None, str]
    reverse: Union[None, str]
    mobile: Optional[bool]
    proxy: Optional[bool]
    hosting: Optional[bool]
    query: Union[None, str]

    class Config:
        allow_population_by_field_name = True


async def get_ip_info(client: AsyncClient, url: str) -> dict:
    response = await client.get(url)
    return response.json()


async def get_all_ip_info(ip_lst: list) -> list[OneIpInfo]:
    all_ip_info = []
    async with AsyncClient() as client:
        tasks = []
        for ip in ip_lst:
            url = f"http://ip-api.com/json/{ip}?fields=66846719"
            tasks.append(asyncio.create_task(get_ip_info(client, url)))
        all_info = await asyncio.gather(*tasks)
    for info in all_info:
        all_ip_info.append(OneIpInfo(**info))
    return all_ip_info


# ip_lst = ['127.243.173.151',
# '60.31.111.175',
# '153.101.155.148',
# '91.76.31.251',
# '31.151.119.203',
# '20.83.167.5',
# '83.255.182.121',
# '191.135.253.203',
# '169.250.83.202',
# '78.147.117.224']
