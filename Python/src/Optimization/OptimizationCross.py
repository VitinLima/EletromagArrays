# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 18:02:32 2023

@author: Vitinho
"""

import sys
import os
path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, path)

import time
import pickle

import numpy as np

import Antenna
import Analysis
import SpecialOptim

import Scripts.AntennasLoaders.LoadHFSSYagis

Ntheta=91
Nphi=91

antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(Ntheta=Ntheta, Nphi=Nphi, elevation=-90)

export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/OptimizationCross'
if not os.path.exists(export_directory):
    os.mkdir(export_directory)

theta=np.linspace(0, 180, Ntheta)
phi=np.linspace(-180, 180, Nphi)

F = Analysis.Analysis(name='F',expression='F')
Fref = Analysis.Analysis(name='Fref',expression='Fref',color_expression='')
Fcross = Analysis.Analysis(name='Fcross',expression='Fcross',color_expression='')
Frhcp = Analysis.Analysis(name='Frhcp',expression='Frhcp',color_expression='')
Flhcp = Analysis.Analysis(name='Flhcp',expression='Flhcp',color_expression='')
    
target_antenna = Antenna.Antenna(name='Target Cross',
                              theta=theta.copy(),
                              phi=phi.copy())
target_antenna.evaluate_as = 'expressions'
target_antenna.evaluation_arguments['expression theta'] = '0'
target_antenna.evaluation_arguments['expression phi'] = '(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
target_antenna.set_orientation(elevation=-90,azimuth=90)
target_antenna.evaluate()

# weight_mask = np.ones(target_distribution_theta.shape)
# weight_mask[target_distribution_theta.mesh_theta>np.pi/2] = 0.5

optim = SpecialOptim.SpecialOptim(
                     available_antennas = [
                                # antennas['hfss_yagi1EL'],
                                antennas['hfss_yagi2EL'],
                                # antennas['hfss_yagi3EL'],
                                # antennas['hfss_yagi4EL'],
                                # antennas['hfss_yagi1EL_V'],
                                # antennas['hfss_yagi2EL_V'],
                                # antennas['hfss_yagi3EL_V'],
                                # antennas['hfss_yagi4EL_V']
                         ],
                     analyses = [
                            Fref,
                            Fcross,
                         ],
                     # weights=[1],
                     target_antenna = target_antenna,
                     variables=[
                            'elevation',
                            # 'azimuth',
                            # 'roll',
                            # 'x',
                            'y',
                            # 'z',
                            # 'current magnitude',
                            # 'current phase',
                         ],
                     N_start = 1,
                     N_stop = 2,
                     # weight_mask=weight_mask,
                     # method = 'L-BFGS-B',
                      disp=False,
                     )

try:
    start_time = time.time()
    optim.run()
    elapsed_time = time.time()-start_time
finally:
    for k in optim.best_results.keys():
        result = optim.best_results[k]
        filename = os.path.join(export_directory,'best array with {N} antenna and cost {cost}.dat'.format(N=k, cost=result.cost))
        with open(filename, mode='wb') as f:
            result.working_array.listeners = []
            pickle.dump(result.working_array, f)

result_array = optim.best_result.working_array
print('elapsed time was ' + str(elapsed_time))
print('number of evaluations was ' + str(optim.number_of_evaluations))
print('final cost: {}'.format(optim.best_result.cost))
print('final array have {N} antennas:'.format(N=len(result_array.antennas)))
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

import Scripts.ExportResults

target_antenna.name = 'Target Antenna'
result_array.name = 'Result Array'

Scripts.ExportResults.run([
    target_antenna,
    result_array,
    ], export_directory)

# os.system('shutdown /h')

import App
import ResultFrame
import Result

app = App.App()
try:
    app.add_antenna(result_array)
    app.add_antenna(target_antenna)
    
    app.add_analysis(F)
    app.add_analysis(Fref)
    app.add_analysis(Fcross)
    app.add_analysis(Frhcp)
    app.add_analysis(Flhcp)
    
    field = 'F'
    plot = '2d Polar Patch'
    
    tab = ResultFrame.ResultFrame(master=app.tabs,name=field,iy=2)
    Result.Result(tab=tab,
                  title='',
                  name='Result F',
                  antenna=result_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  preferred_position=1)
    Result.Result(tab=tab,
                  title='',
                  name='Target F',
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
                  name='Result Ref',
                  antenna=result_array,
                  field=field,
                  plot=plot,
                  ticks_flag=False,
                  in_dB=True,
                  preferred_position=1)
    Result.Result(tab=tab,
                  title='',
                  name='Target Ref',
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
                  name='Result Cross',
                  antenna=result_array,
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