from datetime import datetime

from app.api import client, schemas
from app.logging.base import botlog
from app.exception.base import ApiTimeoutError
from app.logic.utils import class_decor, BaseExceptionResponse
from app.redis.links import links as redis_links

@class_decor
class BaseLogic:
    client = client
    schemas = schemas
    links = redis_links

    def __init__(self, ds_id: int, fullname: str | None = None, purpose_ds_id: int | None = None, **kwargs):
        self.ds_id = ds_id
        self.fullname = fullname
        self.purpose_ds_id = purpose_ds_id or ds_id
        self.kwargs = kwargs

    @property
    async def user_id(self):
        return None

    @property
    async def body(self):
        return self.schemas.QueryBody(user_id=await self.user_id, is_admin=self.is_admin, request_id=self.request_id)

    @property
    def is_admin(self):
        return self.kwargs.get('is_admin', False)

    @property
    def request_id(self):
        return self.kwargs.get('request_id')

    @property
    def guild_id(self):
        return self.kwargs.get('guild_id')
        
    @classmethod
    async def test_api_connect(cls, logged: bool = True, is_raise: bool = False):
        try:
            try:
                start = datetime.now()
                response = await cls.client.main()
                if response:
                    end = datetime.now()
                    result = f'{int((end - start).total_seconds()*1000)}'
                    if logged:
                        botlog.logger.info('API работает', ping=result, url=cls.client.client.config.base_url)
                    return result
                raise ApiTimeoutError('API не работает')
            except:
                raise ApiTimeoutError('API не работает')
        except:
            if is_raise:
                raise

    def redact_kwargs(self, **new_kwargs):
        self.kwargs |= new_kwargs
        return self

    def check_is_not_none(self, *objs):
        for obj in objs:
            if not obj is None:
                return obj