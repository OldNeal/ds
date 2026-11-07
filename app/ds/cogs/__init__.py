from discord import Bot

from .base import MainCog
from .wiki import WikiCog

cogs = [MainCog, WikiCog]

def global_setup(bot: Bot):
    [bot.add_cog(cog(bot)) for cog in cogs]

    