from typing import Union, List

from functools import partial
from queue import Queue, LifoQueue, PriorityQueue
from collections import deque
import copy
import time

from epta.core import BaseTool
from epta.core.base_ops import Variable, Concatenate

from lodca.tools.base.trigger import Triggers


class SkillNode(Variable):
    """
    Simple skill is just labels and a tool.

    Args:
        tool (BaseTool): Used to get value of a skill or/and **modify** game state.

    Keyword Args:
        labels (list, set): Short skill description. Some labels may be triggered on.
        name (str): Node name.
    """

    def __init__(self, tool: BaseTool, labels: Union[list, set] = None, name: str = 'Node', **kwargs):
        labels = labels if labels else list()
        self.labels = set(labels)

        self.game_state_snapshot: dict = dict()
        self.value = None
        self.triggers = Triggers()

        super(SkillNode, self).__init__(tool=tool, name=name, **kwargs)
        self._default_tool = tool

    def snapshot_state(self, game_state: 'GameState'):
        self.game_state_snapshot = game_state  # ()

    def use(self, *args, **kwargs) -> 'SkillNode':
        self.value = self.tool(self.game_state_snapshot)
        return self

    def update(self, *args, **kwargs):
        """
        Reset current tool changed by triggers while calculating.
        """
        # print(self._default_tool, self._default_tool.name)
        # print('update', self.name, self.tool, self.tool.name)
        self.tool = self._default_tool

    def __copy__(self) -> 'SkillNode':
        return SkillNode(self._default_tool, self.labels, self.name)

    def __repr__(self) -> str:
        s = f'{self.__class__.__name__}(name={self.name}, value={self.value})'
        return s


class Deq(deque):
    def __init__(self, *args, **kwargs):
        super(Deq, self).__init__(*args, **kwargs)

    def empty(self):
        return len(self) == 0

    def put(self, item):
        self.append(item)

    def get(self):
        return self.pop()


class Skill(Concatenate):
    """
    Skill contains of multiple :class:`~lodca.engine.skill.SkillNodes` or  :class:`~lodca.engine.skill.Skill`.

    Keyword Args:
        use_condition (callable): Function, that returns True or False if node is usable or not.
    """

    def __init__(self, *args, name: str = 'Skill', use_condition: callable = None, **kwargs):
        super(Skill, self).__init__(*args, name=name, **kwargs)
        self.node_queue = LifoQueue()
        # self.node_queue = Deq()

        self.triggers_to_use = list()

        self.use_condition = use_condition if use_condition is not None else lambda *_, **__: True

        self.value = None
        self.game_state = None

    def snapshot_state(self, game_state: 'GameState'):
        """
        Add game state link for self.

        Args:
            game_state (GameState): game state to get data from.

        Returns:

        """
        self.game_state = game_state

    def use(self, game_state: 'GameState' = None, **kwargs) -> List['SkillNode']:
        """
        Every use nodes are being reset to default triggers with ``node.update()`` and being put into the skills queue.
        Each node gets **pseudo** unique **snapshot** of the ``game state`` as the inputs.
        Each skill gets actual game state and can modify it.

        Returns:
            result (list): Result of the current Skill
        """

        game_state = game_state or self.game_state
        if not self.is_usable(game_state):
            return list()

        for node in self.tools[::-1]:
            node.update()
            self.node_queue.put(node)

        result = list()
        initial_health = game_state.target_unit.stats.get('current_health', 0)
        # print(self.name)
        # print(self.game_state.triggers.get_all())
        while not self.node_queue.empty():
            # print(self.node_queue)
            node = self.node_queue.get()
            # print('    ', node)
            if isinstance(node, Skill):
                node.snapshot_state(game_state)
                node()
                result.append(node)
            elif isinstance(node, SkillNode):
                node.snapshot_state(game_state)

                for trigger in game_state.triggers.get_all():
                    # print('        ', trigger)
                    trigger(game_state, node, skill=self)

                value = node()
                result.append(value)
            else:
                node(game_state)

        self.value = sum([temp_node.value for temp_node in result if temp_node.value])
        stats = game_state.target_unit.stats
        stats['current_health'] = max(0, initial_health - self.value)
        game_state.target_unit.stats.use_on_fill()

        return result

    def update(self, *args, **kwargs):
        for node in self.tools:
            node.update()
        self.triggers_to_use = list()

    def is_usable(self, game_state: 'GameState') -> bool:
        return self.use_condition(game_state)

    def __deepcopy__(self, memodict={}) -> 'Skill':
        new_tools = list()
        for tool in self.tools:
            if isinstance(tool, SkillNode):
                new_tools.append(copy.copy(tool))
            elif isinstance(tool, Skill):
                new_tools.append(copy.deepcopy(tool))
            else:
                new_tools.append(tool)
        cls = Skill(new_tools, name=self.name, use_condition=self.use_condition)
        cls.snapshot_state(self.game_state)
        # cls.triggers_to_use = cls.triggers_to_use
        return cls

    def __repr__(self) -> str:
        s = f'{self.__class__.__name__}(['
        for node in self.tools:
            s += f'{node}, '
        s += '])'
        return s
