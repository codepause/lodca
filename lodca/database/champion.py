from functools import lru_cache
import json
from typing import Union

from lodca.engine.champion import Champion
from lodca.database import Entry, BaseDatabase
from lodca.database.champion_skills import local_skills_database, local_combos_database


class ChampionEntry(Entry):

    @classmethod
    def build(cls, data: Union[str, dict] = None, **kwargs):
        if isinstance(data, str):
            data = json.loads(data)
        elif not isinstance(data, dict):
            data = dict()
        name = data.get('name', 'default')
        skills = local_skills_database.get(name, dict())
        combos = local_combos_database.get(name, dict())
        return cls(
            Champion(
                name=name,
                meta_data=data,
                skills=skills,
                combos=combos,
            )
        )


class ChampionDatabase(BaseDatabase):
    def __init__(self, *args, **kwargs):
        super(ChampionDatabase, self).__init__(*args, **kwargs)
        self.fill_database(self.config.settings.base_stats_path)

    def fill_database(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data = data['data']
        for key, value in data.items():
            self.data[key] = ChampionEntry.build(data=value)

    @lru_cache(maxsize=200)
    def get(self, name: str, **kwargs):
        return self.data.get(name, ChampionEntry.build())


if __name__ == '__main__':
    from lodca.configs.app_configs import DatabaseConfig

    cfg = DatabaseConfig()
    cfg.settings.base_stats_path = '../../tests/temp/database/champion.json'
    db = ChampionDatabase(cfg)
    champion = db.get('Vayne')
    print(champion)
