import asyncio

from config import bot, settings
from app.logic.base import BaseLogic as logic
from app.logging.base import global_botlog as botlog
from app.redis.base import redis_client, redis_ping
from app.ds.cogs import global_setup

@bot.event
async def on_ready():
    botlog.logger.log('BOT START', f'Бот запущен как {bot.user}')

@botlog.logger.catch(reraise=True)
async def main():
    try:
        botlog.logger.info('Бот запускается')
        await logic.test_api_connect(True)
        await redis_ping(True)
        global_setup(bot)
        settings.info['main'] = bot
        await bot.start(settings.token)
    except:
        pass
    finally:
        await redis_client.aclose()
        botlog.stop()

if __name__ == "__main__": 
    try:
        asyncio.run(main())
    except RuntimeError as e:
        botlog.stop()
    

