from functools import partial

from epta.core import Config, Settings

from .app_settings import *
from lodca.tools.recognition.utils import resize_thr


class TesserocrConfig(Config):
    def __init__(self):
        self.prepr_mapping = dict(
            stats=partial(resize_thr, thr=85, resc=2.5, pad=True),
            additional_stats=partial(resize_thr, thr=80, resc=3, pad=True, to_gray=True, save_values=35),
            rune_stats=partial(resize_thr, thr=120),
            champion_level=partial(resize_thr, thr=80, resc=3, save_values=35),
            health_bar=partial(resize_thr, thr=160, pad=True, resc=2, cut=0, to_gray=False),
            mana_bar=partial(resize_thr, thr=160, pad=True, resc=2, cut=0, to_gray=False),
            current_health=partial(resize_thr, thr=120, pad=False, resc=2.3, cut=0, to_gray=True, same_values=35),
            total_health=partial(resize_thr, thr=120, pad=False, resc=2.3, cut=0, to_gray=True, same_values=35),
            current_mana=partial(resize_thr, thr=120, pad=False, resc=2.3, cut=0, to_gray=True, same_values=35),
            total_mana=partial(resize_thr, thr=120, pad=False, resc=2.3, cut=0, to_gray=True, same_values=35),
        )
        super(TesserocrConfig, self).__init__(settings=TesserocrSettings())


class TesserocrTargetConfig(Config):
    def __init__(self):
        self.prepr_mapping = dict(
            stats=partial(resize_thr, thr=100, resc=3.0, pad=True, to_gray=True),
            champion_level=partial(resize_thr, thr=80, resc=1.5, pad=True, same_values=True),
            health_bar=partial(resize_thr, thr=160, pad=True, resc=2, cut=0, to_gray=False),
            mana_bar=partial(resize_thr, thr=160, pad=True, resc=2, cut=0, to_gray=False),
            current_health=partial(resize_thr, thr=80, pad=True, resc=4, cut=0, to_gray=True, same_values=30),
            total_health=partial(resize_thr, thr=80, pad=True, resc=4, cut=0, to_gray=True, same_values=30),
            current_mana=partial(resize_thr, thr=100, pad=True, resc=4, cut=0, to_gray=True, same_values=35),
            total_mana=partial(resize_thr, thr=100, pad=True, resc=4, cut=0, to_gray=True, same_values=35),
        )
        super(TesserocrTargetConfig, self).__init__(settings=TesserocrSettings())


class ImageRecognitionConfig(Config):
    def __init__(self, **kwargs):
        self.tesseract_config = kwargs.get('tesseract_config', None) or TesserocrConfig()
        # self.template_config = kwargs.get('template_config', None) or TemplateConfig()
        self.fnc_mapping = dict(
            skill_points='skill_level_rec',
            # exclude target indicator data from processing
            # actually, in app this key is not requested (game.py; get_source_named_crops)
            target_indicator=None
        )
        super(ImageRecognitionConfig, self).__init__(settings=Settings())


class ItemTemplateConfig(Config):
    def __init__(self):
        super(ItemTemplateConfig, self).__init__(settings=ItemTemplateSettings())


class TargetChampionTemplateConfig(Config):
    def __init__(self):
        super(TargetChampionTemplateConfig, self).__init__(settings=TargetChampionTemplateSettings())


class GameConfig(Config):
    def __init__(self):
        super(GameConfig, self).__init__(settings=GameSettings())


class RenderConfig(Config):
    def __init__(self):
        super(RenderConfig, self).__init__(settings=Settings())


class KeyboardHookerConfig(Config):
    def __init__(self):
        super(KeyboardHookerConfig, self).__init__(settings=KeyboardHookerSettings())


class ScreenHookerConfig(Config):
    def __init__(self):
        super(ScreenHookerConfig, self).__init__(settings=ScreenHookerSettings())


class DatabaseConfig(Config):
    def __init__(self):
        super(DatabaseConfig, self).__init__(settings=DatabaseSettings())


class AppConfig(Config):
    def __init__(self, game_config: 'GameConfig' = None, **kwargs):
        self.game_config = game_config or GameConfig()
        self.item_template_config = ItemTemplateConfig()
        self.target_champion_template_config = TargetChampionTemplateConfig()
        self.tess_config = TesserocrConfig()
        self.tess_target_config = TesserocrTargetConfig()  # different tess settings

        self.ir_config = ImageRecognitionConfig(**kwargs)
        self.render_config = RenderConfig()
        self.kh_config = KeyboardHookerConfig()
        self.sh_config = ScreenHookerConfig()

        super(AppConfig, self).__init__(settings=AppSettings(), **kwargs)
