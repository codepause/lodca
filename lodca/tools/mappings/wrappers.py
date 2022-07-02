from typing import Mapping

from epta.core import *
from epta.core.base_ops import *
import epta.tools.base as etb


class RelativeInterfaceWrapper(ToolDict):
    # wrapper with global position manager
    def __init__(self, position_manager: Mapping[str, etb.PositionMapperWrapper], key: str, **kwargs):
        self.position_manager = position_manager
        self.key = key
        tools = dict(self.position_manager[key].tool)
        for name in ['x', 'y']:
            tools[name] = Compose(
                lambda pm, nm: pm['fixed_point'].get(f'relative_{nm}', 0) + pm[self.key].get(nm, 0),
                (
                    Wrapper(self.position_manager),
                    name
                )
            )
        super(RelativeInterfaceWrapper, self).__init__(tools=tools, **kwargs)


class RelativeWrapper(ToolDict):
    # wrapper with global position manager
    def __init__(self, position_manager: Mapping[str, etb.PositionMapperWrapper], key: str, **kwargs):
        self.position_manager = position_manager
        self.key = key
        tools = dict(self.position_manager[key].tool)
        for name in ['x', 'y']:
            tools[name] = Compose(
                lambda pm, nm: pm[self.key].get(nm, 0) - pm['interface'].get(nm, 0),
                (
                    Wrapper(self.position_manager),
                    name
                )
            )
        super(RelativeWrapper, self).__init__(tools=tools, **kwargs)


class InventoryWrapper(ToolDict):
    # wrapper with global position manager
    def __init__(self, position_manager: Mapping[str, etb.PositionMapperWrapper], key: str, **kwargs):
        self.position_manager = position_manager
        self.key = key
        tools = dict(self.position_manager[key].tool)

        for name in ['x', 'y']:
            tools[name] = Compose(
                lambda pm, nm: pm[self.key].get(nm, 0) - pm['interface'].get(nm, 0),
                (
                    Wrapper(self.position_manager),
                    name
                )
            )
        for name in ['w', 'h']:
            tools[name] = Compose(
                lambda pm, nm: pm[self.key].get(f'crop_{nm}', 0),
                (
                    Wrapper(self.position_manager),
                    name
                )
            )

        super(InventoryWrapper, self).__init__(tools=tools, **kwargs)


class SkillPointsWrapper(ToolDict):
    # wrapper with global position manager
    def __init__(self, position_manager: Mapping[str, etb.PositionMapperWrapper], key: str, **kwargs):
        self.position_manager = position_manager
        self.key = key
        tools = dict(self.position_manager[key].tool)

        for name in ['x', 'y']:
            tools[name] = Compose(
                lambda pm, nm: pm[self.key].get(nm, 0) - pm['interface'].get(nm, 0),
                (
                    Wrapper(self.position_manager),
                    name
                )
            )
        for name in ['w', 'step_w']:
            tools[name] = Compose(
                lambda pm, nm: position_manager['skill'].get(nm, 0),
                (
                    Wrapper(self.position_manager),
                    name
                )
            )
        super(SkillPointsWrapper, self).__init__(tools=tools, **kwargs)


class StatsWrapper(ToolDict):
    # wrapper with global position manager
    def __init__(self, position_manager: Mapping[str, etb.PositionMapperWrapper], key: str, **kwargs):
        self.position_manager = position_manager
        self.key = key
        tools = dict(self.position_manager[key].tool)

        tools['x'] = Compose(
            lambda pm, nm: 1.2 * pm[self.key].get('w', 0) + pm[self.key].get(f'attack_speed_{nm}', 0) - pm[
                'interface'].get(nm, 0),
            (
                Wrapper(self.position_manager),
                'x'
            )
        )
        tools['y'] = Compose(
            lambda pm, nm: -2 * (pm[self.key].get('h', 0) + pm[self.key].get('step_h', 0)) + pm[self.key].get(
                f'attack_speed_{nm}', 0) -
                           pm['interface'].get(nm, 0),
            (
                Wrapper(self.position_manager),
                'y'
            )
        )
        tools['w'], tools['step_w'] = tools['step_w'], tools['w']
        super(StatsWrapper, self).__init__(tools=tools, **kwargs)


