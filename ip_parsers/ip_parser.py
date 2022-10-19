from dataclasses import dataclass, field
from enum import Enum
from ipaddress import ip_address, IPv4Address, IPv6Address
import aiofiles
import re


@dataclass(slots=True, kw_only=True)
class ParsedIPs:
    ip_count: int = field(init=False)
    ip_lst: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.ip_count = len(self.ip_lst)


class RegexParsePatterns(Enum):
    ipv4 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ipv6 = r'\w{1,4}\:\w{1,4}\:\w{1,4}\:\w{1,4}\:\w{1,4}\:\w{1,4}\:\w{1,4}\:\w{1,4}\b'


async def message_text_parse(text: str) -> ParsedIPs:
    validated_ip_lst = await text_parse(text)
    return ParsedIPs(ip_lst=validated_ip_lst)


async def file_text_parse(filepath: str) -> ParsedIPs:
    async with aiofiles.open(filepath, mode='r', encoding='utf-8', errors='ignore') as file:
        validated_ip_lst = await text_parse(str(await file.read()).replace("\n", ""))
    return ParsedIPs(ip_lst=validated_ip_lst)


async def text_parse(text: str) -> list:
    validated_ip_lst = []
    for ip_pattern in RegexParsePatterns:
        possible_ip_lst = re.findall(ip_pattern.value, text)
        for possible_ip in possible_ip_lst:
            valid_ip = await _validate_ip(possible_ip)
            if valid_ip:
                validated_ip_lst.append(str(valid_ip))
    return validated_ip_lst


async def _validate_ip(ip: str) -> IPv4Address | IPv6Address | None:
    try:
        valid_ip = ip_address(ip)
        return valid_ip
    except ValueError:
        return None
