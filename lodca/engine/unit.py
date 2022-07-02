from functools import partial
from typing import Mapping, Dict, Any

from epta.core import ToolDict, BaseTool
from epta.core.base_ops import Sequential

from lodca.tools.base import DatabaseCache
from lodca.database.database import DataBase
from lodca.tools.base import Triggers

from .stats import Stats, StatsWrapper
from .items import Items, ItemsWrapper

import time


def wrap_stats(database_builder: callable):
    # database_builder is a partial function, input for it is is a champion_name
    return lambda champion_name: StatsWrapper(Stats(database_builder(champion_name)))


def wrap_items(database_builder: callable):
    # database_builder is a partial function, input for it is is a champion_name
    return lambda item_name: ItemsWrapper(Items(database_builder(item_name)))


class LocalCache:
    """
    Local cache for current unit stats and etc.
    Used to store already required and modified data from database.
    """

    def __init__(self, database: DataBase = None):
        if database is None:
            database = DataBase()
        self._database = database

        # TODO: replace this as it is too complex to follow
        self.stats = DatabaseCache(self._database.base_stats, builder=wrap_stats)
        self.items = ItemsWrapper(Items(self._database.items))
        # DatabaseCache(self._database.items, builder=wrap_items)
        self.champions = DatabaseCache(self._database.champions)


class Unit(BaseTool):
    def __init__(self, database: DataBase = None, name: str = 'Unit', **kwargs):
        super(Unit, self).__init__(name=name, **kwargs)
        self._cache = LocalCache(database)

        # current data:
        self.champion = None
        self.stats = None
        self.items = None

        self._default_triggers = Triggers()
        self.current_triggers = Triggers()

        self.update()

    def update_stats(self, ocr_data: dict, **kwargs):
        champion_name = ocr_data.get('champion_name', 'default')
        stats = self._cache.stats[champion_name]
        stats(ocr_data)
        self.stats = stats

    def update_items(self, ocr_data: dict, **kwargs):
        items = self._cache.items
        items(ocr_data)
        self.items = items

    def update_champion(self, ocr_data: dict, **kwargs):
        champion_name = ocr_data.get('champion_name', 'default')
        self.champion = self._cache.champions[champion_name]

    def reset_triggers(self):
        self.current_triggers.reset()

    def gather_triggers(self):
        self.current_triggers.merge(self._default_triggers)
        for item in self.items.values():
            if item:
                self.current_triggers.merge(item['triggers'])

    def update(self, ocr_data: dict = None):
        if ocr_data is None:
            ocr_data = dict()

        self.update_champion(ocr_data)
        self.update_stats(ocr_data)
        self.update_items(ocr_data)

        self.reset_triggers()
        self.gather_triggers()

    def set_stats(self, data: dict = None):
        self.stats._tools.update(data)

    def snapshot(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Snapshotting current game state. ``stats`` values are the copy of the current ones.
        Other values are pointers to the classes.

        Returns:
            dict
        """
        # TODO: prettify code
        # TODO: items.get_all() as triggers?
        return {
            'champion': self.champion, 'items': self.items,
            'stats': dict(self.stats._tools),
            'triggers': self.current_triggers
        }

    def use(self, *args, **kwargs) -> Dict[str, Any]:
        return self.snapshot(*args, **kwargs)

    def __getitem__(self, item):
        # TODO: change to ToolDict?
        return self.__dict__[item]
