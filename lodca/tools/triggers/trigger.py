from epta.core.base_ops import Concatenate

from lodca.tools.base import Trigger
from lodca.engine.skill import Skill, SkillNode


class LabelTrigger(Trigger):
    """
    Simple trigger to use on label name.
    """

    def __init__(self, trigger_on: str, name: str = 'Trigger', **kwargs):
        self.trigger_on = trigger_on
        super(LabelTrigger, self).__init__(name=name, **kwargs)

    def is_usable(self, game_state: 'GameState', node: 'SkillNode', **kwargs) -> bool:
        if self.trigger_on in node.labels:
            return True
        return False


class OnHitTrigger(LabelTrigger):
    """
    Add ``skill_instance()`` to the skills queue if **onhit** label.
    """

    def __init__(self, skill_instance: type, name: str = 'OnHitTrigger', trigger_on: str = 'onhit', **kwargs):
        super(OnHitTrigger, self).__init__(name=name, trigger_on=trigger_on, **kwargs)
        self.skill_instance = skill_instance

    def use(self, game_state: 'GameState', node: 'SkillNode', skill: 'Skill' = None, **kwargs):
        """
        new_skill = self.skill_instance()
        new_skill.snapshot_state(game_state)
        new_skill()
        return new_skill
        """
        skill.node_queue.put(self.skill_instance())
