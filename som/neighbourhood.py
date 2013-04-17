#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np


def neighbourhood(x, y, radius, width, height):
    '''
    Generates a mask with [0, 1] values to activate the inside of the @radius
    radius circle centered in (x,y). Returnes 1D numpy array with liniarized
    matrix mask.
    '''
    mask = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            distance = np.sqrt((i - y)**2 + (j - x)**2)
            if distance <= radius:
                mask[i, j] = 1 - distance / float(radius)

    return mask.reshape(1, mask.size)

if __name__ == "__main__":
    '''Test example: python neighbourhood.py 5 6 3 7 7'''
    m = neighbourhood(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]),
                      int(sys.argv[4]), int(sys.argv[5]))
    print m
