import numpy as np

from epta.tools.recognition import BaseRecogniser


class EasyTargetIndicator(BaseRecogniser):
    def __init__(self, name: str = 'target_indicator', **kwargs):
        self._border_value = np.array([90, 81, 49])
        super(EasyTargetIndicator, self).__init__(name=name, **kwargs)

    def image_to_data(self, image: np.ndarray, *args, **kwargs) -> bool:
        image = image[:, 0]
        if np.all(image == self._border_value):
            return True
        else:
            return False

class AlwaysActiveIndicator(BaseRecogniser):
    def __init__(self, name: str = 'target_indicator', **kwargs):
        super(AlwaysActiveIndicator, self).__init__(name=name, **kwargs)

    @staticmethod
    def image_to_data(*args, **kwargs) -> bool:
        return True
