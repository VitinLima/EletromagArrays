# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:08:15 2023

@author: 160047412
"""

import ResultFrame
import Result

def load_compare_graphs(app, name, antennas, titles):
    tab = ResultFrame.ResultFrame(master=app.tabs,name=name,iy=2)
    ix = len(antennas)
    for i,antenna,title in zip(range(len(antennas)),antennas,titles):
        # Result.Result(tab=tab,
        #               name='F ' + title,
        #               antenna=antenna,field='F',
        #               plot='3d Polar',
        #               in_dB=True,
        #               preferred_position=1+i)
        Result.Result(tab=tab,
                      name='Fref ' + title,
                      antenna=antenna,field='Fref',
                      plot='2d Polar Patch',
                      in_dB=True,
                      preferred_position=1+i+ix*1)
        Result.Result(tab=tab,
                      name='Fcross ' + title,
                      antenna=antenna,field='Fcross',
                      plot='2d Polar Patch',
                      in_dB=True,
                      preferred_position=1+i+ix*2)
        # Result.Result(tab=tab,
        #               name='Ftheta ' + title,
        #               antenna=antenna,field='Ftheta',
        #               plot='2d Polar Patch',
        #               in_dB=True,
        #               preferred_position=1+i+ix*3)
        # Result.Result(tab=tab,
        #               name='Fphi ' + title,
        #               antenna=antenna,field='Fphi',
        #               plot='2d Polar Patch',
        #               in_dB=True,
        #               preferred_position=1+i+ix*4)
    app.add_tab(tab)