#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 22:42:28 2023

@author: Vitinho
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
                     disp=False)

try:
    optim.run()
finally:
    print('\tcost: {}'.format(optim.cost))

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