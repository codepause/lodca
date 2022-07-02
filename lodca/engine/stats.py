from typing import Any, List

from epta.core import ToolDict
from epta.tools.base import ToolWrapper

from .stats_utils import *


class Stats(ToolDict):
    """
    Way of gathering values from previous steps.
    """

    def __init__(self, base_stats_getters: list, name: str = 'Stats', **kwargs):
        self.ocr_stat_getters = build_ocr_getters()
        self.missing_stats_getters = build_missing_getters()
        self.base_stats_getters = base_stats_getters

        tools = [*self.ocr_stat_getters, *self.missing_stats_getters, *self.base_stats_getters]
        super(Stats, self).__init__(tools=tools, name=name, **kwargs)


# TODO: init with default stat names to exclude soft atomics default value when __getitem__
class StatsWrapper(ToolWrapper):
    tool: Stats

    def __init__(self, stats: 'Stats', **kwargs):
        super(StatsWrapper, self).__init__(stats, **kwargs)

    def use(self, data: dict, **kwargs):
        self.use_on_ocr(data, **kwargs)
        self.use_on_base(**kwargs)
        self.use_on_fill(**kwargs)

    def _single_use(self, data: Any, tool_: 'BaseTool', **kwargs):
        new_stat = tool_(data, **kwargs)
        # print(tool_.name, new_stat)
        if new_stat:
            self._tools.update(new_stat)

    def _multi_use(self, data: Any, tools: List['BaseTool'], **kwargs):
        if tools is None:
            tools = list()
        for tool_ in tools:
            self._single_use(data, self.tool[tool_.name], **kwargs)

    def use_on_ocr(self, ocr_data: dict, **kwargs):
        """
        Fill stats from the ocr data.
        """
        self._multi_use(ocr_data, self.tool.ocr_stat_getters, **kwargs)

    def use_on_base(self, **kwargs):
        """
        Fill stats from the database
        """
        self._multi_use(self, self.tool.base_stats_getters, **kwargs)

    def use_on_fill(self, **kwargs):
        """
        Fill remaining values like **missing* and **perc**.
        """
        self._multi_use(self, self.tool.missing_stats_getters, **kwargs)

    def __repr__(self):
        s = f'{self.__class__.__name__}([\n'
        for key, value in self.items():
            s += f'\t{key}={value},\n'
        s += '])'
