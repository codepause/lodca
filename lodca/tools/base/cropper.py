from typing import Tuple

from epta.tools.base import PositionCropper as PCr


class PositionCropper(PCr):
    """
    Modified position cropper to handle new namespaces (**step**, etc.).
    """
    @staticmethod
    def _make_single_position(n_row: int = 0, n_col: int = 0, **kwargs) -> Tuple[int, int, int, int]:
        positions = kwargs.get('positions', {})
        starting_x = kwargs.get('x', 0.)
        starting_y = kwargs.get('y', 0.)
        w = kwargs.get('w', None) or positions.get('w', 0)
        h = kwargs.get('h', None) or positions.get('h', 0)
        step_w = kwargs.get('step_w', None) or positions.get('step_w', 0)
        step_h = kwargs.get('step_h', None) or positions.get('step_h', 0)

        current_x_start = starting_x + n_col * (w + step_w)
        current_y_start = starting_y + n_row * (h + step_h)
        current_x_end = int(current_x_start + w)
        current_y_end = int(current_y_start + h)

        current_y_start = int(current_y_start)
        current_x_start = int(current_x_start)

        return current_x_start, current_y_start, current_x_end, current_y_end

    def make_single_position(self, *args, key: str = None, **kwargs):
        if key is None:
            key = self.key
        kwrgs = dict(self.position_manager[key].items())
        return self._make_single_position(*args, **kwrgs)


class MultiCropper(PositionCropper):
    """
    Crop multiple rectangles from grid of :attr:`n_rows` and :attr:`n_rows`.

    Args:
        n_rows (int): number of rows.
        n_cols (int): number of columns.
    """
    def __init__(self, n_rows: int = 2, n_cols: int = 3, name: str = 'multi_cropper', **kwargs):
        super(MultiCropper, self).__init__(name=name, **kwargs)

        self._n_rows = n_rows
        self._n_cols = n_cols

    def make_single_position(self, key: str = None, *args, **kwargs) -> list:
        if key is None:
            key = self.key
        kwrgs = dict(self.position_manager[key].items())
        result = list()
        for n_row in range(self._n_rows):
            for n_col in range(self._n_cols):
                result.append(self._make_single_position(n_row, n_col, **kwrgs))
        return result

    def crop(self, image: 'np.ndarray', *args, **kwargs) -> list:
        result = list()
        for position in self.inner_position:
            x_start, y_start, x_end, y_end = position
            crop = image[y_start:y_end, x_start:x_end]
            result.append(crop)
        return result

