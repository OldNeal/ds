from __future__ import annotations

from discord import ApplicationContext, SlashCommandGroup, Option
from discord.ext import commands

from app.ds.cogs.base import BaseCog
from app.service.wiki import WikiService

class WikiCog(BaseCog):
    service_cls = WikiService
    service: WikiService

    path = SlashCommandGroup('path')
    ga = SlashCommandGroup('ga')

    @path.command(description='Список всех путей')
    async def list(self, ctx: ApplicationContext):
        answer = await self.service.all_paths()
        await ctx.respond(
            content=answer.content,
            embed=answer.embed,
            view=answer.view,
            delete_after=answer.delete_after,
            ephemeral=answer.ephemeral
            )

    @path.command(description='Искать путь')
    async def search(self, ctx: ApplicationContext, value = Option(description='Поисковое значение')):
        answer = await self.service.search_path(value)
        await ctx.respond(
            content=answer.content,
            embed=answer.embed,
            view=answer.view,
            delete_after=answer.delete_after,
            ephemeral=answer.ephemeral
            )

    @ga.command(description='Список всех ВД')
    async def list(self, ctx: ApplicationContext):
        answer = await self.service.all_gas()
        await ctx.respond(
            content=answer.content,
            embed=answer.embed,
            view=answer.view,
            delete_after=answer.delete_after,
            ephemeral=answer.ephemeral
            )

    @ga.command(description='Искать ВД')
    async def search(self, ctx: ApplicationContext, value = Option(description='Поисковое значение')):
        answer = await self.service.search_ga(value)
        await ctx.respond(
            content=answer.content,
            embed=answer.embed,
            view=answer.view,
            delete_after=answer.delete_after,
            ephemeral=answer.ephemeral
            )