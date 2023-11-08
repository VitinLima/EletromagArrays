# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:16:37 2023

@author: 160047412
"""

import numpy as np

sqrt2 = np.sqrt(2)


def rotx(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    R = np.zeros((angle.shape[0], angle.shape[1], 3, 3))
    R[:, :, 0, 0] = 1
    R[:, :, 0, 1] = 0
    R[:, :, 0, 2] = 0
    R[:, :, 1, 0] = 0
    R[:, :, 1, 1] = c
    R[:, :, 1, 2] = -s
    R[:, :, 2, 0] = 0
    R[:, :, 2, 1] = s
    R[:, :, 2, 2] = c

    return R


def roty(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    R = np.zeros((angle.shape[0], angle.shape[1], 3, 3))
    R[:, :, 0, 0] = c
    R[:, :, 0, 1] = 0
    R[:, :, 0, 2] = s
    R[:, :, 1, 0] = 0
    R[:, :, 1, 1] = 1
    R[:, :, 1, 2] = 0
    R[:, :, 2, 0] = -s
    R[:, :, 2, 1] = 0
    R[:, :, 2, 2] = c

    return R


def rotz(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    R = np.zeros((angle.shape[0], angle.shape[1], 3, 3))
    R[:, :, 0, 0] = c
    R[:, :, 0, 1] = -s
    R[:, :, 0, 2] = 0
    R[:, :, 1, 0] = s
    R[:, :, 1, 1] = c
    R[:, :, 1, 2] = 0
    R[:, :, 2, 0] = 0
    R[:, :, 2, 1] = 0
    R[:, :, 2, 2] = 1

    return R


def rotate(vec, R):
    new_vec = np.zeros_like(vec)
    R_swapped = R.swapaxes(2, 3)
    new_vec[:, :, 0] = (vec*R_swapped[:, :, :, 0]).sum(2)
    new_vec[:, :, 1] = (vec*R_swapped[:, :, :, 1]).sum(2)
    new_vec[:, :, 2] = (vec*R_swapped[:, :, :, 2]).sum(2)
    return new_vec
