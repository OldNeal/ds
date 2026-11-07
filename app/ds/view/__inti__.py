from discord import Bot

from .base import BaseView
from .wiki import WikiView

views = []

def global_setup(bot: Bot):
    [bot.add_view() for view in views]
