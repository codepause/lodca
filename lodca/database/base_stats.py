from functools import lru_cache
import json
from typing import Union

from lodca.tools.scalings import *

from lodca.database import Entry, BaseDatabase

name_mappings = {'hp': 'health', 'mp': 'mana', 'movespeed': 'move_speed',
                 'spellblock': 'magic_resist', 'attackrange': 'attack_range',
                 'hpregen': 'health_regen', 'mpregen': 'mana_regen',
                 'crit': 'critical_chance', 'attackdamage': 'attack_damage',
                 'attackspeed': 'attack_speed', 'armor': 'armor',
                 }
name_mappings = {key: f'base_{value}' for key, value in name_mappings.items()}

# TODO: split str and tool databases / caches
class StatEntry(Entry):
    @classmethod
    def build(cls, data: Union[str, dict] = None, **kwargs):
        """
        Create scalings for base stat growths.

        Args:
            data (str, dict): data to create from.

        Returns:
            Entry class for the given data.
        """
        if isinstance(data, str):
            data = json.loads(data)
        elif not isinstance(data, dict):
            data = dict()
        if 'stats' in data:
            data = data['stats']

        base_scalings = dict()
        for key, value in name_mappings.items():
            if key in data:
                base_scalings[value] = ecb.Sum()
            else:
                # for 'default' champion total == base
                base_scalings[value] = ecb.SoftAtomic(key=value.replace('base', 'total'), default_value=0.)

        for key, value in data.items():
            base_stat_name = key.replace('perlevel', '')
            base_stat_value = data.get(base_stat_name, 0.)
            name = name_mappings.get(base_stat_name, base_stat_name)

            # TODO: scaling for attack speed
            if 'perlevel' in key and 'attackspeed' not in key:  # ats has different formula
                scaling = StatLevelScaling(value)
            else:
                # Constant base value (lvl 1)
                scaling = ecb.Wrapper(base_stat_value)

            base_scalings[name].append(scaling)

        for key, value in base_scalings.items():
            # output should be {stat: value}
            base_scalings[key] = ecb.Compose(
                lambda k, v: {k: v},
                (
                    key,
                    value
                ),
                name=key
            )

        return cls(list(base_scalings.values()))


class BaseStatsDatabase(BaseDatabase):
    def __init__(self, *args, **kwargs):
        super(BaseStatsDatabase, self).__init__(*args, **kwargs)
        self.fill_database(self.config.settings.base_stats_path)

    def fill_database(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data = data['data']
        for key, value in data.items():
            self.data[key] = StatEntry.build(value)

    @lru_cache(maxsize=20)
    def get(self, name: str, **kwargs):
        data = self.data.get(name) or StatEntry.build()
        return data
