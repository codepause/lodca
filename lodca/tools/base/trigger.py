from typing import Union

from epta.core import BaseTool


class Trigger(BaseTool):
    """
    Checks if tool is usable under certain conditions.
    """

    def __init__(self, name: str = 'Trigger', labels: list = None, **kwargs):
        labels = labels if labels else list()
        self.labels = set(labels)
        super(Trigger, self).__init__(name=name, **kwargs)

    def is_usable(self, game_state: 'GameState', node: 'SkillNode', **kwargs) -> bool:
        return False

    def use(self, game_state: 'GameState', node: 'SkillNode', **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        if self.is_usable(*args, **kwargs):
            return self.use(*args, **kwargs)


class Triggers:
    """
    Storage of triggers.

    Args:
        unique (dict, list): unique triggers.
        basic (list): not unique triggers.
    """

    def __init__(self, unique: Union[dict, list] = None, basic: list = None, name: str = 'Triggers', **kwargs):
        unique = dict() if unique is None else unique
        basic = list() if basic is None else basic

        if not isinstance(unique, dict):
            unique = {trigger.name: trigger for trigger in unique}

        self.name = name
        self.unique = dict()
        self.basic = list()
        self.trigger_order = dict()

        for key, value in unique.items():
            self.add_unique(value)
        for value in basic:
            self.add_basic(value)

    def reset(self):
        self.unique = dict()
        self.basic = list()
        self.trigger_order = dict()

    def add_unique(self, trigger: Trigger):
        if trigger.name not in self.unique:
            self.trigger_order[id(trigger)] = len(self.trigger_order)
            self.unique[trigger.name] = trigger

    def add_basic(self, trigger: Trigger):
        self.trigger_order[id(trigger)] = len(self.trigger_order)
        self.basic.append(trigger)

    def get_all(self) -> list:
        return self.basic + list(self.unique.values())

    def get(self, typed: str = None, label: str = None) -> list:
        triggers = list()
        if typed != 'basic':
            if label:
                triggers.extend([trigger for trigger in self.unique.values() if label in trigger.labels])
            else:
                triggers.extend(list(self.unique.values()))
        if typed != 'unique':
            if label:
                triggers.extend([trigger for trigger in self.basic if label in trigger.labels])
            else:
                triggers.extend(self.basic)
        return triggers

    def _update_names_and_order(self, triggers: 'Triggers'):
        self.trigger_order.update({key: len(self.trigger_order) + idx for key, idx in triggers.trigger_order.items()})

    def merge_all(self, triggers: 'Triggers'):
        """
        Merge current triggers with some additional ones.

        Args:
            triggers  (Trigger): to merge with.
        """
        self.unique.update(triggers.unique)
        self.basic += triggers.basic
        self._update_names_and_order(triggers)

    def merge(self, triggers: 'Triggers', typed: str = None, label: str = None):
        if typed != 'unique':
            self.basic += triggers.get('basic', label)
            self._update_names_and_order(triggers)
        if typed != 'basic':
            self.unique.update({trigger.name: trigger for trigger in triggers.get('unique', label)})
            self._update_names_and_order(triggers)

    def update(self, *args, **kwargs):
        # detach composition tools. (Reset to default). UNUSED RN.
        for trigger in self.unique.values():
            trigger.update()
        for trigger in self.basic:
            trigger.update()
