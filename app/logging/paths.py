from pathlib import PurePath

from config import settings

class LogPaths:
    logs = PurePath(settings.log_files_path)
    base = logs / PurePath('base/')

    categories = {
        'base':base
    }

    @classmethod
    def get(cls, category: str):
        path = cls.categories.get(category)
        return path
    