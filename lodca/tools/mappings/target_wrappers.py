from typing import Mapping

from epta.core import *
from epta.core.base_ops import *
import epta.tools.base as etb

from . import wrappers as wrp


class StatsWrapper(ToolDict):
    # wrapper with global position manager
    def __init__(self, position_manager: Mapping[str, etb.PositionMapperWrapper], key: str, **kwargs):
        self.position_manager = position_manager
        self.key = key
        tools = dict(self.position_manager[key].tool)

        tools['x'] = Compose(
            lambda pm, nm: pm[self.key].get('w', 0) + pm[self.key].get(f'attack_damage_{nm}', 0) - pm['interface'].get(
                nm, 0),
            (
                Wrapper(self.position_manager),
                'x'
            )
        )
        tools['y'] = Compose(
            lambda pm, nm: pm[self.key].get(f'attack_damage_{nm}', 0) - pm['interface'].get(nm, 0),
            (
                Wrapper(self.position_manager),
                'y'
            )
        )
        tools['w'], tools['step_w'] = tools['step_w'], tools['w']
        super(StatsWrapper, self).__init__(tools=tools, **kwargs)


class ActualManager(ToolDict):
    def __init__(self, relative_manager: Mapping[str, etb.PositionMapperWrapper], name: str = 'actual_manager',
                 **kwargs):
        tools = [
            etb.PositionMapperWrapper(mapper) for mapper in
            [
                # all of them are wrapped to match hooked coordinates because of relative.
                wrp.RelativeInterfaceWrapper(relative_manager, key='interface', name='interface'),
                *[
                    wrp.InventoryWrapper(relative_manager, key='inventory', name='inventory'),
                    StatsWrapper(relative_manager, key='stats', name='stats'),

                ],
                *[
                    wrp.RelativeWrapper(relative_manager, key=key, name=key)
                    for key in [
                        # 'health_bar', 'mana_bar',
                        'champion_level', 'current_health',
                        'total_health', 'current_mana', 'total_mana', 'champion', 'indicator'
                    ]
                ]
            ]
        ]
        super(ActualManager, self).__init__(tools=tools, name=name, **kwargs)
