from tesserocr import PyTessBaseAPI, PSM
import os
import logging
import re

from epta.core import ConfigDependent, ToolDict
import epta.core.base_ops as ecb
from epta.tools.recognition import BaseRecogniser

from .utils import *

import epta


def get_cv_image(image, color='BGR'):
    # https://github.com/sirfz/tesserocr/issues/198
    """ Sets an OpenCV-style image for recognition.

    'image' is a numpy ndarray in color, grayscale, or binary (boolean)
        format.
    'color' is a string representing the current color of the image,
        for conversion using OpenCV into an RGB array image. By default
        color images in OpenCV use BGR, but any valid channel
        specification can be used (e.g. 'BGRA', 'XYZ', 'YCrCb', 'HSV', 'HLS',
        'Lab', 'Luv', 'BayerBG', 'BayerGB', 'BayerRG', 'BayerGR').
        Conversion only occurs if the third dimension of the array is
        not 1, else 'color' is ignored.

    """
    bytes_per_pixel = image.shape[2] if len(image.shape) == 3 else 1
    height, width = image.shape[:2]
    bytes_per_line = bytes_per_pixel * width

    if bytes_per_pixel != 1 and color != 'RGB':
        # non-RGB color image -> convert to RGB
        image = cv.cvtColor(image, getattr(cv, f'COLOR_{color}2RGB'))
    elif bytes_per_pixel == 1 and image.dtype == bool:
        # binary image -> convert to bitstream
        image = np.packbits(image, axis=1)
        bytes_per_line = image.shape[1]
        width = bytes_per_line * 8
        bytes_per_pixel = 0
    # else image already RGB or grayscale
    return image.tobytes(), width, height, bytes_per_pixel, bytes_per_line


class TesserocrRecognition(BaseRecogniser, ConfigDependent):
    def __init__(self, config: 'Config', name: str = 'tesserocr_rec', **kwargs):
        super(TesserocrRecognition, self).__init__(config=config, name=name, **kwargs)
        tess_path = os.path.join(os.getcwd(), self.config.settings.relative_path, 'tessdata')
        logging.info(f'Setting tesseract path to: {tess_path}')
        self.api = PyTessBaseAPI(path=tess_path,
                                 psm=getattr(PSM, self.config.settings.psm))
        self.api.SetVariable("tessedit_char_whitelist", self.config.settings.whitelist)
        # self.images = 0

    def end_api(self):
        self.api.End()

    def image_to_data(self, image: np.ndarray, *args, name: str = None, **kwargs) -> str:
        preprocess = self.config.prepr_mapping.get(name, None)
        if preprocess:
            image = preprocess(image)
        # epta.utils.utils._save_crops({self.images: image}, './temp/prepr/', prefix=f'{self.name}')
        # self.images += 1
        self.api.SetImageBytes(*get_cv_image(image, color='RGB'))
        self.api.Recognize()
        result = self.api.GetUTF8Text()
        # confidence:
        """
        if result:
            ri = self.api.GetIterator()
            level = tesserocr.RIL.SYMBOL
            for r in tesserocr.iterate_level(ri, level):
                symbol = r.GetUTF8Text(level)  # r == ri
                conf = r.Confidence(level)
                print(symbol, conf)
        """
        return result

    def use_on_1d_dict(self, data: dict, name: str = None, **kwargs):
        ret = dict()
        for key, value in data.items():
            res = self.image_to_data(value, name=(name if name else key), **kwargs)
            ret[key] = res
        return ret

    def use_on_2d_dict(self, data: dict, name: str = None, **kwargs):
        ret = dict()
        for key, value in data.items():
            res = self.use_on_1d_dict(value, name=(name if name else key), **kwargs)
            ret[key] = res
        # print(ret)
        return ret


class TessTool(ecb.Variable):
    def __init__(self, cfg: 'Config', name='TessTool', **kwargs):
        tess_rec = TesserocrRecognition(cfg)
        super(TessTool, self).__init__(name=name, tool=tess_rec, **kwargs)

    def use(self, data: dict, names: list = None, **kwargs):
        # converts 2d dict of images to 1d dict of strings with key selecting possibility
        if names is None:
            names = list()
        inp = {key: data[key] for key in names if key in data} if names else data
        data_2d = self.tool.use_on_2d_dict(inp)
        data_1d = {key: value for values in data_2d.values() for key, value in values.items()}
        return data_1d


class ToNumeric(ToolDict):
    def __init__(self, *args, **kwargs):
        super(ToNumeric, self).__init__(*args, **kwargs)
        # paired stats means two values to unpack.
        self.pair_stats = {'armor_pen', 'magic_pen', 'health_bar', 'mana_bar', 'vamp'}
        self.float_stats = {'attack_speed'}

    @staticmethod
    def find_all(st: str, rgx: str):
        return re.findall(rgx, st.replace(' ', ''))

    @staticmethod
    def to_float(inp: str):
        return float(inp)

    @staticmethod
    def to_int(inp: str) -> int:
        inp = re.sub(r'\D', '', inp)
        return int(inp)

    def use(self, data: dict, names: list = None, **kwargs):
        if names is None:
            names = list()
        inp = {key: data[key] for key in names if key in data} if names else data
        result = dict()
        for key, value in inp.items():
            res = self.find_all(value, r'(?:\d?\d\.?)?\d+')
            if key in self.pair_stats:
                if len(res) > 1:
                    result[f'{key}_0'] = self.to_int(res[0])
                    result[f'{key}_1'] = self.to_int(res[1])
            else:
                if res:
                    if key in self.float_stats:
                        result[key] = self.to_float(res[0])
                    else:
                        result[key] = self.to_int(res[0])
        return result
