from functools import partial

import epta
from epta.core import BaseTool, ToolDict, ConfigDependent

from lodca.tools.base import BuilderCache, DatabaseCache
from .builders import *


class Layout(ToolDict):
    """
    Storage for tools.
    Use ``.build()`` after init to assign tools.
    """

    def __init__(self, *args, name: str = 'Layout', **kwargs):
        super(Layout, self).__init__(*args, name=name, **kwargs)

    def build(self, builder: callable, *args, **kwargs):
        for key, value in builder(*args, **kwargs).items():
            self[key] = value
        self.update()

    @staticmethod
    def use_on_hooked(data: dict, **kwargs):
        # use on data: dict = {'image': image, ...}
        return data

    @staticmethod
    def prepare_output(data: dict, **kwargs):
        # prepare data from tools for the output: convert stats etc.
        return data


class TargetLayout(Layout):
    """
    Default target layouts.

    Keyword Args:
        default_tools_kwargs (dict): ``kwargs`` to pass to the tools and manage tools usage (on/off also).
    """

    def __init__(self, *args, default_tools_kwargs: dict = None, **kwargs):
        super(TargetLayout, self).__init__(*args, **kwargs)
        if default_tools_kwargs is None:
            default_tools_kwargs = {
                'tess': {
                    'names': [
                        'stats', 'health_bar', 'mana_bar',
                        'champion_level',
                        'current_health', 'total_health',
                        'current_mana', 'total_mana',
                    ]
                },
                'item': {}
            }
        self.default_tools_kwargs = default_tools_kwargs

    def use(self, *args, **kwargs):
        image = self['image_hooker'](*args, **kwargs)
        if image is not None:
            return self.use_on_hooked({'image': image}, **kwargs)

    def crop_hooked(self, data: dict, **kwargs):
        image = data['image']
        crops = self['cropper'](image)
        return crops

    def use_on_hooked(self, data: dict, tools_kwargs: dict = None, **kwargs):
        if tools_kwargs is None:
            tools_kwargs = self.default_tools_kwargs

        crops = self.crop_hooked(data, **kwargs)
        result = dict()
        for tool_name in self.default_tools_kwargs:
            # launch by default if not {tool_name: None}
            if (kwgs := tools_kwargs.get(tool_name, {})) is not None:
                updated_kwargs = {**self.default_tools_kwargs[tool_name], **kwgs}
                local_result = self['image_rec'][tool_name](crops, **updated_kwargs)
                result.update(local_result)
        return {**result, 'champion_name': data['champion_name']}


class PlayerLayout(TargetLayout):
    # default player layout
    def __init__(self, *args, **kwargs):
        default_tools_kwargs = {
            'tess': {
                'names': [
                    'stats', 'additional_stats',
                    'rune_stats', 'health_bar', 'mana_bar',
                    'champion_level',
                    'current_health', 'total_health',
                    'current_mana', 'total_mana',
                ]
            },
            'item': {},
            'skill_level': {}
        }
        super(PlayerLayout, self).__init__(*args, default_tools_kwargs=default_tools_kwargs, **kwargs)


def wrap_default_builder(cls, builder: callable) -> callable:
    """
    Wrap init and build to the single function
    Args:
        cls: Layout class instance.
        builder: function to build layout with.

    Returns:
        callable
    """

    def build(*args, **kwargs):
        # build from instance
        obj = cls()
        obj.build(builder, *args, **kwargs)
        return obj

    return build


class LayoutManager(DatabaseCache, ConfigDependent):
    """
    Cache already built layouts for different champions.

    Args:
        config (AppConfig): app config to get settings from

    Keyword Args:
        target (bool): if to build for target (different layout settings).
        default_builder (callable): custom default layout builder.
    """

    def __init__(self, config: 'AppConfig', target: bool = False, default_builder: callable = None, **kwargs):
        # TODO: for each champion do not spawn TessRec object.
        if target:
            builder = partial(target_builder, config=config)
            cls = partial(TargetLayout, name='TargetLayout')
        else:
            builder = partial(player_builder, config=config)
            cls = partial(PlayerLayout, name='PlayerLayout')

        if default_builder is None:
            default_builder = wrap_default_builder(cls, builder)
        self._default_builder = default_builder

        default_layout = default_builder()
        super(LayoutManager, self).__init__(database=dict(), builder=partial(self._wrap_builder),
                                            tools={'default': default_layout},
                                            config=config, **kwargs)

    def _wrap_builder(self, database_builder: callable) -> callable:
        def builder(layout_name: str) -> Layout:
            # build from database
            # database_builder == self.database.get

            # if layout is not unique (kled etc)
            if layout_name in self.database:
                layout_builder = self.database[layout_name]
                layout = layout_builder()
            else:
                layout = self['default']
            return layout

        return builder

    def select_layout(self, *args, **kwargs) -> dict:
        """
        Use default layout to detect the champion and then pass data to its own layout if needed.
        Store image not to hook screen 2 times.
        """
        default_layout = self['default']
        image = default_layout['image_hooker'](*args, **kwargs)
        crops = default_layout['cropper'](image)
        # 2d dict:
        # 1st is a name for a tool. 2nd is a name for the output of a tool
        layout = None
        champion_name = None
        if default_layout['image_rec']['indicator'](crops):
            # Something detected, but no such a champion: creep or scuttle etc.
            champion_name = default_layout['image_rec']['champion'](crops) or 'default'
            # this layout is automatically cached
            layout = self[champion_name]

        # return image as not to hook 2 times
        return {'layout': layout, 'image': image, 'champion_name': champion_name}

    def use(self, *args, **kwargs):
        data = self.select_layout(*args, **kwargs)
        result = None
        if layout := data['layout']:
            local_result = layout.use_on_hooked(data, **kwargs)
            result = layout.prepare_output(local_result)

        return result
