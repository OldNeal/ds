from app.ds.view.base import BaseView
from app.service.base import BaseService

class BaseIKB:
    def __init__(self, service_cls: type[BaseService], ds_id: int):
        self.service_cls = service_cls
        self.ds_id = ds_id

