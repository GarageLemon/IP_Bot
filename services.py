from emoji import emojize


async def setting_data_to_str(settings_data: dict, key: str, value: str = None) -> str:
    if value in ('IP', 'IP Check status', 'IP Check message'):
        return f"Always ON {emojize(':check_mark_button:')}"
    if settings_data[key]:
        return f"ON {emojize(':check_mark_button:')}"
    return f"OFF {emojize(':cross_mark:')}"
