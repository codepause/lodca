from typing import Mapping

from epta.core import *
from epta.core.base_ops import *
import epta.tools.base as etb

from lodca.tools.base import MultiCropper

from functools import partial


def build_spread_multi_cropper(pos_manager: Mapping[str, etb.PositionMapperWrapper], key: str,
                               n_rows: int = 1, n_cols: int = 1,
                               names: List[str] = None, name: str = None, **kwargs):
    if names is None:
        names = [f'placeholder_{idx}' for idx in range(n_rows * n_cols)]
    multi_cropper = Sequential([
        MultiCropper(n_rows=n_rows, n_cols=n_cols, position_manager=pos_manager, key=key),
        DataSpread(names)
    ], name=name)
    return multi_cropper


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
    'additional_stats': partial(build_spread_multi_cropper,
                                key='additional_stats',
                                name='additional_stats',
                                n_rows=4,
                                n_cols=2,
                                names=['health_regen', 'mana_regen',
                                       'armor_pen', 'magic_pen',
                                       'life_steal', 'vamp',
                                       'attack_range', 'tenacity']),
    'rune_stats': partial(build_spread_multi_cropper,
                          key='rune_stats',
                          name='rune_stats',
                          n_rows=4,
                          n_cols=2),
    'inventory': partial(build_spread_multi_cropper,
                         key='inventory',
                         name='inventory',
                         n_rows=2,
                         n_cols=3,
                         names=[f'item_{idx}' for idx in range(6)]),
    'skill_points': partial(build_spread_multi_cropper,
                            key='skill_points',
                            name='skill_points',
                            n_rows=1,
                            n_cols=4,
                            names=[f'skill_level_{idx}' for idx in range(4)]),
}


# TODO: merge with target croppers
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
