from functools import lru_cache
import json
from typing import Union

from lodca.database import Entry, BaseDatabase

from lodca.tools.base import Triggers
from lodca.database.triggers import *

_local_database = {
    # Shadowflame #4645 example:
    # '3020': Triggers(unique=[Botrk()]),
    # '3089': Triggers(unique=[Botrk()]),
    "4645": Triggers(unique=[Shadowflame()]),
    "1043": Triggers(unique=[RecurveBow()]),
    "3047": Triggers(unique=[Tabi()]),
    "3153": Triggers(unique=[Botrk()])
    # "4630": Triggers(unique=[Shadowflame()])
}


class ItemEntry(Entry):
    @classmethod
    def build(cls, data: Union[str, dict] = None, id_name: str = '', **kwargs) -> 'Entry':
        if isinstance(data, str):
            data = json.loads(data)
        elif not isinstance(data, dict):
            data = dict()

        new_data = dict()
        new_data['meta_data'] = data
        new_data['id_name'] = id_name
        new_data['triggers'] = _local_database.get(id_name, Triggers())
        return cls(new_data)

    def __repr__(self) -> str:
        s = f'{self.__class__.__name__}(name={self.data["id_name"]}, item_name={self.data["meta_data"]["name"]})'
        return s

class ItemDatabase(BaseDatabase):
    def __init__(self, *args, **kwargs):
        super(ItemDatabase, self).__init__(*args, **kwargs)
        self.fill_database(self.config.settings.items_path)

    def fill_database(self, path: str = None):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data = data['data']
        for key, value in data.items():
            self.data[key] = ItemEntry.build(data=value, id_name=key)

    @lru_cache(maxsize=200)
    def get(self, name: str, **kwargs):
        return self.data.get(name, ItemEntry.build())


if __name__ == '__main__':
    from lodca.configs.app_configs import DatabaseConfig

    cfg = DatabaseConfig()
    cfg.settings.items_path = '../../tests/temp/database/item.json'
    db = ItemDatabase(cfg)
    item = db.get('3020')
    print(item)
