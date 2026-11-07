from discord import Interaction, SelectOption
from discord.ui import View, Item, Select, Button
from typing import Any, Coroutine

from app.service.base import BaseService
from app.exception.base import BotError, PythonError, ALienCallbackError
from app.validate.ds import Answer

class BaseView(View):
    def __init__(self, service_cls: type[BaseService], ds_id: int, is_author_check: bool = True, **kwargs):
        super().__init__(timeout=None, disable_on_timeout=False)
        self.service_cls = service_cls
        self.ds_id = ds_id
        self.is_author_check = is_author_check
        self.page = 0
        self.max_page = 0
        self.add_items(**kwargs)

    def add_items(self, **kwargs):
        pass 

    async def interaction_check(self, interaction: Interaction):
        self.servise = self.service_cls(interaction.user, interaction.guild)
        self.servise.botlog.callback(interaction.custom_id, interaction.data)
        if self.is_author_check and interaction.user.id != self.ds_id:
            raise ALienCallbackError()
        return True

    async def on_error(self, error, item: Item, interaction: Interaction):
        if isinstance(error, BotError):
            await interaction.respond(error.to_msg, ephemeral=True)
        else:
            await interaction.respond(PythonError.msg, ephemeral=True)
            raise error

    def create_button_page(self, page: int = 0, max_page: int = 0, row: int = 1):
        last_page = max(0, max_page - 1)
        back_page_10 = Button(emoji='⏮️', custom_id=f'back_page_10:{max(0, page - 5)}', disabled=page <= 0, row=row)
        back_page = Button(emoji='◀️', custom_id=f'back_page:{max(0, page - 1)}', disabled=page <= 0, row=row)
        this_page = Button(label=f'📄 Страница {page + 1}/{max_page}', disabled=True, row=row)
        next_page = Button(emoji='▶️', custom_id=f'next_page:{min(last_page, page + 1)}', disabled=page >= last_page, row=row)
        next_page_10 = Button(emoji='⏭️', custom_id=f'next_page_10:{min(last_page, page + 5)}', disabled=page >= last_page, row=row)
        return back_page_10, back_page, this_page, next_page, next_page_10

    def add_button_page(self, callback, page: int = 0, max_page: int = 0, row: int = 1):   
        self.page = page
        self.max_page = max_page
        if max_page > 1:
            page_buttons = self.create_button_page(page, max_page, row)
            for page_button in page_buttons:
                page_button.callback = callback
                self.add_item(page_button)

    def parse_page(self, custom_id: str):
        return int(custom_id.split(':')[1])

    async def answer(self, interaction: Interaction, callback: Coroutine[Any, Any, Answer]):
        answer = await callback
        await interaction.response.edit_message(
            content=answer.content,
            embed=answer.embed,
            view=answer.view,
            delete_after=answer.delete_after
            )
        return interaction