import asyncio

from config import bot, settings
from app.logic.base import BaseLogic as logic
from app.logging.base import botlog
from app.redis.base import redis_client, redis_ping

@botlog.logger.catch(reraise=True)
async def main():
    try:
        botlog.logger.info('Бот запускается')
        await logic.test_api_connect(True)
        await redis_ping(True)
        botlog.start()
        bot.run(settings.token)
        settings.info['main'] = bot
    except:
        pass
    finally:
        await stop()

async def stop():
    botlog.stop()
    await redis_client.aclose()

if __name__ == "__main__": 
    try:
        asyncio.run(main())
    except RuntimeError as e:
        botlog.stop()
    

