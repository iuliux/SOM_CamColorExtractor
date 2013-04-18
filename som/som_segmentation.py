#!/usr/bin/python
# -*- coding: utf-8 -*-

from learning_rate import *
from radius import *
from neighbourhood import *
from brightness import *

import numpy as np


LOWER_BOUND = 0.2
UPPER_BOUND = 0.7


def euclidian(x1, y1, z1, x2, y2, z2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)


def som_train(img_pixels, n, max_iters=3000, thresh=0.001):
    '''
    Learns the SOM and returns resulted n^2 cluster centroids, as 3 1D arrays:
        (R, G, B)
    @img_pixels = list of tuples (r, g, b), with values in [0, 1]
    @n = width of square neurons map (sqrt of total number of resulting colors)
    '''
    img_len = len(img_pixels)

    # Randomly init neurons' color
    WR = np.random.sample((1, n ** 2))
    WG = np.random.sample((1, n ** 2))
    WB = np.random.sample((1, n ** 2))

    delta = 99999
    deltas = []
    it = 0

    while it < max_iters and delta >= thresh:
        pick = np.random.randint(0, img_len)
        pick_rgb = img_pixels[pick]

        # Computes all distances and picks the closest
        dists = euclidian(WR, WG, WB, *pick_rgb)
        choosen = dists.argmin()

        # Restore matrix indeces from liniar index
        choosen_x = choosen % n
        choosen_y = choosen / n

        rad = radius(it, max_iters, n, n)
        eta = learning_rate(it, max_iters)
        # Generate neighbouring mask used to only influence the neighbours
        neigh = neighbourhood(choosen_x, choosen_y, rad, n, n)

        # Compute an aditional weight which favours medium-bright colors
        bright_w = brightness_score(*pick_rgb)

        # Compute deltas
        deltaR = eta * neigh * bright_w * (pick_rgb[0] - WR)
        deltaG = eta * neigh * bright_w * (pick_rgb[1] - WG)
        deltaB = eta * neigh * bright_w * (pick_rgb[2] - WB)

        # Update weights
        WR += deltaR
        WG += deltaG
        WB += deltaB

        # Convergence check
        delta = np.sum(np.abs(deltaR)) + np.sum(np.abs(deltaG)) + \
            np.sum(np.abs(deltaB))
        deltas.append(delta)

        it += 1
    return (WR, WG, WB)


def som_score_colors(orig_pixels, WR, WG, WB):
    '''
    Scores color centroids based on original image (SOM given as @WR, @WG, @WB)
    @orig_pixels = list of tuples (r, g, b), with values in [0, 1]
    @WR, @WG, @WB = red, green and blue coordinates of SOM neurons
    '''
    scores = [0] * WR.size

    for i, px in enumerate(orig_pixels):
        # Skip dark pixels
        if px[0] < LOWER_BOUND and px[1] < LOWER_BOUND and px[2] < LOWER_BOUND:
            continue
        # And bright ones
        if px[0] > UPPER_BOUND and px[1] > UPPER_BOUND and px[2] > UPPER_BOUND:
            continue

        dists = euclidian(WR, WG, WB, *px)
        choosen = dists.argmin()

        scores[choosen] += 1

    return scores
