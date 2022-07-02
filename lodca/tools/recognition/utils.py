import numpy as np
import cv2 as cv


def to_black_white(image: 'np.ndarray', thr: int = 100, *args, **kwargs) -> 'np.ndarray':
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = np.where(image > thr, 0, 255)
    return image.astype(np.uint8)
    # return np.concatenate([image.astype(np.uint8)[..., None]]*3, axis=-1)


def wrapper(fnc, **f_kwargs):
    def fn(*args, **kwargs):
        return fnc(*args, **f_kwargs, **kwargs)

    return fn


def resize_thr(image: 'np.ndarray', thr: int = 100, pad: bool = False, resc: int = 4, cut: bool = True,
               invert: bool = False, to_gray: bool = True, same_values: int = False, thr_gauss: bool = False,
               **kwargs) -> 'np.ndarray':
    if same_values:
        image = same_values_filer(image, thr=same_values)
    image = cv.resize(image, (int(image.shape[1] * resc), int(image.shape[0] * resc)), cv.INTER_LINEAR)
    pad_value = 0
    if invert:
        image = 255 - image
        pad_value = 255
    if pad:
        image = pad_image(image, resc=resc, pad_value=pad_value)
    if to_gray:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    if cut:
        image = image[:, :-10]
    if thr:
        image = np.where(image > thr, 0, 255).astype(np.uint8)
    if thr_gauss:
        image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

    return image.astype(np.uint8)


def invert_colors(image: "np.ndarray", *args, **kwargs) -> 'np.ndarray':
    return 255 - image


def pad_image(image: 'np.ndarray', resc: int = 1, pad_value: int = 0, *args, **kwargs):
    extra_left, extra_right = int(10 * resc), int(10 * resc)
    extra_top, extra_bottom = int(5 * resc), int(5 * resc)
    return np.pad(image, ((extra_left, extra_right), (extra_top, extra_bottom), (0, 0)),
                  mode='constant', constant_values=pad_value)


def same_values_filer(image: 'np.ndarray', thr: int = 20, **kwargs):
    # Remove values with difference > thr
    image = np.array(image, dtype=np.int32)
    rg = np.abs(image[..., 0] - image[..., 1])[..., None]
    gb = np.abs(image[..., 1] - image[..., 2])[..., None]
    rb = np.abs(image[..., 0] - image[..., 2])[..., None]
    mask = np.any(np.concatenate([rg, gb, rb], axis=-1) > thr, axis=-1)[..., None]
    image = np.where(mask, [0, 0, 0], image).astype(np.uint8)
    return image
