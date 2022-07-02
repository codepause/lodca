def unit_ocr_stats_fill_test():
    from lodca.engine.unit import Unit
    import json

    data = """
        {
            "item_4": null,
            "attack_damage": 61,
            "ability_power": 221,
            "armor": 34,
            "magic_resist": 31,
            "attack_speed": 0.78,
            "ability_haste": 0,
            "critical_chance": 0,
            "move_speed": 400,
            "health_regen": 7,
            "mana_regen": 10,
            "magic_pen_0": 18,
            "magic_pen_1": 15,
            "life_steal": 0,
            "vamp_0": 0,
            "vamp_1": 0,
            "attack_range": 550,
            "placeholder_0": 0,
            "placeholder_1": 0,
            "placeholder_2": 0,
            "placeholder_3": 9,
            "placeholder_6": 5,
            "health_bar_0": 683,
            "health_bar_1": 683,
            "skill_level_3": 0,
            "champion_level": 4,
            "current_health": 683,
            "tenacity": 30,
            "total_health": 683,
            "current_mana": 533,
            "total_mana": 533,
            "item_0": {
                "name": "3089",
                "top_left": [
                    3,
                    2
                ],
                "value": 0.7962110638618469
            },
            "item_1": {
                "name": "3020",
                "top_left": [
                    3,
                    2
                ],
                "value": 0.7550195455551147
            },
            "item_2": {
                "name": "4630",
                "top_left": [
                    2,
                    2
                ],
                "value": 0.8322218060493469
            },
            "item_3": null,
            "item_5": null,
            "skill_level_0": 2,
            "skill_level_1": 0,
            "skill_level_2": 0,
            "champion_name": "Lux"
        }
    """
    data = json.loads(data)

    unit = Unit()

    unit.update(ocr_data=data)
    # unit.stats.use(data)
    # unit.stats.tool.keys() all getters

    print(unit.stats.items())

    return unit


def game_state_test():
    import copy
    from lodca.engine.game_state import GameState

    game_state = GameState()
    data = game_state()
    # game_state.player_unit = unit_ocr_stats_fill_test()
    # game_state.target_unit = copy.deepcopy(game_state.player_unit)

    return None


def skill_test():
    # triggers: {'magic': {m_res}, 'onhit': {botrk, luden}}
    # botrk: [tool, phys, onhit_label]
    # skill = [
    #   [tool, magic_trigger, spell](game_state_snapshot), -> tool
    #   [onhit_trigger], -> [onhit tools]
    #   [tool, crit, onhit] -> ([tool, onhit tools], [tool, onhit tools, critted])
    # ]
    # skill_2 = [[skill, crit], skill, [onhit]]

    # skill_3 = [[tool, magic, spell, onhit]] -> [[tool, magic, spell], [botrk, luden]] ->
    # [[tool, magic, spell], [tool, phys, onhit_label], [tool, magic, onhit_label]]

    import copy

    import epta.core.base_ops as ecb

    from lodca.engine.skill import SkillNode, Skill
    from lodca.engine.game_state import GameState
    from lodca.database.triggers import Tabi

    game_state = GameState()
    game_state.player_unit = unit_ocr_stats_fill_test()
    game_state.target_unit = unit_ocr_stats_fill_test()
    game_state.target_unit._default_triggers.add_unique(Tabi())
    game_state.update()

    # game_state
    # [tool, magic, spell]
    s = Skill([
        SkillNode(ecb.Lambda(lambda *_, **__: 150), labels=['magic', 'spell'], name='SimpleSkill')
    ])
    s.snapshot_state(game_state)
    print(s())
    # [[tool, magic, spell], [tool, magic]]
    s = Skill([
        SkillNode(ecb.Lambda(lambda *_, **__: 150), labels=['magic', 'spell'], name='SimpleSkill'),
        SkillNode(ecb.Lambda(lambda *_, **__: 100), labels=['magic'], name='SimpleSkill')
    ])
    s.snapshot_state(game_state)
    print(s())
    # [[tool, physical, spell, onhit], [tool, magic], [tool, physical]
    s = Skill([
        SkillNode(ecb.Lambda(lambda *_, **__: 150), labels=['base', 'spell', 'onhit'], name='OnHitSkill'),
        SkillNode(ecb.Lambda(lambda *_, **__: 100), labels=['magic'], name='SimpleSkill'),
        SkillNode(ecb.Lambda(lambda *_, **__: 150), labels=['base'], name='SimpleSkill')
    ])
    s.snapshot_state(game_state)
    print(s())
    return game_state


