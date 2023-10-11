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

# import numpy as np

import Optimization
# import SpecialOptim

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
    
    # optim = SpecialOptim.SpecialOptim(
    #                      available_antennas = [
    #                                 # antennas['hfss_yagi1EL'],
    #                                 antennas['hfss_yagi2EL'],
    #                                 # antennas['hfss_yagi3EL'],
    #                                 # antennas['hfss_yagi4EL'],
    #                                 # antennas['hfss_yagi1EL_V'],
    #                                 # antennas['hfss_yagi2EL_V'],
    #                                 # antennas['hfss_yagi3EL_V'],
    #                                 # antennas['hfss_yagi4EL_V']
    #                          ],
    #                      # weights=[1],
    #                      target_antenna = target_antenna,
    #                      variables=[
    #                             'elevation',
    #                             # 'azimuth',
    #                             # 'roll',
    #                             # 'x',
    #                             'y',
    #                             # 'z',
    #                             # 'current magnitude',
    #                             # 'current phase',
    #                          ],
    #                      N_start = 1,
    #                      N_stop = 2,
    #                      # weight_mask=weight_mask,
    #                      # method = 'L-BFGS-B',
    #                       disp=False,
    #                      )
    
    try:
        result = optim.run()
    except Exception as e:
        print(e)
    
    return optim, result
    
    # os.system('shutdown /h')