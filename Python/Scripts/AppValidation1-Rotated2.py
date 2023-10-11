# -*- coding: utf-8 -*-
"""
Created on Wed May 24 19:11:14 2023

@author: 160047412
"""

import sys
import os
import numpy as np

path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, path)

import Antenna
import Array

theta=np.linspace(0, 180, 91)
phi=np.linspace(-180, 180, 91)
# antennas_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
antennas_dir = '/media/vitinho/DADOS/TCC/Antennas'

file_name = '1Y-4EL.csv'
file_path = os.path.join(antennas_dir, file_name)
hfss_yagi4EL = Antenna.load_from_file(file_path,
                                 name='Yagi 4EL',
                                 theta=theta,
                                 phi=phi,
                                 load_mesh_from_file=False)

file_name = '1Y-4EL-Rotated.csv'
file_path = os.path.join(antennas_dir, file_name)
hfss_yagi4EL_R = Antenna.load_from_file(file_path,
                                      name='HFSS Y4EL R',
                                      theta=theta,
                                      phi=phi,
                                      load_mesh_from_file=False)

import App
import ResultFrame
import Result

app = App.App()

app.add_antenna(hfss_yagi4EL)
app.add_antenna(hfss_yagi4EL_R)

plot='2d Polar Patch Type 2'
field='Ftheta'
color='Color by phase'
in_dB = False

tab_1 = ResultFrame.ResultFrame(master=app.tabs,name='Phase',iy=2)
result_1 = Result.Result(tab=tab_1,
                         name='Array',
                         title='Array',
                         antenna=hfss_yagi4EL,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         preferred_position=1)
result_2 = Result.Result(tab=tab_1,
                         name='HFSS',
                         title='HFSS',
                         antenna=hfss_yagi4EL_R,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         preferred_position=2)
app.add_tab(tab_1)

field='F'
color='Color by magnitude'
tab_2 = ResultFrame.ResultFrame(master=app.tabs,name='Mag',iy=2)
result_1 = Result.Result(tab=tab_2,
                         name='Array',
                         title='Array',
                         antenna=hfss_yagi4EL,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         preferred_position=1)
result_2 = Result.Result(tab=tab_2,
                         name='HFSS',
                         title='HFSS',
                         antenna=hfss_yagi4EL_R,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         preferred_position=2)
app.add_tab(tab_2)

# def custom_plot(result):
#     pass

# tab_2 = ResultFrame.ResultFrame(master=app.tabs,name='Difference',iy=2)
# result_3 = Result.Result(tab=tab_2,
#                          name='Difference',
#                          plot='custom')


app.mainloop()