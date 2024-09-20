import math


def find_distance(height):
    return -16.10 * height + 2875


def find_angle(monitor_x_position):
    pixels_from_center = monitor_x_position - 1280
    angle = pixels_from_center * 0.04376
    return angle



