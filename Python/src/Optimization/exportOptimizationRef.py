#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 21:06:42 2023

@author: vitinho
"""

import sys
import os
path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, path)

import matplotlib.pyplot as plt
plt.close('all')

print("Loading antennas")

import Scripts.AntennasLoaders.LoadHFSSYagis
antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(Ntheta=91, Nphi=91)

print("Loading export results directory")

export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/OptimizationLinear'
if not os.path.exists(export_directory):
    os.mkdir(export_directory)

print("Creating target distribution")

import numpy as np

import Array

Ntheta=91
Nphi=181

theta=np.linspace(0, 180, Ntheta)
phi=np.linspace(-180, 180, Nphi)

target_antenna = Array.Array(name='Target Cross',
                            theta=theta.copy(),
                            phi=phi.copy(),
                            antennas=[
                                antennas['hfss_yagi2EL'].copy(),
                                antennas['hfss_yagi2EL'].copy(),
                                antennas['hfss_yagi2EL'].copy(),
                          ])
target_antenna.antennas[0].set_position(x=0,y=0,z=0)
target_antenna.antennas[0].set_orientation(elevation=-90,azimuth=90)
target_antenna.antennas[1].set_position(x=0,y=0.5,z=0)
target_antenna.antennas[1].set_orientation(elevation=-90,azimuth=0)
target_antenna.antennas[2].set_position(x=0,y=1,z=0)
target_antenna.antennas[2].set_orientation(elevation=-90,azimuth=120)
target_antenna.evaluate()

print("Creating working array")

working_array = Array.Array(name='Initial array',
                            theta=theta.copy(),
                            phi=phi.copy(),
                            antennas=[
                                antennas['hfss_yagi2EL'].copy(),
                                antennas['hfss_yagi2EL'].copy(),
                                antennas['hfss_yagi2EL'].copy(),
                          ])
working_array.antennas[0].set_position(x=0,y=0,z=0)
working_array.antennas[0].set_orientation(elevation=-90,azimuth=90)
working_array.antennas[1].set_position(x=0.3,y=1.3,z=0)
working_array.antennas[1].set_orientation(elevation=-90,azimuth=90)
working_array.antennas[2].set_position(x=-0.3,y=0.6,z=0)
working_array.antennas[2].set_orientation(elevation=-90,azimuth=90)
working_array.evaluate()

print("Exporting initial state")

import Scripts.ExportResults

# Scripts.ExportResults.run([
#     working_array,
#     ], export_directory)

print("Optimizing")

def cost_function(target, result):
    total_cost = np.abs(np.abs(target.Fcross)-np.abs(result.Fcross)).sum()
    total_cost += np.abs(np.abs(target.Fref)-np.abs(result.Fref)).sum()
    return total_cost

import Optimization

optim = Optimization.Optimization(
    target_antenna=target_antenna,
    working_array=working_array,
    x_map = [
        dict(
            antenna=working_array.antennas[1],
            variables = [
                'x',
                'y',
                'roll',
                ],
            ),
        dict(
            antenna=working_array.antennas[2],
            variables = [
                'x',
                'y',
                'roll',
                ],
            ),
        ],
    cost_function=cost_function,
    # method = 'L-BFGS-B',
    )

result = optim.run()
result_array = optim.working_array

print(result)

target_antenna.name = 'Target Antenna'
result_array.name = 'Result Array'

print("Exporting results")

# Scripts.ExportResults.run([
#     target_antenna,
#     result_array,
#     ], export_directory)

print("Starting visualization")

import App
import ResultFrame
import Result

app = App.App(antennas=[target_antenna, result_array])
try:
    Ntheta = 91
    Nphi = 181
    field = 'F'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
    Result.Result(tab=tab,
                  title='',
                  name='Result F',
                  antenna=result_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  column=1,row=1,
                  Ntheta=Ntheta,
                  Nphi=Nphi)
    Result.Result(tab=tab,
                  title='',
                  name='Target F',
                  antenna=target_antenna,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  column=2,row=1,
                  Ntheta=Ntheta,
                  Nphi=Nphi)
    app.add_tab(tab)
    
    field = 'Fref'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
    Result.Result(tab=tab,
                  title='Result Ref',
                  name='Result Ref',
                  antenna=result_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  column=1,row=1,
                  Ntheta=Ntheta,
                  Nphi=Nphi)
    Result.Result(tab=tab,
                  title='Target ref',
                  name='Target Ref',
                  antenna=target_antenna,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  column=2,row=1,
                  Ntheta=Ntheta,
                  Nphi=Nphi)
    app.add_tab(tab)
    
    field = 'Fcross'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
    Result.Result(tab=tab,
                  title='',
                  name='Result Cross',
                  antenna=result_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  column=1,row=1,
                  Ntheta=Ntheta,
                  Nphi=Nphi)
    Result.Result(tab=tab,
                  title='',
                  name='Target Cross',
                  antenna=target_antenna,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  column=2,row=1,
                  Ntheta=Ntheta,
                  Nphi=Nphi)
    app.add_tab(tab)
    
    # Main application loop
    app.mainloop()
except Exception as e:
    # If some error occur, destroy the application to close the window,
    # then show the error
    app.destroy()
    raise e