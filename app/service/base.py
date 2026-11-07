import asyncio, functools, uuid
from datetime import datetime
from discord import ApplicationContext, User, TextChannel, Member, Guild
from typing import Callable, Any, Coroutine

from config import settings
from app.logic.base import BaseLogic
from app.logging.base import botlog as global_botlog, BotLogger
from app.ds.text.base import BaseText
from app.validate.ds import Answer

NOT_NEW_STATE = object()

class BaseService:
    asyncio = asyncio
    datetime = datetime
    settings = settings

    logic_class: type[BaseLogic] = BaseLogic
    logic: BaseLogic
    text: type[BaseText] = BaseText

    def __init__(self,
                 user: Member | User,
                 guild: Guild | None = None,
                 botlog: BotLogger = global_botlog,
                 add_logic_kwargs: dict = {},
                 **kwargs):
        self.user = user
        self.botlog = botlog
        self.kwargs = kwargs
        self.guild = guild
        self.ds_id = self.user.id
        self.add_logic_kwargs = add_logic_kwargs

        self.logic = self.logic_class(
            ds_id=self.ds_id,
            **self.logic_kwargs
        )
        self.logger = self.logger_bind()
        self.add_ikb()

    def add_ikb(self):
        pass

    @property
    def logic_kwargs(self):
        return {'is_admin': self.is_admin,
                'request_id': self.request_id,
                'guild_id': self.guild_id} | self.add_logic_kwargs

    @property
    def log_kwargs(self):
        return {'ds_id':self.ds_id, 'request_id': self.request_id, 'guild_id': self.guild_id}

    @property
    def request_id(self):
        return self.kwargs.get('request_id', uuid.uuid4().hex)
   
    @property
    def is_admin(self):
        return self.kwargs.get('is_admin', False) and self.ds_id_in_admins

    @property
    def to_json(self):
        return self.kwargs.get('to_json', False)

    @property
    def guild_id(self):
        return self.guild.id if self.guild else None

    @property
    def ds_id_in_admins(self):
        return self.ds_id in self.settings.admins

    def redact_kwargs(self, **new_kwargs):
        self.kwargs |= new_kwargs
        return self

    def check_is_not_none(self, *objs):
        for obj in objs:
            if obj is not None:
                return obj

    def logger_bind(self, **kwargs):
        self.botlog = self.botlog.bind(**self.log_kwargs | kwargs)
        return self.botlog

    def __getattr__(self, name) -> Callable[..., Coroutine[Any, Any, Answer]]:
        pass