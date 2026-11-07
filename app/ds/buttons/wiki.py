from app.ds.buttons.base import BaseIKB
from app.ds.view.wiki import AllPathsView, SearchPathView, AllGasView, SearchGaView
from app.validate.api import AnswerGAInfo, AnswerPathInfo

class WikiIKB(BaseIKB):
    def all_paths(self, groups: list[str], paths: list[AnswerPathInfo], group: str | None = None, path_name: str | None = None):
        return AllPathsView(
            service_cls=self.service_cls,
            ds_id=self.ds_id,
            groups=groups,
            paths=paths,
            group=group,
            path_name=path_name
            )

    def search_path(self, search_value: str, paths: list[AnswerPathInfo], path_name: str | None = None, page: int = 0, max_page: int = 0):
        return SearchPathView(
            service_cls=self.service_cls,
            ds_id=self.ds_id,
            search_value=search_value,
            paths=paths,
            path_name=path_name,
            page=page,
            max_page=max_page
            )

    def all_gas(self, groups: list[str], gas: list[AnswerGAInfo] | None, paths: list[AnswerPathInfo], group: str | None = None, ga_id: int | None = None, ga_name: str | None = None, path_name: str | None = None):
        return AllGasView(
            service_cls=self.service_cls,
            ds_id=self.ds_id,
            groups=groups,
            gas=gas,
            paths=paths,
            group=group,
            ga_id=ga_id,
            ga_name=ga_name,
            path_name=path_name,
            )
    
    def search_ga(self, search_value: str, gas: list[AnswerGAInfo] | None, paths: list[AnswerPathInfo], ga_id: int | None = None, ga_name: str | None = None, path_name: str | None = None, page: int = 0, max_page: int = 0):
        return SearchGaView(
            service_cls=self.service_cls,
            ds_id=self.ds_id,
            search_value=search_value,
            gas=gas,
            paths=paths,
            ga_id=ga_id,
            ga_name=ga_name,
            path_name=path_name,
            page=page,
            max_page=max_page
            )