from typing import Dict, Any

import epta.core as ec

from lodca.database.triggers import ResistDamage
from lodca.tools.base import Triggers

from .unit import Unit


class GameState(ec.BaseTool):
    """
    Current game state that acts like global state the values for calculations are to get from.
    """
    def __init__(self, name: str = 'GameState', **kwargs):
        super(GameState, self).__init__(name=name, **kwargs)

        self.player_unit = Unit(name='PlayerUnit')
        self.target_unit = Unit(name='TargetUnit')

        self._default_triggers = Triggers([ResistDamage('magic'), ResistDamage('physical')])

        self.triggers = Triggers()

    def gather_triggers(self, **kwargs):
        """
        Gather triggers for the current calculation tick.

        Returns:
            None
        """
        # filter targets and players inventories:
        self.player_unit.gather_triggers()
        self.target_unit.gather_triggers()
        self.triggers.merge(self.player_unit.current_triggers, label='offensive')
        self.triggers.merge(self.target_unit.current_triggers, label='defensive')

        self.triggers.merge(self._default_triggers)

        return self.triggers

    def snapshot(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Snapshot current state:
            Triggers are stored as the list.
            Unit stats are stored as a copy of **current game state unit stats**.
            All the other things are the **pointers** to classes.

        Returns:
            Snapshotted dictionary.
        """
        return {
            'player_unit': self.player_unit(),
            'target_unit': self.target_unit(),
            'triggers': self.triggers
        }

    def use(self, *args, **kwargs):
        # do i need to update on every skill snapshot?
        # self.update(*args, **kwargs)
        return self.snapshot(*args, **kwargs)

    def reset_triggers(self):
        self.triggers.reset()
        self.player_unit.reset_triggers()
        self.target_unit.reset_triggers()

    def update(self, *args, **kwargs):
        self.reset_triggers()
        self.gather_triggers(**kwargs)

    def __getitem__(self, item):
        # TODO: change to ToolDict?
        return self.__dict__[item]
