from typing import Union

from epta.core import BaseTool
import epta.core.base_ops as ecb
from .skill import Skill, SkillNode

class AddTrigger(ecb.Variable):
    """
    Add trigger to the **end** of `current_triggers`.
    """

    def __init__(self, trigger_instance: 'Trigger', is_unique: bool = True, name: str = 'add_trigger', **kwargs):
        self._trigger_instance = trigger_instance
        self.is_unique = is_unique

        if self.is_unique:
            tool_ = ecb.Lambda(lambda gs_snap, **k: gs_snap['triggers'].add_unique(self._trigger_instance()))
        else:
            tool_ = ecb.Lambda(lambda gs_snap, **k: gs_snap['triggers'].add_basic(self._trigger_instance()))

        super(AddTrigger, self).__init__(tool=tool_, name=name, **kwargs)


class RemoveTrigger(ecb.Variable):
    def __init__(self, remove_name: str, is_unique: bool = True, name: str = 'remove_trigger', **kwargs):
        self.remove_name = remove_name
        self.is_unique = is_unique

        def remove_unique(gs_snap: dict, **k):
            triggers = gs_snap['triggers'].unique
            if self.remove_name in triggers:
                del triggers[self.remove_name]

        def remove_basic(gs_snap: dict, **k):
            triggers = gs_snap['triggers'].basic
            remove_idx = [idx for idx, trigger in enumerate(triggers) if trigger.name == self.remove_name]
            for idx in remove_idx[::-1]:
                del triggers[idx]

        if self.is_unique:
            tool_ = ecb.Lambda(remove_unique)
        else:
            tool_ = ecb.Lambda(remove_basic)

        super(RemoveTrigger, self).__init__(tool=tool_, name=name, **kwargs)


class ActivateLabelsTriggers(SkillNode):
    def __init__(self, labels: Union[list, set], name: str = 'activate_labels_triggers', **kwargs):
        tool_ = ecb.Lambda(lambda *_, **__: 0)

        super(ActivateLabelsTriggers, self).__init__(tool=tool_, labels=labels, name=name, **kwargs)


class ActivateUniqueTrigger(SkillNode):
    def __init__(self, trigger_name: str, name: str = 'activate_label_trigger', **kwargs):
        tool_ = ecb.Lambda(lambda *_, **__: 0)
        self.trigger_name = trigger_name
        super(ActivateUniqueTrigger, self).__init__(tool=tool_, name=name, **kwargs)

    def use(self, *args, **kwargs) -> 'SkillNode':
        print(self.trigger_name)
        if self.trigger_name in self.game_state_snapshot['triggers'].unique:
            trigger = self.game_state_snapshot['triggers'].unique[self.trigger_name]
            trigger(self.game_state_snapshot, self, **kwargs)
        return self

