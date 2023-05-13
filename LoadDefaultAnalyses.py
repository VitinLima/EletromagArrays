# -*- coding: utf-8 -*-
"""
Created on Wed May 10 17:30:52 2023

@author: 160047412
"""

import Analysis

def load_default_analyses():
    F = Analysis.Analysis(name='F',expression='F')
    Ftheta = Analysis.Analysis(name='Ftheta',expression='Ftheta',color_expression='')
    Fphi = Analysis.Analysis(name='Fphi',expression='Fphi',color_expression='')
    Frhcp = Analysis.Analysis(name='Frhcp',expression='Frhcp',color_expression='')
    Flhcp = Analysis.Analysis(name='Flhcp',expression='Flhcp',color_expression='')
    
    return dict(F,
                Ftheta,
                Fphi,
                Frhcp,
                Flhcp)