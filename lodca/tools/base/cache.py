from typing import Any
from functools import partial

import epta.core as ec


class BuilderCache(ec.ToolDict):
    """
    The way to build missing values. If the required key not present - build it with :attr:`builder`
    Built tools are stored in ``self._tools``.

    Args:
        builder (callable): to call on build.
    """
    def __init__(self, builder: callable, name: str = 'BuilderCache', **kwargs):
        super(BuilderCache, self).__init__(name=name, **kwargs)
        self.builder = builder

    def __getitem__(self, key: str) -> Any:
        if key not in self._tools:
            self._tools[key] = self.builder(key)
        return self._tools[key]

    def get(self, key: str, **kwargs):
        return self.__getitem__(key)


class DatabaseCache(BuilderCache):
    """
    Args:
        database (Database): From where to get data.
        builder (callable): function to customise building process.
            Default input for it is a :func:`~lodca.database.database_meta.BaseDatabase.get`.
    """
    def __init__(self, database: 'DataBase', builder: callable = partial, name: str = 'DatabaseCache', **kwargs):
        self.database = database
        builder = builder(partial(self.database.get))

        super(DatabaseCache, self).__init__(builder, name=name, **kwargs)
