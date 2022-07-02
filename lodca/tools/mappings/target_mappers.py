from functools import partial

from epta.core import *
from epta.core.base_ops import *
import epta.tools.base as etb

from .utils import linear_interpolation as lint


class RelativePositionMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'fixed_point', **kwargs):
        tools = dict(
            relative_x=partial(lint((0., 0.), (1., 0.)), game_config),
            relative_y=partial(lint((0., 0.), (1., 0.)), game_config),
        )
        super(RelativePositionMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class ItemMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'item', **kwargs):
        tools = dict(
            w=partial(lint((0., 18.), (1., 26.)), game_config),
            h=partial(lint((0., 18.), (1., 27.)), game_config),
        )
        super(ItemMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeInventoryPositionMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'inventory', **kwargs):
        tools = dict(
            x=partial(lint((0., 90.), (1., 138.)), game_config),
            y=partial(lint((0., 53.), (1., 80.)), game_config),
            step_w=partial(lint((0., -0.3), (1., -0.5)), game_config),
            step_h=partial(lint((0., 0.), (1., 0.)), game_config),

            crop_w=partial(lint((0., 20.), (1., 30.)), game_config),
            crop_h=partial(lint((0., 20.), (1., 30.)), game_config),
        )
        super(RelativeInventoryPositionMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeHealthBarMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'health_bar', **kwargs):
        tools = dict(
            x=partial(lint((0., 134.), (1., 204.)), game_config),
            y=partial(lint((0., 25.), (1., 39.)), game_config),
            w=partial(lint((0., 93.), (1., 141.)), game_config),
            h=partial(lint((0., 13.), (1., 19.)), game_config),
            slash_w=partial(lint((0., 8.), (1., 10.)), game_config),
        )
        super(RelativeHealthBarMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeManaBarMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'mana_bar', **kwargs):
        tools = dict(
            x=partial(lint((0., 134.), (1., 204.)), game_config),
            y=partial(lint((0., 38.), (1., 58.)), game_config),
            w=partial(lint((0., 93.), (1., 141.)), game_config),
            h=partial(lint((0., 13.), (1., 19.)), game_config),
            slash_w=partial(lint((0., 8.), (1., 10.)), game_config),
        )
        super(RelativeManaBarMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeCurrentHealthMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'current_health', **kwargs):
        tools = dict(
            x=partial(lint((0., 135.), (1., 204.)), game_config),
            y=partial(lint((0., 25.), (1., 39.)), game_config),
            w=partial(lint((0., 40.), (1., 60.)), game_config),
            h=partial(lint((0., 13.), (1., 19.)), game_config),
        )
        super(RelativeCurrentHealthMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeCurrentManaMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'current_mana', **kwargs):
        tools = dict(
            x=partial(lint((0., 135.), (1., 204.)), game_config),
            y=partial(lint((0., 38.), (1., 58.)), game_config),
            w=partial(lint((0., 40.), (1., 60.)), game_config),
            h=partial(lint((0., 13.), (1., 19.)), game_config),
        )
        super(RelativeCurrentManaMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeTotalHealthMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'total_health', **kwargs):
        tools = dict(
            x=partial(lint((0., 184.), (1., 277.)), game_config),
            y=partial(lint((0., 25.), (1., 39.)), game_config),
            w=partial(lint((0., 38.), (1., 60.)), game_config),
            h=partial(lint((0., 13.), (1., 19.)), game_config),
        )
        super(RelativeTotalHealthMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeTotalManaMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'total_mana', **kwargs):
        tools = dict(
            x=partial(lint((0., 184.), (1., 277.)), game_config),
            y=partial(lint((0., 38.), (1., 58.)), game_config),
            w=partial(lint((0., 38.), (1., 60.)), game_config),
            h=partial(lint((0., 13.), (1., 19.)), game_config),
        )
        super(RelativeTotalManaMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeChampionLevelMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'champion_level', **kwargs):
        tools = dict(
            x=partial(lint((0., 116.), (1., 176.)), game_config),
            y=partial(lint((0., 35.), (1., 53.)), game_config),
            w=partial(lint((0., 15.), (1., 22.)), game_config),
            h=partial(lint((0., 14.), (1., 22.)), game_config),
        )
        super(RelativeChampionLevelMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeChampionMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'champion', **kwargs):
        tools = dict(
            x=partial(lint((0., 91.), (1., 138.)), game_config),
            y=partial(lint((0., 10.), (1., 15.)), game_config),
            w=partial(lint((0., 40.), (1., 60.)), game_config),
            h=partial(lint((0., 40.), (1., 60.)), game_config),
        )
        super(RelativeChampionMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeStatsMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'stats', **kwargs):
        tools = dict(
            w=partial(lint((0., 12.), (1., 18.)), game_config),  # icon
            h=partial(lint((0., 12.), (1., 18.)), game_config),
            step_w=partial(lint((0., 28.), (1., 42.)), game_config),
            step_h=partial(lint((0., 5.), (1., 8.)), game_config),
            attack_damage_x=partial(lint((0., 9.), (1., 14.)), game_config),
            attack_damage_y=partial(lint((0., 10.), (1., 15.)), game_config),
        )
        super(RelativeStatsMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeInterfaceMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'interface', **kwargs):
        tools = dict(
            w=partial(lint((0., 246.), (1., 374.)), game_config),
            h=partial(lint((0., 86.), (1., 133.)), game_config),
        )
        super(RelativeInterfaceMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeIndicatorMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'indicator', **kwargs):
        tools = dict(
            x=partial(lint((0., 0.), (1., 0.)), game_config),
            y=partial(lint((0., 5.), (1., 5.)), game_config),
            w=partial(lint((0., 4.), (1., 4.)), game_config),
            h=partial(lint((0., 10.), (1., 10.)), game_config),
        )
        super(RelativeIndicatorMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeManager(ToolDict):
    """
    Storage to get relative values from.
    """

    def __init__(self, cfg: 'Config', name: str = 'relative_manager', **kwargs):
        tools = [
            etb.PositionMapperWrapper(mapper) for mapper in
            [
                *[
                    cls(cfg) for cls in [
                        RelativeInterfaceMapper,
                        RelativePositionMapper, RelativeInventoryPositionMapper,
                        # RelativeHealthBarMapper, RelativeManaBarMapper,
                        RelativeChampionLevelMapper, RelativeChampionMapper,
                        RelativeStatsMapper, RelativeTotalHealthMapper,
                        RelativeCurrentHealthMapper, RelativeTotalManaMapper, RelativeCurrentManaMapper,
                        ItemMapper, RelativeIndicatorMapper
                    ]
                ]
            ]
        ]
        super(RelativeManager, self).__init__(tools=tools, name=name, **kwargs)
