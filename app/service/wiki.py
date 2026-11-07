from app.service.main import BotService
from app.logic.wiki import WikiLogic
from app.validate.ds import Answer
from app.ds.text.wiki import WikiText
from app.ds.buttons.wiki import WikiIKB
from app.exception.wiki import GASearchError, PathSearchError

class WikiService(BotService):
    logic_class: type[WikiLogic] = WikiLogic
    logic: WikiLogic
    text: type[WikiText] = WikiText
    ikb_cls = WikiIKB
    IKB: WikiIKB

    async def all_paths(self, group: str | None = None, path_id: int | None = None):
        data = await self.logic.all_paths()
        if path_id:
            path = await self.logic.path(id=path_id)
            embed = self.text.path(path)
        else:
            embed = None
        return Answer(
            embed=embed,
            view=self.IKB.all_paths(
                groups={p.group for p in data.paths}, 
                paths=[p for p in data.paths if p.group.startswith(group)] if group else None,
                group=group,
                path_name=path.name if path_id else None),
            ephemeral=True
            )
    
    async def search_path(self, search_value: str | None = None, path_id: int | None = None, page: int = 0):
        data = await self.logic.search_path(search_value, page)
        if data.count == 0:
            raise PathSearchError()
        if data.count == 1:
            path_id = data.paths[0].path_id
        if path_id:
            path = await self.logic.path(id=path_id)
            embed = self.text.path(path)
        else:
            embed = None
        return Answer(
            content=self.text.select_search_path(data.count),
            embed=embed,
            view=self.IKB.search_path(
                search_value=search_value, 
                paths=[p for p in data.paths],
                path_name=path.name if path_id else None,
                page=data.page.number,
                max_page=data.page.max
                ),
            ephemeral=True
            )

    async def all_gas(self, group: str | None = None, ga_id: int | None = None, path_id: int | None = None):
        data = await self.logic.all_gas()
        if ga_id:
            ga = await self.logic.ga(id=ga_id)
            embed = self.text.ga(ga)
            if path_id:
                path = await self.logic.path(id=path_id)
                embed = self.text.path(path)
        else:
            embed = None
        return Answer(
            embed=embed,
            view=self.IKB.all_gas(
                groups={g.group for g in data.gas}, 
                gas=[g for g in data.gas if g.group.startswith(group)] if group else None,
                paths=ga.paths if ga_id else None,
                group=group,
                ga_id=ga_id,
                ga_name=ga.name if ga_id else None,
                path_name=path.name if path_id else None),
            ephemeral=True
            )
    
    async def search_ga(self, search_value: str | None = None, ga_id: int | None = None, path_id: int | None = None, page: int = 0):
        data = await self.logic.search_ga(search_value, page)
        if data.count == 0:
            raise PathSearchError()
        if data.count == 1:
            ga_id = data.gas[0].ga_id
        if ga_id:
            ga = await self.logic.ga(id=ga_id)
            embed = self.text.ga(ga)
            if path_id:
                path = await self.logic.path(id=path_id)
                embed = self.text.path(path)
        else:
            embed = None
        return Answer(
            content=self.text.select_search_ga(data.count),
            embed=embed,
            view=self.IKB.search_ga(
                search_value=search_value, 
                gas=[p for p in data.gas],
                paths=ga.paths if ga_id else None,
                ga_id=ga_id,
                ga_name=ga.name if ga_id else None,
                path_name=path.name if path_id else None,
                page=data.page.number,
                max_page=data.page.max
                ),
            ephemeral=True
            )