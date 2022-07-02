from dataclasses import dataclass
from epta.core import Settings


@dataclass
class GameSettings(Settings):
    scale: float = 1.0
    minimap_on_left: bool = True
    screen_w: int = 1920
    screen_h: int = 1080
    champion: str = None


@dataclass
class ItemTemplateSettings(Settings):
    images_root_path: str = '../tests/temp/templates/item/'
    masks_root_path: str = None
    method: str = 'cv.TM_CCOEFF_NORMED'  # 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF_NORMED'
    threshold: float = 0.60
    # root_image_path: str = '../templates/images'


@dataclass
class TargetChampionTemplateSettings(Settings):
    images_root_path: str = '../tests/temp/templates/champion/'
    masks_root_path: str = '../tests/temp/templates/champion_masks/'
    method: str = 'cv.TM_CCOEFF_NORMED'  # 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF_NORMED'
    threshold: float = 0.60
    # root_image_path: str = '../templates/images'


@dataclass
class TesserocrSettings(Settings):
    # https://github.com/sirfz/tesserocr/blob/master/tesserocr.pyx
    psm: str = 'SINGLE_LINE'  # 'RAW_LINE'
    whitelist: str = '1234567890|\/.%'
    relative_path: str = "../tests/temp/tessexe/"


@dataclass
class AppSettings(Settings):
    remember_last_target: bool = True
    always_update_base_stats: bool = True
    launch_only_when_active_key_pressed: bool = False

    # image_hooker: str = 'imread'
    image_hooker: str = 'mss'


@dataclass
class KeyboardHookerSettings(Settings):
    combo_state_key: str = 'NUM_3'
    render_state_key: str = 'NUM_2'
    working_state_key: str = 'NUM_1'
    exit_state_key: str = 'NUM_0'
    active_state_key: str = 'c'  # launches additional player names recognition


@dataclass
class ScreenHookerSettings(Settings):
    window_name: str = 'League of Legends (TM) Client'
    x: int = 0
    y: int = 0
    w: int = 1920
    h: int = 1080


@dataclass
class DatabaseSettings(Settings):
    base_stats_path: str = '../tests/temp/database/champion.json'
    items_path: str = '../tests/temp/database/item.json'
