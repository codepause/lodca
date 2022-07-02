import abc
from typing import Union, Any, Iterator

from lodca.configs.app_configs import DatabaseConfig

class Entry(abc.ABC):
    def __init__(self, data: Any, **kwargs):
        self.data = data
        super(Entry, self).__init__(**kwargs)

    @classmethod
    @abc.abstractmethod
    def build(cls, *args, **kwargs) -> 'Entry':
        pass

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[str]:
        return iter(self.data)


class BaseDatabase(abc.ABC):
    def __init__(self, config: 'Config' = None, **kwargs):
        self.data = dict()
        self.config = config or DatabaseConfig()

    @abc.abstractmethod
    def fill_database(self, *args, **kwargs):
        pass

    def get(self, name: str, **kwargs):
        return self.data.get(name, Entry.build())
