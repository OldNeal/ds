from discord import ApplicationContext, Cog, Bot, Interaction, InteractionType
from discord.ext import commands
from discord.errors import Forbidden

from config import settings
from app.service.base import BaseService
from app.exception.base import BotError, PermissionError, PythonError

class BaseCog(Cog):
    service_cls = BaseService

    def __init__(self, bot: Bot):
        self.bot = bot

    def new_message(self, ctx: ApplicationContext):
        if ctx.command:
            self.botlog.message(f'/{f'{ctx.command.full_parent_name} ' if len(ctx.command.full_parent_name) > 0 else ''}{ctx.command.name}', args=ctx.options)
        elif ctx.message:
            self.botlog.message(ctx.message.content)

    async def cog_before_invoke(self, ctx: ApplicationContext):
        self.service = self.service_cls(ctx.author, ctx.guild)
        self.botlog = self.service.botlog
        self.new_message(ctx)

    async def cog_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, BotError):
            await ctx.respond(error.to_msg, ephemeral=True)
        else:
            await ctx.respond(PythonError.msg, ephemeral=True)
            raise error

class MainCog(BaseCog):
    @commands.command()
    async def hello(self, ctx: ApplicationContext):
        await ctx.send("Привет!")
        
    @commands.slash_command(description='Получить ваш айди и айди сервера')
    async def ids(self, ctx: ApplicationContext):
        await ctx.respond('\n'.join([
            f'Ваш айди: {self.service.ds_id}',
            f'Айди сервера: {self.service.guild_id}',
            ]))