# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:02:31 2023

@author: 160047412
"""

import os
import pickle
import numpy as np

from Antenna import Antenna
from Array import Array
from Analysis import Analysis

import Optimization

theta=np.linspace(0, 180, 91)
phi=np.linspace(-180, 180, 91)

target_distribution = Antenna(name='Target',
                              theta=theta.copy(),
                              phi=phi.copy())
target_distribution.evaluate_as = 'expressions'
target_distribution.evaluation_arguments['expression theta'] = '(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
target_distribution.evaluation_arguments['expression phi'] = '1j*(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
target_distribution.set_orientation(elevation=-90,azimuth=90)
target_distribution.evaluate()

F = Analysis(name='F',expression='F')
Ftheta = Analysis(name='Ftheta',expression='Ftheta',color_expression='')
Fphi = Analysis(name='Fphi',expression='Fphi',color_expression='')
Frhcp = Analysis(name='Frhcp',expression='abs(Frhcp)',color_expression='')
Flhcp = Analysis(name='Flhcp',expression='abs(Flhcp)',color_expression='')

weight_mask = np.ones(target_distribution.shape)
weight_mask[target_distribution.mesh_theta>np.pi/2] = 0.5

filename = os.path.join('Optimization Results Theta','best array with 3 antenna and cost 139.7724336651349.dat')
with open(filename, 'rb') as f:
    array_theta = pickle.load(f)

filename = os.path.join('Optimization Results Phi','best array with 3 antenna and cost 199.83945169107284.dat')
with open(filename, 'rb') as f:
    array_phi = pickle.load(f)

array_rhcp = Array(name='Array RHCP',
                   antennas=[array_theta.copy(), array_phi.copy()],
                   theta=theta,phi=phi)
array_rhcp.antennas[1].set_position(y=3)
array_rhcp.antennas[1].set_current(current_phase=-90)
array_rhcp.evaluate()

x_map = []
for antenna in array_rhcp.antennas:
    x_map.append(dict(
        antenna=antenna,
        variables=[
                'elevation',
               # 'azimuth',
                # 'x',
                'y',
               # 'z',
               'current magnitude',
               'current phase',
            ]
        ))
optim = Optimization.Optimization(x_map=x_map,
                     working_array=array_rhcp,
                     target_antenna=target_distribution,
                     method='BFGS',
                     analyses=[Frhcp, Flhcp],
                     weight_mask=weight_mask)
optim.run()

from App import App
from ResultFrame import ResultFrame

app = App()
try:
    app.add_antenna(array_theta)
    app.add_antenna(array_phi)
    # app.add_antenna(target_distribution)
    app.add_antenna(array_rhcp)
    
    app.add_analysis(F)
    app.add_analysis(Ftheta)
    app.add_analysis(Fphi)
    app.add_analysis(Frhcp)
    app.add_analysis(Flhcp)
    
    result_tab = ResultFrame(master=app.tabs,name='Array Theta',
                             antenna=array_theta,analysis=F,
                             plot='2d Polar Patch')
    app.add_result_tab(result_tab)
    
    result_tab = ResultFrame(master=app.tabs,name='Array Phi',
                             antenna=array_phi,analysis=F,
                             plot='2d Polar Patch')
    app.add_result_tab(result_tab)
    
    result_tab = ResultFrame(master=app.tabs,name='Array RHCP',
                             antenna=array_rhcp,analysis=Frhcp,
                             plot='2d Polar Patch')
    app.add_result_tab(result_tab)
    
    # Main application loop
    app.mainloop()
except Exception as e:
    # If some error occur, destroy the application to close the window,
    # then show the error
    app.destroy()
    raise e