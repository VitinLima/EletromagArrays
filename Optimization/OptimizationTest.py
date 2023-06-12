#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 22:42:28 2023

@author: vitinho
"""

import sys
import os
path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, path)

import numpy as np
import pickle

# import Antenna
import Array
import Analysis
import Optimization

import Scripts.AntennasLoaders.LoadHFSSYagis

antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(Ntheta=91, Nphi=91, elevation=-90)
export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/Optimization Results Test'
if not os.path.exists(export_directory):
    os.mkdir(export_directory)

theta=np.linspace(0, 180, 91)
phi=np.linspace(-180, 180, 91)

F = Analysis.Analysis(name='F',expression='F')
Fref = Analysis.Analysis(name='Fref',expression='Fref',color_expression='')
Fcross = Analysis.Analysis(name='Fcross',expression='Fcross',color_expression='')
Frhcp = Analysis.Analysis(name='Frhcp',expression='Frhcp',color_expression='')
Flhcp = Analysis.Analysis(name='Flhcp',expression='Flhcp',color_expression='')
    
target_antenna = Array.Array(
    theta=theta,
    phi=phi,
    antennas=[antennas['hfss_yagi2EL'].copy()]
    )
target_antenna.antennas[0].set_orientation(elevation=-45,azimuth=45)
target_antenna.evaluate()

optimizing_array = Array.Array(
    theta=theta,
    phi=phi,
    antennas=[antennas['hfss_yagi2EL'].copy()]
    )
optimizing_array.antennas[0].set_orientation(elevation=-45,azimuth=45)

# weight_mask = np.ones(target_distribution_theta.shape)
# weight_mask[target_distribution_theta.mesh_theta>np.pi/2] = 0.5

x_map = []
x_map.append(dict(
    antenna=optimizing_array.antennas[0],
    variables=[
        'elevation',
        'azimuth'
        ]
    ))
optim = Optimization.Optimization(x_map=x_map,
                     method='L-BFGS-B',
                     working_array=optimizing_array,
                     target_antenna=target_antenna,
                     analyses=[Fref, Fcross],
                     disp=True)

try:
    optim.run()
finally:
    print('\tcost: {}'.format(optim.cost))
    # for k in optim.best_results.keys():
    #     result = optim.best_results[k]
    #     filename = os.path.join(export_directory,'best array with {N} antenna and cost {cost}.dat'.format(N=k, cost=result.cost))
    #     with open(filename, mode='wb') as f:
    #         result.working_array.listeners = []
    #         pickle.dump(result.working_array, f)

# array = optim.best_result.working_array
# print('final cost: {}'.format(optim.best_result.cost))
# print('working rhcp array have {N} antennas:'.format(N=len(array.antennas)))
# for i in range(len(array.antennas)):
#     antenna = array.antennas[i]
#     print('\tantenna {i}: '.format(i=i) + antenna.name)
#     print('\t\televation: {e}'.format(e=antenna.elevation))
#     print('\t\tazimuth: {a}'.format(a=antenna.azimuth))
#     print('\t\troll: {a}'.format(a=antenna.roll))
#     print('\t\tx: {x}'.format(x=antenna.x))
#     print('\t\ty: {y}'.format(y=antenna.y))
#     print('\t\tz: {z}'.format(z=antenna.z))
#     print('\t\tcurrent magnitude: {magnitude}'.format(magnitude=antenna.current_mag))
#     print('\t\tcurrent phase: {phase}'.format(phase=antenna.current_phase))

# os.system('shutdown /h')

import App
import ResultFrame
import Result

app = App.App()
try:
    app.add_antenna(optimizing_array)
    app.add_antenna(target_antenna)
    
    app.add_analysis(F)
    app.add_analysis(Fref)
    app.add_analysis(Fcross)
    app.add_analysis(Frhcp)
    app.add_analysis(Flhcp)
    
    field = 'F'
    plot = '3d Polar'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,iy=2)
    Result.Result(tab=tab,
                  title='',
                  name='Array Cross',
                  antenna=optimizing_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  preferred_position=1)
    Result.Result(tab=tab,
                  title='',
                  name='Target Cross',
                  antenna=target_antenna,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  preferred_position=2)
    app.add_tab(tab)
    
    field = 'Fref'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,iy=2)
    Result.Result(tab=tab,
                  title='',
                  name='Array Cross',
                  antenna=optimizing_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  preferred_position=1)
    Result.Result(tab=tab,
                  title='',
                  name='Target Cross',
                  antenna=target_antenna,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  preferred_position=2)
    app.add_tab(tab)
    
    field = 'Fcross'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,iy=2)
    Result.Result(tab=tab,
                  title='',
                  name='Array Cross',
                  antenna=optimizing_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  preferred_position=1)
    Result.Result(tab=tab,
                  title='',
                  name='Target Cross',
                  antenna=target_antenna,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  preferred_position=2)
    app.add_tab(tab)
    
    # Main application loop
    app.mainloop()
except Exception as e:
    # If some error occur, destroy the application to close the window,
    # then show the error
    app.destroy()
    raise e