# -*- coding: utf-8 -*-
"""
Created on Thu May 11 00:58:16 2023

@author: 160047412
"""

import ResultFrame
import Result

def load_default_graphs(app, name, antenna, fields=['F', 'Fref', 'Fcross', 'Ftheta', 'Fphi']):
    plots = dict(F='3d Polar Surface',
                 Fref='2d Polar Patch',
                 Fcross='2d Polar Patch',
                 Ftheta='2d Polar Patch',
                 Fphi='2d Polar Patch')
    pos = dict(F=(1,2),
               Fref='i',
               Fcross='i',
               Ftheta='i',
               Fphi='i')
    tab = ResultFrame.ResultFrame(master=app.tabs,name=name,iy=2)
    i = 1
    for field in fields:
        if pos[field]=='i':
            Result.Result(tab=tab,
                          name=field,
                          title=field,
                          antenna=antenna,field=field,
                          plot=plots[field],
                          in_dB=True,
                          preferred_position=i)
            i += 1
        else:
            Result.Result(tab=tab,
                          name=field,
                          title=field,
                          antenna=antenna,field=field,
                          plot=plots[field],
                          in_dB=True,
                          preferred_position=pos[field])
            i += len(pos[field])
    app.add_tab(tab)