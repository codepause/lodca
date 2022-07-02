from types import FunctionType
from functools import partial

from epta.core import *
from epta.core.base_ops import *
import epta.tools.base as etb

from .utils import linear_interpolation as lint


class RelativePositionMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'fixed_point', **kwargs):
        tools = dict(
            relative_x=partial(lint((0., 958.), (1., 958.)), game_config),
            relative_y=partial(lint((0., 1035.), (1., 1015.)), game_config),
        )
        super(RelativePositionMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeInterfaceMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'interface', **kwargs):
        tools = dict(
            y=partial(lint((0., -141.), (1., -220.)), game_config),
            w=partial(lint((0., 513. + 296.), (1., 778. + 444.)), game_config),
            h=partial(lint((0., 143. + 45.), (1., 214. + 65.)), game_config),
        )
        super(RelativeInterfaceMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)

    # Define custom update
    def update(self, *args, **kwargs):
        if self.config.settings.minimap_on_left:
            self['x'] = partial(lint((0., -296.), (1., -444)), self.config)
        else:
            self['x'] = partial(lint((0., -535.), (1., -808.)), self.config)


class RelativeHealthBarMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'health_bar', **kwargs):
        tools = dict(
            x=partial(lint((0., -186.), (1., -282.)), game_config),
            y=partial(lint((0., 10.), (1., 15.)), game_config),
            w=partial(lint((0., 280.), (1., 422.)), game_config),
            h=partial(lint((0., 16.), (1., 16.)), game_config),
            slash_w=partial(lint((0., 8.), (1., 10.)), game_config)
        )
        super(RelativeHealthBarMapper, self).__init__(config=game_config, tools=tools, name=name,**kwargs)


class RelativeManaBarMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'mana_bar', **kwargs):
        tools = dict(
            x=partial(lint((0., -186.), (1., -282.)), game_config),
            y=partial(lint((0., 22.), (1., 34.)), game_config),
            w=partial(lint((0., 280.), (1., 422.)), game_config),
            h=partial(lint((0., 16.), (1., 16.)), game_config),
            slash_w=partial(lint((0., 8.), (1., 10.)), game_config),
        )
        super(RelativeManaBarMapper, self).__init__(config=game_config, tools=tools, name=name,**kwargs)


class RelativeCurrentHealthMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'current_health',  **kwargs):
        tools = dict(
            x=partial(lint((0., -116.), (1., -177.)), game_config),
            y=partial(lint((0., 8.), (1., 15.)), game_config),
            w=partial(lint((0., 70.), (1., 105.)), game_config),
            h=partial(lint((0., 16.), (1., 16.)), game_config),
        )
        super(RelativeCurrentHealthMapper, self).__init__(config=game_config, tools=tools, name=name,**kwargs)


class RelativeCurrentManaMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'current_mana',**kwargs):
        tools = dict(
            x=partial(lint((0., -116.), (1., -177.)), game_config),
            y=partial(lint((0., 22.), (1., 34.)), game_config),
            w=partial(lint((0., 70.), (1., 105.)), game_config),
            h=partial(lint((0., 16.), (1., 16.)), game_config),
        )
        super(RelativeCurrentManaMapper, self).__init__(config=game_config, tools=tools, name=name,**kwargs)


class RelativeTotalHealthMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'total_health', **kwargs):
        tools = dict(
            x=partial(lint((0., -38.), (1., -61.)), game_config),
            y=partial(lint((0., 8.), (1., 15.)), game_config),
            w=partial(lint((0., 65.), (1., 115.)), game_config),
            h=partial(lint((0., 16.), (1., 16.)), game_config),
        )
        super(RelativeTotalHealthMapper, self).__init__(config=game_config, tools=tools, name=name,**kwargs)


class RelativeTotalManaMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'total_mana', **kwargs):
        tools = dict(
            x=partial(lint((0., -38.), (1., -61.)), game_config),
            y=partial(lint((0., 22.), (1., 34.)), game_config),
            w=partial(lint((0., 65.), (1., 115.)), game_config),
            h=partial(lint((0., 16.), (1., 16.)), game_config)
        )
        super(RelativeTotalManaMapper, self).__init__(config=game_config, tools=tools, name=name,**kwargs)


class RelativeSkillPointsMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'skill_points',**kwargs):
        tools = dict(
            x=partial(lint((0., -147.), (1., -225.)), game_config),
            y=partial(lint((0., 0.), (1., -3.5)), game_config),
            h=partial(lint((0., 6.), (1., 10.)), game_config),
        )
        super(RelativeSkillPointsMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeChampionLevelMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'champion_level', **kwargs):
        tools = dict(
            x=partial(lint((0., -228.), (1., -341.)), game_config),
            y=partial(lint((0., 15.), (1., 25.)), game_config),
            w=partial(lint((0., 19.), (1., 27.)), game_config),
            h=partial(lint((0., 19.), (1., 27.)), game_config),
        )
        super(RelativeChampionLevelMapper, self).__init__(config=game_config, tools=tools, name=name,**kwargs)


class RelativePassiveMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'passive', **kwargs):
        tools = dict(
            x=partial(lint((0., -184.), (1., -278.)), game_config),
            y=partial(lint((0., -43.), (1., -66.)), game_config),
            w=partial(lint((0., 26.), (1., 39.)), game_config),
            h=partial(lint((0., 26.), (1., 39.)), game_config),
        )
        super(RelativePassiveMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)


class RelativeStatsMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'stats', **kwargs):
        tools = dict(
            w=partial(lint((0., 15.), (1., 22.)), game_config),  # icon
            h=partial(lint((0., 15.), (1., 22.)), game_config),
            step_w=partial(lint((0., 48.), (1., 72.)), game_config),
            step_h=partial(lint((0., 5.), (1., 8.)), game_config),

            masteries_step_w=partial(lint((0., 44.), (1., 67.)), game_config),
            masteries_step_h=partial(lint((0., 6.), (1., 9.)), game_config),
            masteries_w=partial(lint((0., 15.), (1., 22.)), game_config),
            masteries_h=partial(lint((0., 15.), (1., 22.)), game_config),

            health_regen_y=partial(lint((0., -130.), (1., -200.)), game_config),
        )
        super(RelativeStatsMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)

    def update(self, *args, **kwargs):
        if self.config.settings.minimap_on_left:
            self['attack_speed_x'] = partial(lint((0., 253.), (1., 385.)), self.config)
            self['attack_speed_y'] = partial(lint((0., 0.), (1., 0.)), self.config)
        else:
            self['attack_speed_x'] = partial(lint((0., -395.), (1., -594.)), self.config)
            self['attack_speed_y'] = partial(lint((0., 0.), (1., 0.)), self.config)


class RelativeInventoryPositionMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'inventory', **kwargs):
        tools = dict(
            x=partial(lint((0., 112.), (1., 170.)), game_config),
            y=partial(lint((0., -45.), (1., -70.)), game_config),
            step_w=partial(lint((0., 1.6), (1., 4.)), game_config),
            step_h=partial(lint((0., 0.5), (1., 1.)), game_config),

            crop_w=partial(lint((0., 31.), (1., 45.)), game_config),
            crop_h=partial(lint((0., 31.), (1., 45.)), game_config),
        )
        super(RelativeInventoryPositionMapper, self).__init__(config=game_config, tools=tools, name=name,**kwargs)


class SkillMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'skill', **kwargs):
        tools = dict(
            w=partial(lint((0., 40.), (1., 60.)), game_config),
            h=partial(lint((0., 40.), (1., 60.)), game_config),
            step_w=partial(lint((0., 4.), (1., 8.)), game_config),
        )
        super(SkillMapper, self).__init__(config=game_config, tools=tools, name=name,**kwargs)


class ItemMapper(ToolDict, ConfigDependent):
    def __init__(self, game_config: 'Config', name: str = 'item', **kwargs):
        tools = dict(
            w=partial(lint((0., 28.), (1., 43.)), game_config),
            h=partial(lint((0., 28.), (1., 43.)), game_config),
        )
        super(ItemMapper, self).__init__(config=game_config, tools=tools, name=name, **kwargs)

# TODO: add relative mapper
class RelativeManager(ToolDict, ConfigDependent):
    def __init__(self, cfg: 'Config', name: str = 'relative_manager', **kwargs):
        tools = [
            etb.PositionMapperWrapper(mapper) for mapper in
            [
                *[
                    cls(cfg) for cls in [
                        RelativePositionMapper,
                        RelativeInterfaceMapper, RelativePositionMapper, RelativeInventoryPositionMapper,
                        # RelativeHealthBarMapper, RelativeManaBarMapper,
                        RelativeSkillPointsMapper, RelativeChampionLevelMapper,
                        SkillMapper, RelativePassiveMapper, RelativeStatsMapper, RelativeTotalHealthMapper,
                        RelativeCurrentHealthMapper, RelativeTotalManaMapper, RelativeCurrentManaMapper,
                        ItemMapper
                    ]
                ]
            ]
        ]
        super(RelativeManager, self).__init__(config=cfg, tools=tools, name=name, **kwargs)