class AdditionalStatsWrapper(ToolDict):
    # wrapper with global position manager
    def __init__(self, position_manager: Mapping[str, etb.PositionMapperWrapper], key: str, **kwargs):
        self.position_manager = position_manager
        self.key = key
        tools = dict(self.position_manager[key].tool)

        tools['x'] = Compose(
            lambda pm, nm: 1.2 * pm[self.key].get('w', 0) + pm[self.key].get(f'attack_speed_{nm}', 0) - pm[
                'interface'].get(nm, 0),
            (
                Wrapper(self.position_manager),
                'x'
            )
        )
        tools['y'] = Compose(
            lambda pm, nm: pm[self.key].get('health_regen_y', 0) - pm['interface'].get(nm, 0),
            (
                Wrapper(self.position_manager),
                'y'
            )
        )
        tools['w'], tools['step_w'] = tools['step_w'], tools['w']
        super(AdditionalStatsWrapper, self).__init__(tools=tools, **kwargs)


class RuneStatsWrapper(ToolDict):
    # wrapper with global position manager
    def __init__(self, position_manager: Mapping[str, etb.PositionMapperWrapper], key: str, **kwargs):
        self.position_manager = position_manager
        self.key = key
        tool_: 'ConfigTool' = self.position_manager[key].tool
        tools = dict(tool_)

        def _fnc(pm: Mapping[str, Any], nm: str, cfg: 'Config'):
            positions = pm[self.key]
            val = 1.2 * positions.get('w', 0) + positions.get(f'attack_speed_{nm}', 0) - pm['interface'].get(nm, 0)
            offset = 2 * positions.get('step_w', 0) + 2 * positions.get('w', 0) + 1.5 * positions.get('step_h', 0)
            if cfg.settings.minimap_on_left:
                return val + offset
            else:
                return val - offset

        tools['x'] = Compose(
            _fnc,
            (
                Wrapper(self.position_manager),
                'x',
                Wrapper(tool_.config)
            )
        )
        tools['y'] = Compose(
            lambda pm, nm: -2 * (pm[self.key].get('h', 0) + pm[self.key].get('step_h', 0)) + pm[self.key].get(
                f'attack_speed_{nm}', 0) -
                           pm['interface'].get(nm, 0),
            (
                Wrapper(self.position_manager),
                'y'
            )
        )
        tools['w'], tools['step_w'] = tools['masteries_step_w'], tools['masteries_w']
        super(RuneStatsWrapper, self).__init__(tools=tools, **kwargs)


class ActualManager(ToolDict):
    """
    Storage to get absolute values from.
    """
    def __init__(self, relative_manager: Mapping[str, etb.PositionMapperWrapper], name: str = 'actual_manager',
                 **kwargs):
        tools = [
            etb.PositionMapperWrapper(mapper) for mapper in
            [
                # all of them are wrapped to match hooked coordinates because of relative.
                RelativeInterfaceWrapper(relative_manager, key='interface', name='interface'),
                *[
                    InventoryWrapper(relative_manager, key='inventory', name='inventory'),
                    StatsWrapper(relative_manager, key='stats', name='stats'),
                    AdditionalStatsWrapper(relative_manager, key='stats', name='additional_stats'),
                    RuneStatsWrapper(relative_manager, key='stats', name='rune_stats'),
                    SkillPointsWrapper(relative_manager, key='skill_points', name='skill_points')
                ],
                *[
                    RelativeWrapper(relative_manager, key=key, name=key)
                    for key in [
                        # 'health_bar', 'mana_bar',
                        'champion_level', 'current_health',
                        'total_health', 'current_mana', 'total_mana'
                    ]
                ]
            ]
        ]
        super(ActualManager, self).__init__(tools=tools, name=name, **kwargs)
