from epta.core.base_ops import *

from lodca.tools.triggers import *

from . import skills


class Shadowflame_0(LabelTrigger):
    # NOT THE ACTUAL SHADOWFLAME. heh
    # https://leagueoflegends.fandom.com/wiki/(ToolDict, ConfigDependent)
    def __init__(self, name: str = 'Shadowflame', **kwargs):
        super(Shadowflame_0, self).__init__(labels=['offensive'], trigger_on='magic', name=name, **kwargs)

    def use(self, game_state: 'GameState', node: 'SkillNode', **kwargs):
        current_health = node.game_state_snapshot['target_unit']['stats']['current_health']
        current_health = min(2500, max(1000, current_health))
        value = (-current_health + 4000) / 150
        current_value = node.game_state_snapshot['player_unit']['stats'].get('total_magic_pen_flat', 0)
        node.game_state_snapshot['player_unit']['stats']['total_magic_pen_flat'] = current_value + value
        print('magic_pen_flat', value)
        # TODO: update stats after change in values


class Shadowflame(OnHitTrigger):
    # https://leagueoflegends.fandom.com/wiki/Shadowflame
    def __init__(self, name: str = 'Shadowflame', **kwargs):
        super(Shadowflame, self).__init__(skill_instance=skills.ShadowflameNode, labels=['offensive'],
                                          trigger_on='magic', name=name, **kwargs)

    def is_usable(self, game_state: 'GameState', node: 'SkillNode', **kwargs) -> bool:
        # exclude infinite procs
        if self.trigger_on in node.labels and node.name != 'shadowflame':
            return True
        return False

    def use(self, game_state: 'GameState', node: 'SkillNode', skill: 'Skill' = None, **kwargs):
        # print('shadowflame trigger has added a shadowflame skill')
        skill.node_queue.put(self.skill_instance(node))


class Botrk(OnHitTrigger):
    # https://leagueoflegends.fandom.com/wiki/Blade_of_the_Ruined_King
    # if both shadowflame and botrk in the inventory - shadowflame damages first.
    def __init__(self, name: str = 'Botrk', **kwargs):
        super(Botrk, self).__init__(labels=['offensive'], skill_instance=skills.Botrk, name=name, **kwargs)

    def use(self, game_state: 'GameState', node: 'SkillNode', skill: 'Skill' = None, **kwargs):
        # print('botrk trigger has added a botrk skill')
        skill.node_queue.put(self.skill_instance())


class RecurveBow(OnHitTrigger):
    # https://leagueoflegends.fandom.com/wiki/Recurve_Bow
    def __init__(self, name: str = 'RecurveBow', **kwargs):
        super(RecurveBow, self).__init__(labels=['offensive'], skill_instance=skills.RecurveBow, name=name, **kwargs)


class Tabi(LabelTrigger):
    # not working on bonus phys damage.
    # https://leagueoflegends.fandom.com/wiki/Plated_Steelcaps
    def __init__(self, name: str = 'Tabi', **kwargs):
        super(Tabi, self).__init__(labels=['defensive'], trigger_on='basic_attack', name=f'{name}', **kwargs)

    def use(self, game_state: 'GameState', node: 'SkillNode', **kwargs):
        # change the way of calculating value. It will be reset every update call to the default tool.
        node.tool = Compose(
            lambda val_dmg: val_dmg * 0.88,
            (
                node.tool,
            )
        )


class Illumination(OnHitTrigger):
    # https://leagueoflegends.fandom.com/wiki/Lux/LoL
    def __init__(self, name: str = 'Illumination', **kwargs):
        super(Illumination, self).__init__(skill_instance=skills.IlluminationNode, labels=['offensive'],
                                           trigger_on='illumination', name=name, **kwargs)


class ResistDamage(LabelTrigger):
    def __init__(self, trigger_on: str, name: str = 'ResistDamage', **kwargs):
        if trigger_on == 'magic':
            resist = skills.variables.EffectiveMagicResist()
        elif trigger_on == 'physical':
            resist = skills.variables.EffectiveArmor()
        else:
            resist = Lambda(lambda *_, **__: 0)
        self.resist = resist
        self.tool = skills.variables.PostMitigationDamage(resist)
        super(ResistDamage, self).__init__(labels=['defensive'], trigger_on=trigger_on, name=f'{name}_{trigger_on}',
                                           **kwargs)

    def use(self, game_state: 'GameState', node: 'SkillNode', **kwargs):
        node.tool = self.tool(node.tool)
