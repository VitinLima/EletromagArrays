# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 21:55:18 2023

@author: 160047412
"""

import numpy as np
import os
import pickle

import Antenna
import Analysis
import SpecialOptim
import LoadDefaultAntennas

theta=np.linspace(0, 180, 91)
phi=np.linspace(-180, 180, 91)
antenna_1_H,antenna_2_H,antenna_3_H,antenna_4_H,antenna_1_V,antenna_2_V,antenna_3_V,antenna_4_V = LoadDefaultAntennas.load_default_antennas()

F = Analysis.Analysis(name='F',expression='F')
Ftheta = Analysis.Analysis(name='Ftheta',expression='Ftheta',color_expression='')
Fphi = Analysis.Analysis(name='Fphi',expression='Fphi',color_expression='')
Frhcp = Analysis.Analysis(name='Frhcp',expression='Frhcp',color_expression='')
Flhcp = Analysis.Analysis(name='Flhcp',expression='Flhcp',color_expression='')
    
target_distribution_theta = Antenna.Antenna(name='Target Phi',
                              theta=theta.copy(),
                              phi=phi.copy())
target_distribution_theta.evaluate_as = 'expressions'
target_distribution_theta.evaluation_arguments['expression theta'] = '(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
target_distribution_theta.evaluation_arguments['expression phi'] = '0'
target_distribution_theta.set_orientation(elevation=-90,azimuth=90)
target_distribution_theta.evaluate()

# weight_mask = np.ones(target_distribution_theta.shape)
# weight_mask[target_distribution_theta.mesh_theta>np.pi/2] = 0.5

optim_theta = SpecialOptim.SpecialOptim(
                     available_antennas = [
                                # antenna_1_H,
                                antenna_2_H,
                                antenna_3_H,
                                antenna_4_H
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
                            # 'roll',
                            # 'x',
                            # 'y',
                            # 'z',
                            # 'current magnitude',
                            # 'current phase',
                         ],
                     N_start = 1,
                     N_stop = 3,
                     # weight_mask=weight_mask,
                     # method = 'L-BFGS-B',
                     # disp=True,
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

# os.system('shutdown /h')

import App
import ResultFrame

app = App.App()
try:
    app.add_antenna(array_theta)
    app.add_antenna(target_distribution_theta)
    
    app.add_analysis(F)
    app.add_analysis(Ftheta)
    app.add_analysis(Fphi)
    app.add_analysis(Frhcp)
    app.add_analysis(Flhcp)
    
    result_tab = ResultFrame.ResultFrame(master=app.tabs,name='Array Theta',
                             antenna=array_theta,analysis=F,
                             plot='2d Polar Patch')
    app.add_result_tab(result_tab)
    
    # Main application loop
    app.mainloop()
except Exception as e:
    # If some error occur, destroy the application to close the window,
    # then show the error
    app.destroy()
    raise e