from typing import Union

import epta.core as ec
import epta.core.base_ops as ecb

from lodca.engine.skill import SkillNode, Skill
from lodca.tools.scalings import LevelScaling, FlatStatScaling
from lodca.tools.stats import UnitStatGetter

from . import variables


class BasicAttack(SkillNode):
    def __init__(self, labels: Union[list, set] = None, **kwargs):
        tool_ = ecb.Compose(
            lambda ad: ad,
            (
                UnitStatGetter('player_unit', 'total_attack_damage'),
            )
        )
        labels = labels or {'basic_attack', 'physical', 'onhit'}
        super(BasicAttack, self).__init__(tool=tool_, labels=labels, name='BasicAttack', **kwargs)


class BonusDamage(SkillNode):
    # TODO: convert any skill to 'bonus' type?
    def __init__(self, *args, **kwargs):
        super(BonusDamage, self).__init__(*args, **kwargs)


class RecurveBow(SkillNode):
    def __init__(self, name: str = 'recurve_bow', **kwargs):
        tool_ = ecb.Lambda(lambda *_, **__: 15)
        labels = {'physical', 'bonus'}
        super(RecurveBow, self).__init__(tool=tool_, name=name, labels=labels, **kwargs)


class BotrkNode(SkillNode):
    def __init__(self, name: str = 'botrk', **kwargs):
        # TODO: lookup range in database, bot by value
        is_ranged = ecb.Compose(
            lambda attack_range: attack_range > 260,
            (
                UnitStatGetter('player_unit', 'base_attack_range'),
            )
        )
        range_scaling = ecb.Compose(
            lambda ranged: 0.08 if ranged else 0.12,
            (
                is_ranged,
            )
        )
        tool_ = ecb.Compose(
            lambda current_health, value: current_health * value,
            (
                UnitStatGetter('target_unit', 'current_health'),
                range_scaling
            ),
        )
        labels = ['physical', 'bonus']
        super(BotrkNode, self).__init__(tool=tool_, name=name, labels=labels, **kwargs)


class Botrk(Skill):
    def __init__(self, name: str = 'botrk', **kwargs):
        super(Botrk, self).__init__([BotrkNode()], name=name, **kwargs)


class ShadowflameNode(SkillNode):
    # Shadowflame damage stat in the item description shows damage before applying magic resist.
    def __init__(self, node: 'SkillNode', name: str = 'shadowflame', **kwargs):
        self._mres_tool = variables.PostMitigationDamageCoeff(resist=variables.EffectiveMagicResist())
        self._node = node

        self._current_health_getter = UnitStatGetter('target_unit', 'current_health')
        self._total_magic_pen_getter = UnitStatGetter('player_unit', 'total_magic_pen_flat')

        def _get_damage_value(game_state_snapshot: dict):
            current_health = self._current_health_getter(self._node.game_state_snapshot)
            # ['target_unit']['stats']['current_health']
            current_health = min(2500, max(1000, current_health))
            value = (-current_health + 4000) / 150
            current_value = self._total_magic_pen_getter(self._node.game_state_snapshot)
            # ['player_unit']['stats'].get('total_magic_pen_flat', 0)

            current_coeff = self._mres_tool(node.game_state_snapshot)
            node.game_state_snapshot['player_unit']['stats']['total_magic_pen_flat'] = current_value + value
            pen_coeff = self._mres_tool(node.game_state_snapshot)
            node.game_state_snapshot['player_unit']['stats']['total_magic_pen_flat'] = current_value

            # Have to calculate damage twice as to make it a different damage source.
            # Else modify skill's tool inline. Check previous commit for it.
            # node.tool has applied magic resit already.
            dmg = self._node._default_tool(node.game_state_snapshot)

            return dmg * (pen_coeff - current_coeff)

        tool_ = ecb.Lambda(_get_damage_value)
        labels = []  # ['magic']

        super(ShadowflameNode, self).__init__(tool=tool_, name=name, labels=labels, **kwargs)


class Shadowflame(Skill):
    def __init__(self, node: 'SkillNode', name: str = 'shadowflame', **kwargs):
        super(Shadowflame, self).__init__([ShadowflameNode(node)], name=name, **kwargs)


class IlluminationNode(SkillNode):
    def __init__(self, name: str = 'illumination', **kwargs):
        tool_ = ecb.Sum([
            LevelScaling('champion_level', [10 + 10 * lvl for lvl in range(0, 19)]),
            FlatStatScaling('total_ability_power', 0.2)
        ])

        labels = ['magic']
        super(IlluminationNode, self).__init__(tool=tool_, name=name, labels=labels, **kwargs)


class Illumination(Skill):
    def __init__(self, name: str = 'illumination', **kwargs):
        super(Illumination, self).__init__([IlluminationNode()], name=name, **kwargs)
