from app.exception.base import BotError

class PathSearchError(BotError):
    msg = 'Путь не найден'


class GASearchError(BotError):
    msg = 'ВД не найден'