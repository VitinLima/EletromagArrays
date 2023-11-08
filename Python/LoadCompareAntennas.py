# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:08:15 2023

@author: 160047412
"""

import ResultFrame
import Result

def load_compare_graphs(app, name, antennas, titles):
    tab = ResultFrame.ResultFrame(
        master=app.tabs,
        name=name,
        columns=2,
        rows=2)
    for i,antenna,title in zip(range(2),antennas,titles):
        # Result.Result(tab=tab,
        #               name='F ' + title,
        #               antenna=antenna,field='F',
        #               plot='3d Polar',
        #               in_dB=True,
        #               position=i+1)
        Result.Result(tab=tab,
                      name='Fref ' + title,
                      title='Fref ' + title,
                      antenna=antenna,field='Fref',
                      plot='2d Polar Patch',
                      in_dB=True,
                      position= i+1)
        Result.Result(tab=tab,
                      name='Fcross ' + title,
                      title='Fcross ' + title,
                      antenna=antenna,field='Fcross',
                      plot='2d Polar Patch',
                      in_dB=True,
                      position= i+1 + 2)
        # Result.Result(tab=tab,
        #               name='Ftheta ' + title,
        #               title='Ftheta ' + title,
        #               antenna=antenna,field='Ftheta',
        #               plot='2d Polar Patch',
        #               in_dB=True,
        #               position=i+1 + 4)
        # Result.Result(tab=tab,
        #               name='Fphi ' + title,
        #               title='Fphi ' + title,
        #               antenna=antenna,field='Fphi',
        #               plot='2d Polar Patch',
        #               in_dB=True,
        #               position=i+1 + 5)
        # Result.Result(tab=tab,
        #               name='Frhcp ' + title,
        #               title='Frhcp ' + title,
        #               antenna=antenna,field='Frhcp',
        #               plot='2d Polar Patch',
        #               in_dB=True,
        #               position=i+1 + 6)
        # Result.Result(tab=tab,
        #               name='Flhcp ' + title,
        #               title='Flhcp ' + title,
        #               antenna=antenna,field='Flhcp',
        #               plot='2d Polar Patch',
        #               in_dB=True,
        #               position=i+1 + 7)
    app.add_tab(tab)