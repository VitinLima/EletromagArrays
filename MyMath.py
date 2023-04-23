# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:16:37 2023

@author: 160047412
"""

import numpy as np

sqrt2 = np.sqrt(2)

def rotate(vec, R):
    new_vec = np.zeros_like(vec)
    R_swapped = R.swapaxes(2,3)
    new_vec[:,:,0] = (vec*R_swapped[:,:,:,0]).sum(2)
    new_vec[:,:,1] = (vec*R_swapped[:,:,:,1]).sum(2)
    new_vec[:,:,2] = (vec*R_swapped[:,:,:,2]).sum(2)
    return new_vec