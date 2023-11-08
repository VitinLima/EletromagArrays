# -*- coding: utf-8 -*-
"""
Created on Wed May 24 13:23:36 2023

@author: 160047412
"""

import sys
import os

import header

import numpy as np

import Antenna
import Array

theta=np.linspace(0, 180, 91)
phi=np.linspace(-180, 180, 91)

file_name = 'antenna-Yagi-4Elements.csv'
file_path = os.path.join(header.antennas_dir, file_name)
hfss_yagi4EL = Antenna.load_from_file(file_path,
                                 name='Yagi 4EL',
                                 theta=theta,
                                 phi=phi,
                                 load_mesh_from_file=False)

array_1Y4EL = Array.Array(
    name='Array 1Y4El',
    theta=theta.copy(),
    phi=phi.copy(),
    antennas=[hfss_yagi4EL])
array_1Y4EL.evaluate()

file_name = '1Y-4EL.csv'
file_path = os.path.join(header.antennas_dir, file_name)
hfss_yagi4EL = Antenna.load_from_file(file_path,
                                      name='HFSS Y4EL',
                                      theta=theta,
                                      phi=phi,
                                      load_mesh_from_file=False)

import App
import ResultFrame
import Result

app = App.App()

app.add_antenna(hfss_yagi4EL)
app.add_antenna(array_1Y4EL)
app.add_antenna(hfss_yagi4EL)

plot='2d Polar Patch Type 2'
field='Ftheta'
color='Color by phase'
in_dB = False

tab_1 = ResultFrame.ResultFrame(
    master=app.tabs,
    name='Phase',
    columns=2)
result_1 = Result.Result(tab=tab_1,
                         name='Array',
                         title='Array',
                         antenna=array_1Y4EL,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         position=1)
result_2 = Result.Result(tab=tab_1,
                         name='HFSS',
                         title='HFSS',
                         antenna=hfss_yagi4EL,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         position=2)
app.add_tab(tab_1)

field='F'
color='Color by magnitude'
tab_2 = ResultFrame.ResultFrame(
    master=app.tabs,
    name='Magnitude',
    columns=2)
result_1 = Result.Result(tab=tab_2,
                         name='Array',
                         title='Array',
                         antenna=array_1Y4EL,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         position=1)
result_2 = Result.Result(tab=tab_2,
                         name='HFSS',
                         title='HFSS',
                         antenna=hfss_yagi4EL,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         position=2)
app.add_tab(tab_2)

app.mainloop()
