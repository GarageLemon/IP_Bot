from dataclasses import dataclass


@dataclass
class ParsedIPs:
    ip_count: int
    ip_lst: list


async def message_text_parse(msg) -> ParsedIPs:
    pass


async def file_text_parse(msg) -> ParsedIPs:
    pass
