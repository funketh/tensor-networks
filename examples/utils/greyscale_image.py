from math import cos, pi, sin

from tensor_networks.annotations import *
from tensor_networks.patched_numpy import np


def color_abs_to_percentage(value: AbsColor) -> PartialColor:
    """
    :param value: An integer color value [0;255]
    :return: The color value in percent [0;1]
    """
    return value / 255


def greyscale_feature(percentage: PartialColor) -> Array:
    """
    :param percentage: A grey value
    :return: An array of a black value and a white value with a sum of 1
    """
    return np.array([cos(pi / 2 * percentage), sin(pi / 2 * percentage)])


def image_feature(absolute_colors: Array) -> Array:
    return np.array(list(map(greyscale_feature,
                             map(color_abs_to_percentage,
                                 absolute_colors))))
