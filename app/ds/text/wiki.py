from discord import Embed, EmbedField

from app.ds.text.base import BaseText
from app.validate.api import AnswerAllPathInfo, AnswerGAFullInfo, AnswerPathFullInfo

class WikiText(BaseText):
    @classmethod
    def all_paths(self):
        return '📜 Все пути'

    @classmethod
    def paths(self, data: AnswerAllPathInfo):
        groups = set([p.group for p in data.paths])
        return Embed(
            title=self.all_paths(),
            fields=[EmbedField(name=g, value='\n'.join([p.name for p in data.paths if p.group == g])) for g in groups],
            color=self.old_neal_color()
        )

    @classmethod
    def path(self, data: AnswerPathFullInfo):
        return Embed(
            title=data.ga.name,
            fields=[EmbedField(name='🧪 Последовательности', value='\n'.join([f'{s.number} - {s.name}' for s in sorted(data.seqs, key=lambda x: x.number)]))],
            color=self.old_neal_color()
        )

    @classmethod
    def select_search_path(self, count: int):
        return f'🔍 Найдены пути ({count} шт.)'

    @classmethod
    def select_search_ga(self, count: int):
        return f'🔍 Найдены ВД ({count} шт.)'
    
    @classmethod
    def ga(self, data: AnswerGAFullInfo):
        paths = '\n'.join(path.name for path in data.paths) or '❌ Нет связанных путей'
        return Embed(
            title=data.name,
            fields=[EmbedField(name='⚗️ Пути', value=paths)],
            color=self.old_neal_color()
        )