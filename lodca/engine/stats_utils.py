import itertools

import epta.core.base_ops as ecb


# be careful to use UNIQUE tool names.

# mapping from ocr to stats
def build_ocr_getters():
    def _build_stat_getter(lookup_name: str, store_name: str, default_value=None):
        tool_ = ecb.Sequential([
            ecb.SoftAtomic(key=lookup_name, default_value=default_value),
            ecb.Lambda(lambda res: {store_name: res} if res is not None else None)
        ],
            name=f'ocr_{store_name}'
        )
        return tool_

    ocr_stats_getters = [
        *[
            _build_stat_getter(key, key) for key in [
                'champion_level'
            ]
        ],
        *[
            _build_stat_getter(key, key) for key in [
                'current_health', 'current_mana',
                'total_health', 'total_mana',
                *[
                    f'skill_level_{i}' for i in range(4)
                ]
            ]
        ],
        *[
            _build_stat_getter(key, f'total_{key}') for key in [
                'attack_damage', 'ability_power', 'magic_resist',
                'attack_speed', 'ability_haste',
                'move_speed', 'health_regen', 'mana_regen',
                'attack_range', 'armor'
            ]
        ],
        *[
            _build_stat_getter(key, f'total_{key}') for key in [
                'critical_chance', 'life_steal', 'tenacity'
            ]
        ],
        _build_stat_getter('magic_pen_0', 'total_magic_pen_flat'),
        _build_stat_getter('magic_pen_1', 'total_magic_pen_perc'),
        _build_stat_getter('armor_pen_0', 'total_lethality'),
        _build_stat_getter('armor_pen_1', 'total_armor_pen_perc'),
        _build_stat_getter('vamp_0', 'total_physical_vamp'),
        _build_stat_getter('vamp_1', 'total_spell_vamp'),

    ]
    return ocr_stats_getters


def build_missing_getters():
    def _build_bonus_getter(name: str):
        # base stat may be higher than total:
        # base: float = 6.23 [source: lvl formula], total: int = 6 [source: ocr]
        # return None if bad rec happened
        tool_ = ecb.Compose(
            lambda total, base, nme: {f'bonus_{nme}': v} if (v := total - round(base)) > -1 else None,
            (
                ecb.SoftAtomic(key=f'total_{name}', default_value=0.),
                ecb.SoftAtomic(key=f'base_{name}', default_value=0.),
                name
            ),
            name=f'bonus_{name}'
        )
        return tool_

    def _build_missing_resource_getter(name: str):
        tool_ = ecb.Compose(
            lambda total, base, nme: {f'missing_{nme}': max(0, total - base)},
            (
                ecb.SoftAtomic(key=f'total_{name}', default_value=0.),
                ecb.SoftAtomic(key=f'current_{name}', default_value=0.),
                name
            ),
            name=f'missing_{name}'
        )
        return tool_

    def _build_perc_data(name: str, perc_name: str):
        # name - name for a stat (total will be taken)
        # perc_name - name for a stat to compute perc for
        tool_ = ecb.Compose(
            lambda total, flat, nme, mnme: {f'{mnme}_perc': 1. if total == 0 else min(flat / total, 1)},
            (
                ecb.SoftAtomic(key=f'total_{name}', default_value=0.),
                ecb.SoftAtomic(key=perc_name, default_value=0.),
                name,
                perc_name
            ),
            name=f'{perc_name}_perc'
        )
        return tool_

    def _build_to_perc(name: str):
        # convert name to rate: tenacity, crit etc.
        # write to the different value names as if not updated - it will stack operations.
        tool_ = ecb.Sequential([
            ecb.SoftAtomic(name),
            ecb.Lambda(lambda val: {f'{name}_rate': val / 100} if val is not None else None)
        ],
            name=f'{name}'
        )
        return tool_

    missing_stats_getters = [
        *[
            _build_bonus_getter(name) for name in [
                'health', 'mana',
                'attack_damage', 'ability_power', 'magic_resist',
                'attack_speed', 'ability_haste', 'critical_chance',
                'move_speed', 'health_regen', 'mana_regen',
                'life_steal', 'attack_range', 'tenacity', 'armor',
                'magic_pen_flat', 'magic_pen_perc', 'lethality',
                'armor_pen_perc', 'physical_vamp', 'spell_vamp'
            ]
        ],
        *[
            _build_missing_resource_getter('health'),
            _build_missing_resource_getter('mana')
        ],

        *[
            _build_perc_data('health', 'missing_health'),
            _build_perc_data('mana', 'missing_mana'),
            _build_perc_data('health', 'current_health'),
            _build_perc_data('mana', 'current_mana')
        ],
        *[
            _build_to_perc(name) for name in
            ['_'.join(key) for key in list(itertools.product(
                ['base', 'total'],
                ['critical_chance', 'life_steal', 'tenacity',
                 'magic_pen_perc', 'armor_pen_perc', 'physical_vamp', 'spell_vamp']))]
        ],
    ]
    return missing_stats_getters
