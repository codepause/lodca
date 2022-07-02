from typing import Union
import math

import epta
import epta.core.base_ops as ecb
import epta.core as ec

from lodca.tools.stats import UnitStatGetter


# STAT SCALINGS:
class _LevelScaling(ecb.Variable):
    def __init__(self, *args, **kwargs):
        scaling = ecb.Compose(
            lambda level: (level - 1) * (0.7025 + 0.0175 * (level - 1)),
            (
                ecb.SoftAtomic('champion_level', default_value=1),
            )
        )
        super(_LevelScaling, self).__init__(tool=scaling, **kwargs)


class StatLevelScaling(ecb.Variable):
    def __init__(self, value: float, **kwargs):
        scaling = ecb.Product([_LevelScaling(), ecb.Wrapper(value)])
        super(StatLevelScaling, self).__init__(tool=scaling, **kwargs)
# ======================================================================================================================

# SKILL SCALINGS:
class LevelScaling(ecb.Variable):
    def __init__(self, skill_key: str, values: list, unit_name: str = 'player_unit', **kwargs):
        self._scale_values = values
        self._max_skill_level = len(values) - 1
        tool_ = ecb.Compose(
            lambda skill_level: self._scale_values[max(0, min(skill_level, self._max_skill_level))],
            (
                UnitStatGetter(unit_name, skill_key),
            )
        )
        super(LevelScaling, self).__init__(tool=tool_, **kwargs)


class FlatStatScaling(ecb.Variable):
    def __init__(self, stat_key: str, value: Union[float, ecb.BaseTool], unit_name: str = 'player_unit', **kwargs):
        self._scale_value = value
        tool_ = ecb.Compose(
            lambda scale_value, stat_value: scale_value * stat_value,
            (
                self._scale_value,
                UnitStatGetter(unit_name, stat_key),
            )
        )
        super(FlatStatScaling, self).__init__(tool=tool_, **kwargs)

