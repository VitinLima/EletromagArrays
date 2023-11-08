#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 18:25:52 2023

@author: vitinho
"""

import sys
import os
path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, path)

import Optimization

def run(target_antenna, working_array, x_map, cost_function, disp=False, **kw):         
    optim = Optimization.Optimization(
        cost_function = cost_function,
        working_array = working_array,
        target_antenna = target_antenna,
        x_map = x_map,
        # method = 'L-BFGS-B',
        disp=disp,
        **kw
        )
    
    try:
        result = optim.run()
    except Exception as e:
        print(e)
    
    return optim, result, optim.working_array
    
    # os.system('shutdown /h')