from epta.core.base_ops import *

from lodca.tools.stats import UnitStatGetter

class EffectiveArmor(Variable):
    # https://leagueoflegends.fandom.com/wiki/Armor_penetration
    def __init__(self, **kwargs):
        effective_resist_after_pen_scale = Compose(
            lambda total_resist, scale_pen: total_resist if total_resist < 0 else total_resist * (1 - scale_pen / 100),
            (
                UnitStatGetter('target_unit', 'total_armor'),
                UnitStatGetter('player_unit', 'total_armor_pen_perc'),
            )
        )
        resist_pen_flat = Compose(
            lambda lethality, level: lethality * (0.6 + 0.4 * level / 18),
            (
                UnitStatGetter('player_unit', 'total_lethality'),
                UnitStatGetter('player_unit', 'champion_level', default_value=1),
            )
        )
        effective_resist_after_pen_flat = Compose(
            lambda resist, pen_flat: resist if resist < 0 else max(0, resist - pen_flat),
            (
                effective_resist_after_pen_scale,
                resist_pen_flat
            )
        )
        super(EffectiveArmor, self).__init__(tool=effective_resist_after_pen_flat, name='effective_armor', **kwargs)


class EffectiveMagicResist(Variable):
    # https://leagueoflegends.fandom.com/wiki/Magic_penetration
    def __init__(self, **kwargs):
        effective_resist_after_pen_scale = Compose(
            lambda total_resist, scale_pen: total_resist if total_resist < 0 else total_resist * (1 - scale_pen / 100),
            (
                UnitStatGetter('target_unit', 'total_magic_resist'),
                UnitStatGetter('player_unit', 'total_magic_pen_perc'),
            )
        )
        effective_resist_after_pen_flat = Compose(
            lambda resist, pen_flat: resist if resist < 0 else max(0, resist - pen_flat),
            (
                effective_resist_after_pen_scale,
                UnitStatGetter('player_unit', 'total_magic_pen_flat'),
            )
        )
        super(EffectiveMagicResist, self).__init__(tool=effective_resist_after_pen_flat, name='effective_magic_resist',
                                                   **kwargs)


class PostMitigationDamageCoeff(Variable):
    def __init__(self, name: str = 'PostMitigationDamageCoeff', resist: 'BaseTool' = None, **kwargs):
        if resist is None:
            resist = Lambda(lambda res_value, **kwgs: res_value)
        tool = Compose(
            lambda res_value: (2 - 100 / (100 - res_value)) if res_value < 0 else (
                    100 / (100 + res_value)),
            (
                resist,
            )
        )

        super(PostMitigationDamageCoeff, self).__init__(tool=tool, name=f'{name}', **kwargs)


class PostMitigationDamage(Variable):
    def __init__(self, resist: 'BaseTool', name: str = 'PostMitigationDamage', **kwargs):
        self.post_mitigation_coeff = PostMitigationDamageCoeff(resist=resist)
        tool = Lambda(lambda tool_: Product([tool_, self.post_mitigation_coeff]))
        super(PostMitigationDamage, self).__init__(tool=tool, name=f'{name}', **kwargs)
