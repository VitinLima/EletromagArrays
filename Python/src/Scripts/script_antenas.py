#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:31:27 2023

@author: vitinho
"""
import os
import sys
import header

python_path = header.python_path
results_dir = os.path.join(header.results_dir, 'Circular Polarization')
home_dir = header.home_dir
antennas_dir = header.antennas_dir

import numpy as np

import matplotlib.pyplot as plt
plt.close('all')

import AntennasLoaders.LoadHFSSYagis
# import Scripts.AntennasLoaders.LoadHFSSValidationArrays
# import Scripts.AntennasLoaders.LoadValidationArrays

Ntheta = 91
Nphi = 91

antennas = AntennasLoaders.LoadHFSSYagis.run(
    Ntheta=Ntheta, Nphi=Nphi, elevation=-90)

import Array

Ntheta=91
Nphi=181

theta=np.linspace(0, 180, Ntheta)
phi=np.linspace(-180, 180, Nphi)

array = Array.Array(name='Custom',
                    theta=theta.copy(),
                    phi=phi.copy(),
                    antennas=[
                        antennas['hfss_yagi2EL'].copy(),
                        antennas['hfss_yagi2EL'].copy(),
                        ])
array.antennas[0].set_position(x=0,y=0,z=0)
array.antennas[0].set_orientation(
    elevation=-90,azimuth=0,roll=0)
array.antennas[0].set_current(
    magnitude=1.0,
    phase=0)
array.antennas[1].set_position(x=0,y=0,z=0)
array.antennas[1].set_orientation(
    elevation=-90,azimuth=0,roll=90)
array.antennas[1].set_current(
    magnitude=1.0,
    phase=90)
array.evaluate()

import Result
import ResultFigure

plot = '2d Polar Patch'

field = 'F'
figure = ResultFigure.ResultFigure(
    columns=1,rows=1)
result = Result.Result(
    tab=figure,
    title='Custom Array',
    name='Custom Array',
    antenna=array,
    field=field,
    plot=plot,
    ticks_flag=False,
    in_dB=True,
    column=1,row=1,
    Ntheta=Ntheta,
    Nphi=Nphi
    )
figure.draw()
fname = os.path.join(
    results_dir, array.name +
        ' F' + '.png')
figure.figure.savefig(fname)
plt.close('all')