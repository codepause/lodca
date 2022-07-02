from typing import Union, Tuple
import numpy as np
import cv2 as cv
import os
from collections import defaultdict

from epta.core import BaseTool, ConfigDependent, PositionDependent


class TemplateRecognition(PositionDependent, ConfigDependent):
    def __init__(self, relative_manager: 'ToolDict', config: 'Config', **kwargs):
        super(TemplateRecognition, self).__init__(position_manager=relative_manager, config=config, **kwargs)

        self.raw_templates = dict()
        self.raw_masks = dict()

        self.current_templates = dict()
        self.current_masks = dict()

        self.method = None

    def make_single_position(self, key: str = None, *args, **kwargs) -> Tuple[int, int]:
        if key is None:
            key = self.key
        positions = self.position_manager.get(key)
        if positions is None:
            return tuple()
        w = int(positions.get('w', 10))
        h = int(positions.get('h', 10))
        return w, h

    @staticmethod
    def load_images(root_path: str) -> dict:
        templates = dict()
        if root_path and os.path.exists(root_path):
            for filename in os.listdir(root_path):
                image = cv.imread(os.path.join(root_path, filename))
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                template_name = filename.split('.')[0]
                templates[template_name] = image
        return templates

    @staticmethod
    def rescale_images(templates: dict, shape: tuple, **kwargs) -> dict:
        result = dict()
        for key, value in templates.items():
            value = cv.resize(value, shape, **kwargs)
            result[key] = value
        return result

    def update(self, *args, **kwargs):
        # rescale templates to match game scale
        self.inner_position = self.make_inner_position(*args, **kwargs)

        if not self.raw_templates:
            self.raw_templates = self.load_images(self.config.settings.images_root_path)
            self.raw_masks = self.load_images(self.config.settings.masks_root_path)
        self.current_templates = self.rescale_images(self.raw_templates, self.inner_position)
        self.current_masks = self.rescale_images(self.raw_masks, self.inner_position)

        self.method = eval(self.config.settings.method)

    def get_mask(self, name: str) -> Union[np.ndarray, None]:
        return self.current_masks.get(name, None)

    def find_template(self, image: np.ndarray, **kwargs):
        results = list()
        for name, template in self.current_templates.items():
            res = cv.matchTemplate(image, template, self.method, mask=self.get_mask(name))
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if self.method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                top_left, value = min_loc, min_val
                take = True if value < self.config.settings.threshold else False
            else:
                top_left, value = max_loc, max_val
                take = True if value > self.config.settings.threshold else False
            # print(top_left, value, name)
            if take:
                results.append({'name': name, 'top_left': top_left, 'value': value})

        results.sort(key=lambda data: data['value'], reverse=self.method not in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED])

        if results:
            result = results[0]
        else:
            result = None

        return result

    def use(self, image: np.ndarray, **kwargs):
        return self.find_template(image, **kwargs)

    def use_on_1d_dict(self, data: dict, names: list = None, **kwargs) -> dict:
        inp = {key: data[key] for key in names if key in data} if names else data
        ret = dict()
        for key, value in inp.items():
            res = self.use(value, **kwargs)
            ret[key] = res
        return ret

class TemplateChampionRecognition(TemplateRecognition):
    def __init__(self, *args, **kwargs):
        super(TemplateChampionRecognition, self).__init__(*args, **kwargs)

    def get_mask(self, name: str) -> Union[np.ndarray, None]:
        return self.current_masks.get('default', None)
