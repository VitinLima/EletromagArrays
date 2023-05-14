# -*- coding: utf-8 -*-
"""
Created on Thu May 11 00:58:16 2023

@author: 160047412
"""

import ResultFrame
import Result

def load_default_graphs(app, name, antenna):
    tab = ResultFrame.ResultFrame(master=app.tabs,name=name,iy=2)
    Result.Result(tab=tab,
                  name='F',
                  antenna=antenna,field='F',
                  plot='3d Polar Surface',
                  in_dB=True,
                  preferred_position=(1,2))
    Result.Result(tab=tab,
                  name='Fref',
                  antenna=antenna,field='Fref',
                  plot='2d Polar Patch',
                  in_dB=True,
                  preferred_position=3)
    Result.Result(tab=tab,
                  name='Fcross',
                  antenna=antenna,field='Fcross',
                  plot='2d Polar Patch',
                  in_dB=True,
                  preferred_position=4)
    # Result.Result(tab=tab,
    #               name='Ftheta',
    #               antenna=antenna,field='Ftheta',
    #               plot='2d Polar Patch',
    #               in_dB=True,
    #               preferred_position=5)
    # Result.Result(tab=tab,
    #               name='Fphi',
    #               antenna=antenna,field='Fphi',
    #               plot='2d Polar Patch',
    #               in_dB=True,
    #               preferred_position=6)
    app.add_tab(tab)