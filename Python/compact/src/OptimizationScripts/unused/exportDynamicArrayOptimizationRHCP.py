#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 22:32:47 2023

@author: vitinho
"""

import sys
import os
path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, path)

import pickle

import matplotlib.pyplot as plt
plt.close('all')

import numpy as np

print("Loading antennas")

import Scripts.AntennasLoaders.LoadHFSSYagis
antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(Ntheta=91, Nphi=91)

antenna_1 = antennas['hfss_yagi1EL']
antenna_2 = antennas['hfss_yagi2EL']
antenna_3 = antennas['hfss_yagi3EL']
antenna_4 = antennas['hfss_yagi4EL']

antenna_1.set_orientation(elevation=-90)
antenna_1.evaluate()
antenna_2.set_orientation(elevation=-90)
antenna_2.evaluate()
antenna_3.set_orientation(elevation=-90)
antenna_3.evaluate()
antenna_4.set_orientation(elevation=-90)
antenna_4.evaluate()

print("Loading export results directory")

export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/OptimizationLinear'
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

# target_antenna = Array.Array(name='Target Cross',
#                             theta=theta.copy(),
#                             phi=phi.copy(),
#                             antennas=[
#                                 antennas['hfss_yagi2EL'].copy(),
#                                 antennas['hfss_yagi2EL'].copy(),
#                                 antennas['hfss_yagi2EL'].copy(),
#                           ])
# target_antenna.antennas[0].set_position(x=0,y=0,z=0)
# target_antenna.antennas[0].set_orientation(elevation=90,azimuth=90)
# target_antenna.antennas[1].set_position(x=0,y=0.5,z=0)
# target_antenna.antennas[1].set_orientation(elevation=90,azimuth=0)
# target_antenna.antennas[2].set_position(x=0,y=1,z=0)
# target_antenna.antennas[2].set_orientation(elevation=90,azimuth=120)
# target_antenna.evaluate()

target_antenna = Antenna.Antenna(
    name='Target RHCP',
    theta=theta.copy(),
    phi=phi.copy())
target_antenna.evaluate_as = 'expressions'
target_antenna.evaluation_arguments['expression theta'] = '0.1 + 0.9*1j*((U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta)))'
target_antenna.evaluation_arguments['expression phi'] = '0.1 + 0.9*((U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta)))'
target_antenna.set_orientation(elevation=-90,azimuth=90)
target_antenna.evaluate()

import DynamicOptimization

def cost_function(target, result):
    total_cost = np.abs(np.abs(target.Frhcp)-np.abs(result.Frhcp)).sum()
    total_cost += np.abs(np.abs(target.Flhcp)-np.abs(result.Flhcp)).sum()
    return total_cost

optim = DynamicOptimization.DynamicOptimization(
    cost_function = cost_function,
    available_antennas = [
        # antenna_1,
        # antenna_2,
        antenna_3,
        antenna_4
        ],
    target_antenna = target_antenna,
    variables=[
        'elevation',
        'azimuth',
        'x',
        'y',
        # 'z',
        'current magnitude',
        'current phase',
        ],
    N_start = 2,
    N_stop = 3,
    # method = 'L-BFGS-B'
    )

# try:
optim.run()
# finally:
#     for k in optim_theta.best_results.keys():
#         result = optim_theta.best_results[k]
#         filename = os.path.join('Optimization Results Theta','best array with {N} antenna and cost {cost}.dat'.format(N=k, cost=result.cost))
#         with open(filename, mode='wb') as f:
#             pickle.dump(result.working_array, f)

export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/OptimizationCross'
if not os.path.exists(export_directory):
    os.mkdir(export_directory)

import Scripts.ExportResults

result_array = optim.best_overall_result.working_array
result = optim.best_overall_result.result
print('final cost: {}'.format(optim.best_overall_result.cost))
print('working theta array have {N} antennas:'.format(N=len(result_array.antennas)))
for i in range(len(result_array.antennas)):
    antenna = result_array.antennas[i]
    print('\tantenna {i}: '.format(i=i) + antenna.name)
    print('\t\televation: {e}'.format(e=antenna.elevation))
    print('\t\tazimuth: {a}'.format(a=antenna.azimuth))
    print('\t\troll: {a}'.format(a=antenna.roll))
    print('\t\tx: {x}'.format(x=antenna.x))
    print('\t\ty: {y}'.format(y=antenna.y))
    print('\t\tz: {z}'.format(z=antenna.z))
    print('\t\tcurrent magnitude: {magnitude}'.format(magnitude=antenna.current_mag))
    print('\t\tcurrent phase: {phase}'.format(phase=antenna.current_phase))

# os.system('shutdown /h')

print(result)

target_antenna.name = 'Target Antenna'
result_array.name = 'Result Array'

print("Exporting results")

Scripts.ExportResults.run([
    target_antenna,
    result_array,
    ], export_directory)

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
    
    field = 'Frhcp'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
    Result.Result(tab=tab,
                  title='',
                  name='Result RCHP',
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
    
    field = 'Flhcp'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
    Result.Result(tab=tab,
                  title='',
                  name='Result LHCP',
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
                  name='Target LCHP',
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