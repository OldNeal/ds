from discord import ApplicationContext, Cog, Bot
from discord.ext import commands

from app.service.base import BaseService

class BaseCog(Cog):
    service_cls = BaseService

    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx: ApplicationContext):
        self.service = self.service_cls(ctx)
