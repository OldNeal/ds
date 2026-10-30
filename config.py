import os, redis.asyncio as redis
from dotenv import load_dotenv
from pathlib import Path
from discord import Bot

load_dotenv(Path(__file__).parent / '.env')

class Settings:
    api_url = os.getenv('api_url')

    bot_token = os.getenv('bot_token')
    dev_bot_token = os.getenv('dev_bot_token', bot_token)
    _is_dev = os.getenv('is_dev', 'f')

    admins = [int(x) for x in os.getenv('admins').split(',')]
    owner = int(os.getenv('owner'))

    _use_redis = os.getenv('use_redis', 'f')
    redis_url = os.getenv('redis_url')
    state_ttl = int(os.getenv('state_ttl', 60*60*24))
    data_ttl = int(os.getenv('data_ttl', 60*60*24))

    redis_host = os.getenv('redis_host', 'localhost')   
    redis_port = int(os.getenv('redis_port', 6379))
    redis_password = os.getenv('redis_password')

    docs_url = os.getenv('docs_url')

    log_files_path = os.getenv('log_files_path', 'logs/')

    throttling_default_max=int(os.getenv('throttling_default_max', 25))
    throttling_default_per_seconds=int(os.getenv('throttling_default_per_seconds', 60))
    debounce_default_window=int(os.getenv('debounce_default_window', 2))

    info: dict = {}

    @property
    def is_dev(self):
        return True if self._is_dev in ['t', 'true', '1'] else False

    @property
    def token(self):
        return self.dev_bot_token if self.is_dev else self.bot_token

    @property
    def use_redis(self):
        return True if self._use_redis in ['t', 'true', '1'] else False

    @property
    def bot(self) -> Bot:
        return self.info.get('main')

settings = Settings()
bot = Bot()
