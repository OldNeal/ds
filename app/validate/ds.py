from discord import Embed
from discord.ui import View

from app.validate.base import BaseValidate

class Answer(BaseValidate):
    content: str | None = None
    embed: Embed | None = None
    view: View | None = None
    delete_after: float | None = None
    ephemeral: bool = False


