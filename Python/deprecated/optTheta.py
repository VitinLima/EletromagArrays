# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 18:20:49 2023

@author: 160047412
"""

import os
import pickle
import numpy as np

from Antenna import Antenna
from Analysis import Analysis

import SpecialOptim

constants = dict()
constants['c'] = 299792458 # m/s
constants['f'] = 433e6 # Hz
constants['eta'] = 120*np.pi
constants['lam'] = constants['c']/constants['f'] # m
constants['w'] = 2*np.pi*constants['f'] # rad/s
constants['k'] = 2*np.pi/constants['lam'] # rad/m

theta=np.linspace(0, 180, 91)
phi=np.linspace(-180, 180, 91)
antennas_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'

isotropic = Antenna(constants,name='Ideal isotropic antenna',
                    theta=theta.copy(),
                    phi=phi.copy())
isotropic.set_evaluation_method('isotropic')
isotropic.evaluation_arguments['isotropic on'] = 'theta'
isotropic.evaluate()

dipole = Antenna(constants,name='Ideal dipole',
                 theta=theta.copy(),
                 phi=phi.copy())
dipole.evaluate()

target_distribution_theta = Antenna(constants, name='Project target',
                              theta=theta.copy(),
                              phi=phi.copy())
target_distribution_theta.evaluate_as = 'expressions'
target_distribution_theta.evaluation_arguments['expression theta'] = '(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
target_distribution_theta.evaluation_arguments['expression phi'] = '0'
target_distribution_theta.set_orientation(elevation=-90,azimuth=90)
target_distribution_theta.evaluate()

antenna_path = os.path.join(antennas_dir, 'antenna-Dipole.csv')
antenna_1 = Antenna(constants,name='Dipole antenna',
                    theta=theta.copy(),
                    phi=phi.copy())
antenna_1.set_evaluation_method('load file')
antenna_1.evaluation_arguments['file path'] = antenna_path
antenna_1.evaluation_arguments['load mesh from file'] = False
antenna_1.set_orientation(elevation=0,azimuth=0)
antenna_1.evaluate()

antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-2Elements.csv')
antenna_2 = Antenna(constants,name='Yagi 2 elements',
                    theta=theta.copy(),
                    phi=phi.copy())
antenna_2.set_evaluation_method('load file')
antenna_2.evaluation_arguments['file path'] = antenna_path
antenna_2.evaluation_arguments['load mesh from file'] = False
antenna_2.set_orientation(elevation=-90)
antenna_2.evaluate()

antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-3Elements.csv')
antenna_3 = Antenna(constants,name='Yagi 3 elements',
                    theta=theta.copy(),
                    phi=phi.copy())
antenna_3.set_evaluation_method('load file')
antenna_3.evaluation_arguments['file path'] = antenna_path
antenna_3.evaluation_arguments['load mesh from file'] = False
antenna_3.set_orientation(elevation=-90)
antenna_3.evaluate()

antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-4Elements.csv')
antenna_4 = Antenna(constants,name='Yagi 4 elements',
                    theta=theta.copy(),
                    phi=phi.copy())
antenna_4.set_evaluation_method('load file')
antenna_4.evaluation_arguments['file path'] = antenna_path
antenna_4.evaluation_arguments['load mesh from file'] = False
antenna_4.set_orientation(elevation=-90)
antenna_4.evaluate()

F = Analysis(name='F',expression='F')
Ftheta = Analysis(name='Ftheta',expression='Ftheta',color_expression='')
Fphi = Analysis(name='Fphi',expression='Fphi',color_expression='')
angleFtheta = Analysis(name='phase Ftheta',expression='Ftheta',color_expression='angle(Ftheta)')
angleFphi = Analysis(name='phase Fphi',expression='Fphi',color_expression='angle(Fphi)')

weight_mask = np.ones(target_distribution_theta.shape)
weight_mask[target_distribution_theta.mesh_theta>np.pi/2] = 0.5

optim_theta = SpecialOptim.SpecialOptim(constants=constants,
                     available_antennas = [
                         antenna_1,
                         antenna_2,
                         # antenna_3,
                         # antenna_4
                         ],
                     analyses = [
                         Ftheta,
                         Fphi,
                         ],
                     # weights=[1],
                     target_antenna = target_distribution_theta,
                     variables=[
                         'elevation',
                         # 'azimuth',
                         # 'x',
                         # 'y',
                         # 'z',
                        # 'current magnitude',
                        # 'current phase',
                         ],
                     N_start = 2,
                     N_stop = 2,
                     weight_mask=weight_mask,
                     method = 'L-BFGS-B'
                     )

try:
    optim_theta.run()
finally:
    for k in optim_theta.best_results.keys():
        result = optim_theta.best_results[k]
        filename = os.path.join('Optimization Results Theta','best array with {N} antenna and cost {cost}.dat'.format(N=k, cost=result.cost))
        with open(filename, mode='wb') as f:
            pickle.dump(result.working_array, f)

array_theta = optim_theta.best_result.working_array
print('final cost: {}'.format(optim_theta.best_result.cost))
print('working theta array have {N} antennas:'.format(N=len(array_theta.antennas)))
for i in range(len(array_theta.antennas)):
    antenna = array_theta.antennas[i]
    print('\tantenna {i}: '.format(i=i) + antenna.name)
    print('\t\televation: {e}'.format(e=antenna.elevation))
    print('\t\tazimuth: {a}'.format(a=antenna.azimuth))
    print('\t\troll: {a}'.format(a=antenna.roll))
    print('\t\tx: {x}'.format(x=antenna.x))
    print('\t\ty: {y}'.format(y=antenna.y))
    print('\t\tz: {z}'.format(z=antenna.z))
    print('\t\tcurrent magnitude: {magnitude}'.format(magnitude=antenna.current_mag))
    print('\t\tcurrent phase: {phase}'.format(phase=antenna.current_phase))

from App import App
from ResultFrame import ResultFrame

app = App()
try:
    app.add_antenna(array_theta)
    app.add_antenna(target_distribution_theta)
    
    app.add_analysis(F)
    app.add_analysis(Ftheta)
    app.add_analysis(Fphi)
    app.add_analysis(angleFtheta)
    app.add_analysis(angleFphi)
    
    result_tab = ResultFrame(master=app.tabs,name='Array Theta',
                             antenna=array_theta,analysis=F,
                             plot='2d Polar Patch')
    app.add_result_tab(result_tab)
    
    result_tab = ResultFrame(master=app.tabs,name='target theta',
                             antenna=target_distribution_theta,analysis=F,
                             plot='2d Polar Patch')
    app.add_result_tab(result_tab)
    
    # Main application loop
    app.mainloop()
except Exception as e:
    # If some error occur, destroy the application to close the window,
    # then show the error
    app.destroy()
    raise e