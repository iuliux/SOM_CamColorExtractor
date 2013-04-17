# -*- coding: utf-8 -*-


def radius(iter_no, iter_count, width, height):
    '''Computes the radius, depending on the step in iteration'''
    MAX_VALUE = max(width, height) / 2.0
    MIN_VALUE = 0
    totalrange = MAX_VALUE - MIN_VALUE
    step = iter_no / float(iter_count)

    # Quadratic function (**2 can be changed for different function)
    r = MAX_VALUE - step**2 * totalrange
    return r
