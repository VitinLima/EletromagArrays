# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:30:55 2023

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
hfss_yagi4EL.set_position(x=0.0,y=0.0,z=0)

array_2Y4EL = Array.Array(
    name='Array 2Y4El',
    theta=theta.copy(),
    phi=phi.copy(),
    antennas=[
        Antenna.load_from_file(
            file_path,
            name='Yagi 4EL',
            theta=theta,
            phi=phi,
            load_mesh_from_file=False),
        Antenna.load_from_file(
            file_path,
            name='Yagi 4EL',
            theta=theta,
            phi=phi,
            load_mesh_from_file=False),
        ])
array_2Y4EL.antennas[0].set_orientation(
    roll=0, elevation=0, azimuth=0)
array_2Y4EL.antennas[0].set_position(x=0.0, y=0.0, z=0)
array_2Y4EL.antennas[1].set_orientation(
    roll=0, elevation=0, azimuth=45)
array_2Y4EL.antennas[1].set_position(x=0.0, y=1.5, z=0)
## Information for all 5 yagis (as a backup)
# array_2Y4EL.antennas[2].set_orientation(
#     roll=0, elevation=-45, azimuth=-45)
# array_2Y4EL.antennas[2].set_position(x=0, y=-1.5, z=0)
# array_2Y4EL.antennas[3].set_orientation(
#     roll=0, elevation=-45, azimuth=135)
# array_2Y4EL.antennas[3].set_position(x=0.34, y=-3.14, z=1.423)
# array_2Y4EL.antennas[4].set_orientation(
#     roll=0, elevation=72, azimuth=14)
# array_2Y4EL.antennas[4].set_position(x=0.83, y=1.19, z=-0.72)
array_2Y4EL.evaluate()

file_name = '2Y-4EL.csv'
file_path = os.path.join(header.antennas_dir, file_name)
hfss_2Y4EL = Antenna.load_from_file(file_path,
                                      name='HFSS Y4EL',
                                      theta=theta,
                                      phi=phi,
                                      load_mesh_from_file=False)

import App
import ResultFrame
import Result

app = App.App()

app.add_antenna(hfss_yagi4EL)
app.add_antenna(array_2Y4EL)
app.add_antenna(hfss_2Y4EL)

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
                         antenna=array_2Y4EL,
                         Ntheta=91,
                         Nphi=91,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         position=1)
result_2 = Result.Result(tab=tab_1,
                         name='HFSS',
                         title='HFSS',
                         antenna=hfss_2Y4EL,
                         Ntheta=91,
                         Nphi=91,
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
                         antenna=array_2Y4EL,
                         Ntheta=91,
                         Nphi=91,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         position=1)
result_2 = Result.Result(tab=tab_2,
                         name='HFSS',
                         title='HFSS',
                         antenna=hfss_2Y4EL,
                         Ntheta=91,
                         Nphi=91,
                         plot=plot,
                         field=field,
                         color=color,
                         in_dB=in_dB,
                         position=2)
app.add_tab(tab_2)

app.mainloop()
