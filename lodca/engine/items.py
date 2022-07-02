from typing import Any, List

from epta.core import ToolDict
from epta.core.base_ops import Lambda
from epta.tools.base import ToolWrapper

from .items_utils import *


class Items(ToolDict):
    """
    The way to get items filled from database + ocr data.
    """
    def __init__(self, database: 'DataBase', name: str = 'Stats', **kwargs):
        self.ocr_item_getters = build_ocr_getters(database)

        tools = [*self.ocr_item_getters]
        super(Items, self).__init__(tools=tools, name=name, **kwargs)


class ItemsWrapper(ToolWrapper):
    tool: Items

    def __init__(self, stats: 'Stats', **kwargs):
        super(ItemsWrapper, self).__init__(stats, **kwargs)

    def use(self, data: dict, **kwargs):
        # get data from ocr:
        self.use_on_ocr(data, **kwargs)

    def _single_use(self, data: Any, tool_: 'BaseTool', **kwargs):
        new_item = tool_(data, **kwargs)
        # print(tool_.name, [item.data if not isinstance(item, dict) and not isinstance(item, str) and item else item for item in list(new_item.values())])
        if new_item:
            self._tools.update(new_item)

    def _multi_use(self, data: Any, tools: List['BaseTool'], **kwargs):
        if tools is None:
            tools = list()
        for tool_ in tools:
            self._single_use(data, self.tool[tool_.name], **kwargs)

    def use_on_ocr(self, ocr_data: dict, **kwargs):
        self._multi_use(ocr_data, self.tool.ocr_item_getters, **kwargs)
