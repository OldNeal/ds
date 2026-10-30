import asyncio, functools
from datetime import datetime
from typing import TypeVar
from discord import ApplicationContext, User

from config import settings, bot
from app.validate.tg import Answer, AnswerBody
from app.logic.base import BaseLogic
from app.logging.base import botlog

NOT_NEW_STATE = object()
DATA_PAGE = TypeVar('DATA_PAGE')

class BaseService:
    asyncio = asyncio
    datetime = datetime
    botlog = botlog
    bot = bot
    settings = settings

    logic_class: type[BaseLogic] = BaseLogic
    logic: BaseLogic

    def __init__(self,
                 ctx: ApplicationContext,
                 add_logic_kwargs: dict = {}, 
                 **kwargs):
        self.ctx = ctx
        self.kwargs = kwargs

        self.user = self.ctx.user
        self.guild = self.ctx.guild
        self.ds_id = self.user.id
        self.add_logic_kwargs = add_logic_kwargs

        self.logic = self.logic_class(
            ds_id=self.ds_id,
            username=self.user.nick,
            fullname=self.user.name,
            **self.logic_kwargs
        )

    @property
    def logic_kwargs(self):
        return {'is_admin':self.is_admin, 'request_id':self.kwargs.get('request_id'), 'guild_id':self.guild.id} | self.add_logic_kwargs

    @property
    def is_admin(self):
        return self.kwargs.get('is_admin', False) and self.ds_id_in_admins

    @property
    def to_json(self):
        return self.kwargs.get('to_json', False)

    @property
    def ds_id_in_admins(self):
        return self.ds_id in self.settings.admins

    def redact_kwargs(self, **new_kwargs):
        self.kwargs |= new_kwargs
        return self

    def check_is_not_none(self, *objs):
        for obj in objs:
            if not obj is None:
                return obj