from typing import Union, Any

import epta.core as ec
import epta.core.base_ops as ecb


class UnitStatGetter(ecb.Variable):
    def __init__(self, unit_name: str, stat_name: str, default_value: Any = 0, name: str = 'UnitStatGetter', **kwargs):
        tool_ = ecb.Sequential([
            ecb.Atomic(unit_name),
            ecb.Atomic('stats'),
            ecb.SoftAtomic(stat_name, default_value=default_value)
        ])
        super(UnitStatGetter, self).__init__(tool=tool_, name=name, **kwargs)
