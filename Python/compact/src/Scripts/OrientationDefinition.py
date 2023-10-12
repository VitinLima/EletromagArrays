#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 19:03:59 2023

@author: vitinho
"""

import sys
import os
path = os.path.split(__file__)[0]
path = os.path.split(path)[0]
sys.path.insert(0, path)
path = os.path.split(path)[0]
home_directory = os.path.split(path)[0]
antennas_dir=os.path.join(home_directory, 'Antennas')

import numpy as np

import Antenna
import Array

import matplotlib.pyplot as plt

theta=np.linspace(0, 180, 91)
phi=np.linspace(-180, 180, 91)

file_name = 'antenna-Yagi-4Elements.csv'
file_path = os.path.join(antennas_dir, file_name)
hfss_yagi4EL = Antenna.load_from_file(file_path,
                                 name='Yagi 4EL',
                                 theta=theta,
                                 phi=phi,
                                 load_mesh_from_file=False)

array_rotated = Array.Array(
    name='Array 1Y4El',
    theta=theta.copy(),
    phi=phi.copy(),
    antennas=[hfss_yagi4EL])
array_rotated.antennas[0].set_orientation(roll=60, elevation=-30,
                                          azimuth=-130)
# array_rotated.antennas[0].set_orientation(roll=0, elevation=0,
#                                           azimuth=0)
array_rotated.evaluate()

plot='3d Polar'
field='F'
color='Color by magnitude'
in_dB = False

export_directory = os.path.join(home_directory,
                                'Python',
                                'ExportedResults',
                                'Orientation')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)

import ResultFigure
import Result

figure = ResultFigure.ResultFigure()
plot = '3d Polar'
Result.Result(tab=figure,
              title='',
              antenna=array_rotated,
              field=field,
              color=color,
              plot=plot,
              ticks_flag=False,
              in_dB=True,
              Ntheta=91,
              Nphi=91,)
figure.draw()
a = array_rotated.antennas[0]
fname = os.path.join(
    export_directory, 'e={}, a={}, r={}'.format(a.elevation,
                                                a.azimuth,
                                                a.roll) + '.png')
figure.figure.savefig(fname)
plt.close('all')