def lux_skill_test():
    import epta.core.base_ops as ecb
    import json

    from lodca.engine.skill import SkillNode, Skill
    from lodca.engine.game_state import GameState
    from lodca.database.triggers import Tabi
    from lodca.database.champion_skills import local_skills_database as cs_db

    lux_data = """{"attack_damage": 67, "ability_power": 118, "armor": 41, "magic_resist": 32, "attack_speed": 0.72, "ability_haste": 0, "critical_chance": 0, "move_speed": 330, "champion_level": 6, "current_health": 73, "total_health": 124, "current_mana": 5324, "total_mana": 37, "item_0": {"name": "4645", "top_left": [3, 2], "value": 0.7288370728492737}, "item_1": {"name": "1004", "top_left": [3, 2], "value": 0.860440194606781}, "item_2": null, "item_3": null, "item_4": null, "item_5": null, "skill_level_0": 2, "skill_level_1": 0, "skill_level_2": 3, "skill_level_3": 1, "champion_name": "Lux"}"""
    kayle_data = """{"attack_damage": 73, "ability_power": 0, "armor": 58, "magic_resist": 36, "attack_speed": 0.73, "ability_haste": 0, "critical_chance": 0, "move_speed": 414, "current_health": 1701, "current_mana": 527, "total_mana": 527, "item_0": {"name": "3047", "top_left": [2, 2], "value": 0.9419614672660828}, "item_1": {"name": "1028", "top_left": [3, 2], "value": 0.9502854943275452}, "item_2": {"name": "1028", "top_left": [2, 2], "value": 0.862642228603363}, "item_3": {"name": "1028", "top_left": [2, 2], "value": 0.8651837706565857}, "item_4": {"name": "1028", "top_left": [2, 2], "value": 0.9508500099182129}, "item_5": {"name": "1028", "top_left": [1, 2], "value": 0.8666967749595642}, "champion_name": "Kayle", "champion_level": 6, "total_health": 1701}"""

    game_state = GameState()

    def update():
        # reset triggers and refill values in data
        game_state.player_unit.update(json.loads(lux_data))
        game_state.target_unit.update(json.loads(kayle_data))
        game_state.update()

    from lodca.database.skills import Illumination
    update()
    print('Illumination:')
    print(Skill([Illumination()], name='Illumination')(game_state))
    print('Q:')
    print(cs_db['Lux']['q'](game_state))
    update()

    print('Auto:')
    print(cs_db['Lux']['auto_attack'](game_state))
    update()

    print('Q, Auto:')
    print(Skill([
        cs_db['Lux']['q'],
        cs_db['Lux']['auto_attack']
    ])(game_state))
    update()

    print('Q, R, Auto:')
    print(Skill([
        cs_db['Lux']['q'],
        cs_db['Lux']['r'],
        cs_db['Lux']['auto_attack'],
    ])(game_state))
    update()

    assert 'Illumination' not in game_state.triggers.unique
    # lux_1920_1080_minimap_on_left_scale_0.23_target_kayle_skillpoints2031_item_shadowflame.png
    return None


def triggers_test():
    import epta.core.base_ops as ecb
    import json
    import copy

    from lodca.engine.skill import SkillNode, Skill
    from lodca.engine.triggers import AddTrigger, RemoveTrigger, ActivateLabelsTriggers, ActivateUniqueTrigger
    from lodca.engine.game_state import GameState
    from lodca.database.triggers import Tabi, Illumination
    from lodca.database.champion_skills import local_skills_database as cs_db
    from lodca.database.skills import BasicAttack
    from lodca.database.skills import Illumination as Illumination_skill

    lux_data = """
    {"attack_damage": 150, "ability_power": 626, "armor": 41, "magic_resist": 32, "attack_speed": 0.72, 
    "ability_haste": 0, "critical_chance": 0, "move_speed": 330, "champion_level": 18, "current_health": 73, 
    "total_health": 124, "current_mana": 5324, "total_mana": 37,
    "magic_pen_0": 31, "magic_pen_1": 40,
    "item_0": {"name": "4645", "top_left": [3, 2], "value": 0.7288370728492737},
    "item_1": {"name": "3153", "top_left": [3, 2], "value": 0.860440194606781}, 
    "skill_level_0": 5, "skill_level_1": 5, "skill_level_2": 5, "skill_level_3": 3, "champion_name": "Lux"} 
    """
    kayle_data = """{"attack_damage": 73, "ability_power": 0,
     "armor": 170, "magic_resist": 170, "attack_speed": 0.73, "ability_haste": 0, "critical_chance": 0, "move_speed": 414,
      "current_health": 2100, "current_mana": 527, "total_mana": 527, "champion_name": "default",
       "champion_level": 6, "total_health": 2100}"""

    game_state = GameState()

    def update():
        # reset triggers and refill values in data
        game_state.player_unit.update(json.loads(lux_data))
        game_state.target_unit.update(json.loads(kayle_data))
        game_state.update()

    from lodca.database.skills import IlluminationNode
    update()

    s0 = Skill([
        AddTrigger(Illumination),
        ActivateUniqueTrigger('o', labels='illumination'),
        BasicAttack(labels=['basic_attack', 'physical', 'onhit']),
        RemoveTrigger(remove_name='Illumination'),  # removes illumination trigger after proc.
    ],
        name='sh_bt')
    s0.snapshot_state(game_state)
    s1 = copy.deepcopy(s0)
    s1.name = 'bt_sh'
    result_0 = s0()
    print()

    lux_data = """
        {"attack_damage": 150, "ability_power": 626, "armor": 41, "magic_resist": 32, "attack_speed": 0.72, 
        "ability_haste": 0, "critical_chance": 0, "move_speed": 330, "champion_level": 18, "current_health": 73, 
        "total_health": 124, "current_mana": 5324, "total_mana": 37,
        "magic_pen_0": 31, "magic_pen_1": 40,
        "item_1": {"name": "4645", "top_left": [3, 2], "value": 0.7288370728492737},
        "item_0": {"name": "3153", "top_left": [3, 2], "value": 0.860440194606781}, 
        "skill_level_0": 5, "skill_level_1": 5, "skill_level_2": 5, "skill_level_3": 3, "champion_name": "Lux"} 
        """
    update()
    result_1 = s1()
    # assert sum([s.value for s in result_0 if s.value]) != sum([s.value for s in result_1 if s.value])
    return None


if __name__ == '__main__':
    unit_ocr_stats_fill_test()
    game_state_test()
    skill_test()
    lux_skill_test()
    triggers_test()
    pass
