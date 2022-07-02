import copy

import epta.core.base_ops as ecb

from lodca.engine.skill import *
from lodca.engine.triggers import AddTrigger, RemoveTrigger, ActivateLabelsTriggers
from lodca.tools.stats import UnitStatGetter
from lodca.tools.scalings import LevelScaling, FlatStatScaling
import lodca.database.triggers as ldt

from .skills import BasicAttack, BonusDamage, IlluminationNode

local_skills_database = {
    'Lux':
        {
            'passive': Skill([
                IlluminationNode()
            ],
                name='Illumination',
                use_condition=ecb.Compose(
                    lambda a, b, c: a or b or c,
                    (
                        UnitStatGetter('player_unit', 'skill_level_0'),
                        UnitStatGetter('player_unit', 'skill_level_2'),
                        UnitStatGetter('player_unit', 'skill_level_3')
                    )
                )
            ),
            'auto_attack': Skill([
                Skill([  # it first procs passive
                    ActivateLabelsTriggers(labels=['illumination']),
                ],
                    name='Illumination',
                ),
                BasicAttack(labels=['basic_attack', 'physical', 'onhit']),
                RemoveTrigger(remove_name='Illumination'),  # removes illumination trigger after proc.
            ],
                name='Auto attack'),
            'q': Skill([
                SkillNode(
                    ecb.Sum([
                        LevelScaling('skill_level_0', [40 + skill_level * 40 for skill_level in range(0, 6)]),
                        FlatStatScaling('total_ability_power', 0.6)
                    ], ),
                    labels=['magic', 'spell'],
                    name='Light Binding',
                ),
                AddTrigger(ldt.Illumination),  # adds trigger for 'illumination' label.
            ],
                name='Light Binding',
                use_condition=UnitStatGetter('player_unit', 'skill_level_0')
            ),
            'r': Skill([
                Skill([  # it first procs passive
                    ActivateLabelsTriggers(labels=['illumination']),
                ],
                    name='Illumination',
                ),
                RemoveTrigger(remove_name='Illumination'),
                SkillNode(
                    ecb.Sum([
                        LevelScaling('skill_level_3', [200 + skill_level * 100 for skill_level in range(0, 4)]),
                        FlatStatScaling('total_ability_power', 1.0)
                    ], ),
                    labels=['magic', 'spell'],
                    name='Final Spark',
                ),
                AddTrigger(ldt.Illumination)
            ],
                name='Final Spark',
                use_condition=UnitStatGetter('player_unit', 'skill_level_3')
            ),

        },

    'Vayne':
        {
            'auto_attack': Skill([
                BasicAttack(),
            ],
                name='auto'),
            # Vayne Q does not get reduced by tabi.
            'q': Skill([
                BasicAttack(labels={'physical', 'onhit'}),
                BonusDamage(
                    FlatStatScaling(
                        'total_attack_damage',
                        LevelScaling(
                            'skill_level_0',
                            [0.55 + 0.05 * skill_level for skill_level in range(0, 6)]
                        )
                    ),
                    labels=['physical']
                ),
            ],
                name='Tumble'),
            # TODO: add cap vs monsters
            'w': Skill([
                BonusDamage(
                    ecb.Compose(
                        lambda dmg, min_dmg: max(dmg, min_dmg),
                        (
                            FlatStatScaling(
                                'total_health',
                                LevelScaling(
                                    'skill_level_1',
                                    [0.015 + 0.025 * skill_level for skill_level in range(0, 6)],
                                ),
                                unit_name='target_unit'
                            ),
                            LevelScaling(
                                'skill_level_1',
                                [35 + 15 * skill_level for skill_level in range(0, 6)]
                            )
                        )
                    ),
                    labels=['true']
                )
            ],
                name='Silver Bolts'
            )
        }
}

local_combos_database = {
    'Lux': {
        # copy and deepcopy are overridden in these classes.
        # copy due to skill nodes are unique.
        'combo': Skill([
            copy.deepcopy(local_skills_database['Lux']['q']),
            copy.deepcopy(local_skills_database['Lux']['r']),
            copy.deepcopy(local_skills_database['Lux']['auto_attack']),
        ],
            name='QRAuto'),
    }
}

"""
        'combo_2': Skill([
            copy.deepcopy(local_skills_database['Lux']['passive']),
            copy.deepcopy(local_skills_database['Lux']['auto_attack']),
        ], name='pAuto'),
        'combo_4': Skill([
            copy.deepcopy(local_skills_database['Lux']['q']),
            copy.deepcopy(local_skills_database['Lux']['auto_attack']),
        ],
            name='qAuto'),
        'combo_5': Skill([
            AddTrigger(ldt.Illumination),
            copy.deepcopy(local_skills_database['Lux']['auto_attack']),
        ],
            name='tAuto')
    }
}
"""