from app.logging.base import botlog as global_botlog
from app.service.base import BaseService
from app.ds.buttons.base import BaseIKB



class BotService(BaseService):
    ikb_cls: type[BaseIKB] = BaseIKB
    IKB: BaseIKB

    def add_ikb(self):
        self.IKB = self.ikb_cls(type(self), ds_id=self.ds_id)
        return self.IKB
