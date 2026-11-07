from discord.ext.commands import Context
from discord import Message
import discord

DEFAULT_BOT_ERROR_HANDLER = None


def is_natural_int(string: str | None,
                   ds_id: int | None = None,
                   error_less_one=ValueError,
                   error_float=ValueError,
                   error_no_int=ValueError,
                   error_group=Exception) -> int:
    try:
        quan = float(string)
    except (ValueError, TypeError):
        raise error_no_int(f'This user(ds_id={ds_id}) enter no int')
    if quan <= 0:
        raise error_less_one(f'This user(ds_id={ds_id}) enter int, but int <=0: {string}')
    if not quan.is_integer():
        raise error_float(f'This user(ds_id={ds_id}) enter float')
    return int(quan)


class RaiseErrorHandler:
    async def on_execution_error(self, ctx: Context, error: Exception):
        raise error