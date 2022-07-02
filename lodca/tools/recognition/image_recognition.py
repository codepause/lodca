from epta.core import *
import epta.core.base_ops as ecb

from lodca.tools.base import Atomic2DTool
from .tesserocr_rec import TessTool, ToNumeric
from .skill_level_rec import SkillLevelRecognition
from .easy_target_indicator import EasyTargetIndicator, AlwaysActiveIndicator
from .template_rec import TemplateRecognition, TemplateChampionRecognition
from .champion_rec import EasyChampionRecognition, ConfigChampionRecognition


class ImageRecognition(ToolDict, ConfigDependent):
    def __init__(self, cfg: 'AppConfig', position_manager: 'ToolDict', **kwargs):
        tools = {
            'tess': ecb.Compose(
                lambda tess, to_num, args, kwgs: to_num(tess(*args, **kwgs)),
                (
                    ecb.Wrapper(TessTool(cfg.tess_config)),
                    ecb.Wrapper(ToNumeric()),
                    # as Sequential does not pass kwargs to the tools, pass it manually
                    ecb.Lambda(lambda *args, **kwgs: args),
                    ecb.Lambda(lambda *args, **kwgs: kwgs)
                ),
            ),
            'item': Atomic2DTool(tool=TemplateRecognition(
                position_manager['relative_manager'],
                config=cfg.item_template_config,
                key='item'),
                key='inventory'
            ),
            'skill_level': Atomic2DTool(tool=SkillLevelRecognition(), key='skill_points'),
            # 'target_indicator': Atomic2DTool(tool=EasyTargetIndicator(), key='indicator'),
            'indicator': ecb.Sequential([
                ecb.SoftAtomic(key='indicator', default_value=dict),
                ecb.SoftAtomic(key='indicator'),
                AlwaysActiveIndicator()
            ]),
            'champion': ecb.Sequential([
                ecb.SoftAtomic(key='champion', default_value=dict),
                ecb.SoftAtomic(key='champion'),
                ConfigChampionRecognition(config=cfg.game_config),
                ecb.SoftAtomic(key='name', default_value='default')
            ])
        }

        super(ImageRecognition, self).__init__(config=cfg, tools=tools, **kwargs)


class ImageRecognitionTarget(ToolDict, ConfigDependent):
    def __init__(self, cfg: 'AppConfig', position_manager: 'ToolDict', **kwargs):
        tools = {
            'tess': ecb.Compose(
                lambda tess, to_num, args, kwgs: to_num(tess(*args, **kwgs)),
                (
                    ecb.Wrapper(TessTool(cfg.tess_target_config)),
                    ecb.Wrapper(ToNumeric()),
                    ecb.Lambda(lambda *args, **kwgs: args),
                    ecb.Lambda(lambda *args, **kwgs: kwgs)
                ),
            ),
            'item': Atomic2DTool(tool=TemplateRecognition(
                position_manager['relative_manager'],
                config=cfg.item_template_config,
                key='item'),
                key='inventory'
            ),

            'indicator': ecb.Sequential([
                # Because crops are stored as 2d dict. May fix this
                ecb.SoftAtomic(key='indicator', default_value=dict),
                ecb.SoftAtomic(key='indicator'),
                EasyTargetIndicator()
            ]),
            'champion': ecb.Sequential([
                ecb.SoftAtomic(key='champion', default_value=dict),
                ecb.SoftAtomic(key='champion'),
                TemplateChampionRecognition(position_manager['relative_manager'],
                                            config=cfg.target_champion_template_config,
                                            key='champion'),
                ecb.Lambda(lambda template_res: template_res.get('name', 'default') if template_res else None)
            ])
        }

        super(ImageRecognitionTarget, self).__init__(config=cfg, tools=tools, **kwargs)
