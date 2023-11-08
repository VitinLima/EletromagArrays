# -*- coding: utf-8 -*-
"""
Created on Thu May 11 00:58:16 2023

@author: 160047412
"""

import sys
import os
path = os.path.split(__file__)[0]
path = os.path.split(path)[0]
sys.path.insert(0, path)
path = os.path.split(path)[0]
home_directory = os.path.split(path)[0]
antennas_dir=os.path.join(home_directory, 'Antennas')

import ResultFrame
import Result

def load_default_graphs(app, name, antenna, 
                        fields=['F',
                                'Fref',
                                'Fcross',
                                # 'Ftheta',
                                # 'Fphi',
                                # 'Frhcp',
                                # 'Flhcp',
                                ]):
    plots = dict(
        # F='3d Polar Surface',
        F='2d Polar Patch',
        Fref='2d Polar Patch',
        Fcross='2d Polar Patch',
        Ftheta='2d Polar Patch',
        Fphi='2d Polar Patch',
        Frhcp='2d Polar Patch',
        Flhcp='2d Polar Patch')
    pos = dict(F='i',
               Fref='i',
               Fcross='i',
               Ftheta='i',
               Fphi='i',
               Frhcp='i',
               Flhcp='i')
    tab = ResultFrame.ResultFrame(
        master=app.tabs,
        name=name,
        columns=3,
        rows=1)
    i = 1
    for field in fields:
        if pos[field]=='i':
            Result.Result(tab=tab,
                          name=field,
                          title=field,
                          antenna=antenna,field=field,
                          plot=plots[field],
                          in_dB=True,
                          position=i)
            i += 1
        else:
            Result.Result(tab=tab,
                          name=field,
                          title=field,
                          antenna=antenna,field=field,
                          plot=plots[field],
                          in_dB=True,
                          position=pos[field])
            i = pos[field][-1]+1
    app.add_tab(tab)