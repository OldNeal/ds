from discord import Interaction, SelectOption
from discord.ui import Select, Button

from app.ds.view.base import BaseView
from app.validate.api import AnswerGAInfo, AnswerPathInfo

class WikiView(BaseView):
    def create_path_select(self, paths: list[AnswerPathInfo], path_name: str | None = None):
        return Select(
                placeholder='⚗️ Выберите путь' if path_name is None else path_name.title(),
                options=[SelectOption(label=p.name, value=str(p.path_id)) for p in paths],
                custom_id='select_path'
            )
    
    def create_ga_select(self, gas: list[AnswerGAInfo] | None, ga_name: str | None = None):
        return Select(
                placeholder='⛩️ Выберите ВД' if ga_name is None else ga_name.title(),
                options=[SelectOption(label=g.name, value=str(g.ga_id)) for g in gas],
                custom_id='select_ga'
            )

    def create_group_select(self, groups: list[str], group: str | None = None, noticy: str = 'путей'):
        return Select(
            placeholder=f'🗃️ Выберите группу {noticy}' if group is None else group.title(),
            options=[SelectOption(label=g.title(), value=g) for g in groups],
            custom_id='select_group'
        )


class AllPathsView(WikiView):
    def add_items(self, groups: list[str], paths: list[AnswerPathInfo] | None, group: str | None = None, path_name: str | None = None):
        if paths and len(paths) > 1:
            path_select = self.create_path_select(paths, path_name)
            path_select.callback = self.to_select_path 
            self.add_item(path_select)
        self.group = group
        group_select = self.create_group_select(groups, group)
        group_select.callback = self.to_select_group
        self.add_item(group_select)

    async def to_select_group(self, interaction: Interaction):
        return await self.answer(interaction, self.servise.all_paths(group=interaction.data.get('values')[0]))
        
    async def to_select_path(self, interaction: Interaction):
        return await self.answer(interaction, self.servise.all_paths(group=self.group, path_id=int(interaction.data.get('values')[0])))

class SearchPathView(WikiView):
    def add_items(self, search_value: str, paths: list[AnswerPathInfo], path_name: str | None = None, page: int = 0, max_page: int = 0):
        if len(paths) > 1:
            path_select = self.create_path_select(paths, path_name)
            path_select.callback = self.to_select_path 
            self.add_item(path_select)
        self.search_value = search_value        
        self.add_button_page(self.to_page, page, max_page)

    async def to_select_path(self, interaction: Interaction):
        return await self.answer(interaction, self.servise.search_path(search_value=self.search_value, path_id=int(interaction.data.get('values')[0]), page=self.page))

    async def to_page(self, interaction: Interaction):
        return await self.answer(interaction, self.servise.search_path(search_value=self.search_value, page=self.parse_page(interaction.custom_id)))


class AllGasView(WikiView):
    def add_items(self, groups: list[str], gas: list[AnswerGAInfo] | None, paths: list[AnswerPathInfo], group: str | None = None, ga_id: int | None = None, ga_name: str | None = None, path_name: str | None = None):
        if gas and len(gas) > 1:
            if paths:
                path_select = self.create_path_select(paths, path_name)
                path_select.callback = self.to_select_path
                self.add_item(path_select)
            path_select = self.create_ga_select(gas, ga_name)
            path_select.callback = self.to_select_ga
            self.add_item(path_select)
        self.group = group
        self.ga_id = ga_id
        group_select = self.create_group_select(groups, group, 'ВД')
        group_select.callback = self.to_select_group
        self.add_item(group_select)

    async def to_select_group(self, interaction: Interaction):
        return await self.answer(interaction, self.servise.all_gas(group=interaction.data.get('values')[0]))

    async def to_select_ga(self, interaction: Interaction):
        return await self.answer(interaction, self.servise.all_gas(group=self.group, ga_id=int(interaction.data.get('values')[0])))
        
    async def to_select_path(self, interaction: Interaction):
        return await self.answer(interaction, self.servise.all_gas(group=self.group, ga_id=self.ga_id, path_id=int(interaction.data.get('values')[0])))

class SearchGaView(WikiView):
    def add_items(self, search_value: str, gas: list[AnswerGAInfo] | None, paths: list[AnswerPathInfo], ga_id: int | None = None, ga_name: str | None = None, path_name: str | None = None, page: int = 0, max_page: int = 0):
        if gas and len(gas) > 1:
            if paths:
                path_select = self.create_path_select(paths, path_name)
                path_select.callback = self.to_select_path
                self.add_item(path_select)
            ga_select = self.create_ga_select(gas, ga_name)
            ga_select.callback = self.to_select_ga
            self.add_item(ga_select)
        self.ga_id = ga_id
        self.search_value = search_value  
        self.add_button_page(self.to_page, page, max_page, 2 if paths else 1)

    async def to_select_ga(self, interaction: Interaction):
        return await self.answer(interaction, self.servise.search_ga(search_value=self.search_value, ga_id=int(interaction.data.get('values')[0]), page=self.page))

    async def to_page(self, interaction: Interaction):
        return await self.answer(interaction, self.servise.search_ga(search_value=self.search_value, page=self.parse_page(interaction.custom_id)))

    async def to_select_path(self, interaction: Interaction):
        return await self.answer(interaction, self.servise.search_ga(search_value=self.search_value, ga_id=self.ga_id, path_id=int(interaction.data.get('values')[0]), page=self.page))
