#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 18:30:36 2023

@author: vitinho
"""

import sys
import os
path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, path)

import matplotlib.pyplot as plt
plt.close('all')

import pickle

import Optimization

print("Loading antennas")

import Scripts.AntennasLoaders.LoadHFSSYagis
antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(Ntheta=91, Nphi=91)

print("Loading export results directory")

N = 7
export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/OptimizationCircular' + str(N)
if not os.path.exists(export_directory):
    os.mkdir(export_directory)

print("Creating target distribution")

import numpy as np

import Antenna
import Array

Ntheta=91
Nphi=181

theta=np.linspace(0, 180, Ntheta)
phi=np.linspace(-180, 180, Nphi)

target_antenna = Antenna.Antenna(
    name='Target RHCP',
    theta=theta.copy(),
    phi=phi.copy())
target_antenna.evaluate_as = 'expressions'
target_antenna.evaluation_arguments['expression theta'] = '0.1 - 0.9*1j*((U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta)))'
target_antenna.evaluation_arguments['expression phi'] = '0.1 + 0.9*((U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta)))'
target_antenna.set_orientation(elevation=-90,azimuth=90)
target_antenna.evaluate()

print("Creating working array")

antennas = [antennas['hfss_yagi2EL'].copy() for a in range(N)]
working_array = Array.Array(
    name='Initial array',
    theta=theta.copy(),
    phi=phi.copy(),
    antennas=antennas
    )
for i in range(len(working_array.antennas)):
    working_array.antennas[i].set_position(
        # x=2*(np.random.rand()-0.5)*len(working_array.antennas),
        # y=2*(np.random.rand()-0.5)*len(working_array.antennas),
        x = 0,
        y = i*0.5,
        z=0)
    working_array.antennas[i].set_orientation(
        elevation=-90,
        azimuth=0,
        roll=90*(np.cos(np.pi*i)/2+0.5))
    working_array.antennas[i].set_current(
        magnitude = 1,
        phase = 90*(np.cos(np.pi*i)/2+0.5))
working_array.evaluate()

print("Exporting initial state")

import Scripts.ExportResults

Scripts.ExportResults.run([
    working_array,
    ], export_directory,
    fields=[
        'F',
        'Fref',
        'Fcross',
        'Frhcp',
        'Flhcp'
        ])

print("Optimizing")

def cost_function(target, result):
    total_cost = np.abs(np.abs(target.Frhcp)-np.abs(result.Frhcp)).sum()
    total_cost += np.abs(np.abs(target.Flhcp)-np.abs(result.Flhcp)).sum()
    return total_cost

optim = Optimization.Optimization(
    target_antenna=target_antenna,
    working_array=working_array,
    x_map = [
        dict(
            antenna=working_array.antennas[i],
            variables = [
                # 'x',
                # 'y',
                # 'elevation',
                # 'azimuth',
                # 'roll',
                'current magnitude',
                # 'current phase',
                ],
            ) for i in range(len(working_array.antennas))
        ],
    cost_function=cost_function,
    disp=True,
    # method='Nelder-Mead',
    # tol = 1,
    # options=dict(maxiter=300),
    )
result = optim.run()
# for k in optim.best_results.keys():
    # result = optim.best_results[k]
filename = os.path.join(export_directory,'Optimization with {N} antennas and cost {cost}.dat'.format(N=len(optim.working_array.antennas), cost=optim.result.fun))
with open(filename, mode='wb') as f:
    # result.working_array.listeners = []
    # pickle.dump(result.working_array, f)
    pickle.dump(optim, f)

working_array = optim.working_array
print(result)

target_antenna.name = 'Target Antenna'
working_array.name = 'Result Array'

print("Exporting results")

Scripts.ExportResults.run([
    target_antenna,
    working_array,
    ], export_directory,
    fields=[
        'F',
        'Fref',
        'Fcross',
        'Frhcp',
        'Flhcp'
        ])

print("Starting visualization")

import App
import ResultFrame
import Result

app = App.App(antennas=[target_antenna, working_array])
try:
    Ntheta = 91
    Nphi = 181
    field = 'F'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
    Result.Result(tab=tab,
                  title='Result',
                  name='Result F',
                  antenna=working_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  column=1,row=1,
                  Ntheta=Ntheta,
                  Nphi=Nphi)
    Result.Result(tab=tab,
                  title='Target',
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
    
    field = 'Frhcp'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
    Result.Result(tab=tab,
                  title='Result',
                  name='Result RHCP',
                  antenna=working_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  column=1,row=1,
                  Ntheta=Ntheta,
                  Nphi=Nphi)
    Result.Result(tab=tab,
                  title='Target',
                  name='Target RHCP',
                  antenna=target_antenna,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  column=2,row=1,
                  Ntheta=Ntheta,
                  Nphi=Nphi)
    app.add_tab(tab)
    
    field = 'Flhcp'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
    Result.Result(tab=tab,
                  title='Result',
                  name='Result LHCP',
                  antenna=working_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  column=1,row=1,
                  Ntheta=Ntheta,
                  Nphi=Nphi)
    Result.Result(tab=tab,
                  title='Target',
                  name='Target LHCP',
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