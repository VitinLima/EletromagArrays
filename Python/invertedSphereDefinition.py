#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 18:55:55 2023

@author: vitinho
"""

import sys
import os
import header

#python_path = header.python_path
results_dir = os.path.join(header.results_dir, 'Validation')
#home_dir = header.home_dir
antennas_dir = header.antennas_dir

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
array_rotated.evaluate()

plot='3d Polar'
field='F'
color='Color by magnitude'
in_dB = False

export_directory = os.path.join(results_dir,
                                'InvertedSphere')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)

import ResultFigure
import Result

figure = ResultFigure.ResultFigure()
plot = '2d Polar Patch'
Result.Result(tab=figure,
              title='',
              antenna=array_rotated,
              field=field,
              color=color,
              plot=plot,
              # ticks_flag=False,
              in_dB=True,
              Ntheta=91,
              Nphi=91,)
figure.draw()
fname = os.path.join(
    export_directory, '2d polar patch' + '.png')
figure.figure.savefig(fname)
plt.close('all')

figure = ResultFigure.ResultFigure()
plot = '2d Polar Patch Type 2'
Result.Result(tab=figure,
              title='',
              antenna=array_rotated,
              field=field,
              color=color,
              plot=plot,
              # ticks_flag=False,
              in_dB=True,
              Ntheta=91,
              Nphi=91,)
figure.draw()
fname = os.path.join(
    export_directory, '2d polar patch 2' + '.png')
figure.figure.savefig(fname)
plt.close('all')
