import numpy as np
import cv2 as cv

from epta.tools.recognition import BaseRecogniser


class SkillLevelRecognition(BaseRecogniser):
    def __init__(self, name: str = 'skill_level_rec', **kwargs):
        super(SkillLevelRecognition, self).__init__(name=name, **kwargs)

    @staticmethod
    def image_to_data(image: 'np.ndarray', *args, **kwargs) -> int:
        bw_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        if not (mid_position := bw_image.shape[0] // 2 - 1) > 0:
            mid_position = 0

        mid_pixels = bw_image[mid_position]

        high_values = np.where(mid_pixels > 100, 1, 0)
        low_values = np.where(mid_pixels < 100, 0, 0)
        all_values = high_values + low_values

        temp = (np.roll(all_values, -1) - all_values)[:-1]
        result = np.sum(temp < 0).item()

        return result
