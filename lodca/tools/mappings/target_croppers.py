from typing import Mapping

from epta.core.base_ops import *
import epta.tools.base as etb

from functools import partial

from .croppers import build_spread_multi_cropper

builders = {
    'stats': partial(build_spread_multi_cropper,
                     key='stats',
                     name='stats',
                     n_rows=4,
                     n_cols=2,
                     names=['attack_damage', 'ability_power',
                            'armor', 'magic_resist',
                            'attack_speed', 'ability_haste',
                            'critical_chance', 'move_speed']),

    'inventory': partial(build_spread_multi_cropper,
                         key='inventory',
                         name='inventory',
                         n_rows=1,
                         n_cols=6,
                         names=[f'item_{idx}' for idx in range(6)]
                         ),
}


# TODO: merge with croppers
class CropperManager(Sequential):
    def __init__(self, position_manager: Mapping[str, etb.PositionMapperWrapper], build_names: List[str] = None,
                 name='cropper_manager', **kwargs):
        # TODO: move this to settings and add registry
        if build_names is None:
            build_names = list()
        local_tools = list()
        for build_name in build_names:
            if build_name in builders:
                tool_ = builders[build_name](position_manager)
            else:
                tool_ = Compose(
                    lambda res, nm: {nm: res},
                    (
                        etb.PositionCropper(position_manager=position_manager, key=build_name, name=build_name),
                        build_name
                    )
                )

            local_tools.append(tool_)

        tools = [
            Concatenate(local_tools),
            DataSpread(build_names)
        ]
        super(CropperManager, self).__init__(name=name, tools=tools, **kwargs)
