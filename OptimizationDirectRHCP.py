# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 22:16:23 2023

@author: 160047412
"""

import numpy as np
import scipy.optimize
import itertools

from Array import Array
from Optimization import Optimization

class MultiAntennaOptimization:
    def __init__(self,
                 available_antennas = None,
                 analyses = None,
                 weights = None,
                 target_antenna = None,
                 variables=['elevation'],
                 N_start = 2,
                 N_stop = 2,
                 method = 'L-BFGS-B',
                 weight_mask = 1,
                 disp=False):
        self.available_antennas=available_antennas
        self.analyses=analyses
        self.weights=weights
        self.target_antenna=target_antenna
        self.variables=variables
        self.N_start=N_start
        self.N_stop=N_stop
        self.method=method
        self.weight_mask=weight_mask
        self.disp=disp
    
    def run(self):
        if self.available_antennas==None:
            return
        if self.analyses==None:
            return
        if self.target_antenna==None:
            return
        
        self.best_result = None
        if not self.target_antenna.ok:
            self.target_antenna.evaluate()
        
        theta=self.target_antenna.theta.copy()
        phi=self.target_antenna.phi.copy()
        
        self.best_results = dict()
        
        for r in range(self.N_start,self.N_stop+1):
            for iterating_antennas in itertools.product(self.available_antennas, repeat=r):
                antennas = [antenna.copy() for antenna in iterating_antennas]
                working_array = Array(theta=theta,phi=phi,
                                      antennas=antennas,
                                      y_mirror=True,
                                      current_mirror=True,
                                      azimuth_symmetry=True)
                print('optimizing with {} antennas:'.format(r))
                print('\t'+str([antenna.name for antenna in antennas]))
                x_map = []
                for i in range(len(antennas)):
                    antenna = antennas[i]
                    antenna.set_position(y=0.25+i*0.5)
                    x_map.append(dict(
                        antenna=antenna,
                        variables=self.variables
                        ))
                optim = Optimization(x_map=x_map,
                                     method=self.method,
                                     working_array=working_array,
                                     target_antenna=self.target_antenna,
                                     analyses=self.analyses,
                                     weight_mask=self.weight_mask,
                                     disp=self.disp)
                optim.run()
                print('\tcost: {}'.format(optim.cost))
                if r in self.best_results.keys():
                    if optim.cost < self.best_results[r].cost:
                        self.best_results[r] = optim
                else:
                    self.best_results[r] = optim
                if self.best_result is None:
                    self.best_result = optim
                elif optim.cost < self.best_result.cost:
                    self.best_result = optim

if __name__=='__main__':
    import os
    import pickle

    from Antenna import Antenna
    from Analysis import Analysis
    import LoadDefaultAntennas
    
    theta=np.linspace(0, 180, 91)
    phi=np.linspace(-180, 180, 91)
    antenna_1_H,antenna_2_H,antenna_3_H,antenna_4_H,antenna_1_V,antenna_2_V,antenna_3_V,antenna_4_V = LoadDefaultAntennas.load_default_antennas(elevation=-45)
    
    F = Analysis(name='F',expression='F')
    Ftheta = Analysis(name='Ftheta',expression='Ftheta',color_expression='')
    Fphi = Analysis(name='Fphi',expression='Fphi',color_expression='')
    Frhcp = Analysis(name='Frhcp',expression='Frhcp',color_expression='')
    Flhcp = Analysis(name='Flhcp',expression='Flhcp',color_expression='')
    
    target_distribution_rhcp = Antenna( name='Target rhcp',
                                  theta=theta.copy(),
                                  phi=phi.copy())
    target_distribution_rhcp.evaluate_as = 'expressions'
    target_distribution_rhcp.evaluation_arguments['expression theta'] = '(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
    target_distribution_rhcp.evaluation_arguments['expression phi'] = '1j*(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
    target_distribution_rhcp.set_orientation(elevation=-90,azimuth=90)
    target_distribution_rhcp.evaluate()
    
    target_distribution_lhcp = Antenna( name='Target lhcp',
                                  theta=theta.copy(),
                                  phi=phi.copy())
    target_distribution_lhcp.evaluate_as = 'expressions'
    target_distribution_lhcp.evaluation_arguments['expression theta'] = '(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
    target_distribution_lhcp.evaluation_arguments['expression phi'] = '-1j*(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
    target_distribution_lhcp.set_orientation(elevation=-90,azimuth=90)
    target_distribution_lhcp.evaluate()
    
    # weight_mask = np.ones(target_distribution_rhcp.shape)
    # weight_mask[target_distribution_rhcp.mesh_theta>np.pi/2] = 0.5

    optim = MultiAntennaOptimization(
                         available_antennas = [
                                    # antenna_1_H,
                                    # antenna_2_H,
                                    # antenna_3_H,
                                    antenna_4_H,
                                    # antenna_1_V,
                                    # antenna_2_V,
                                    # antenna_3_V,
                                    antenna_4_V
                             ],
                         analyses = [
                                Frhcp,
                                Flhcp,
                             ],
                         weights=[1,2],
                         target_antenna = target_distribution_rhcp,
                         variables=[
                                'elevation',
                                # 'azimuth',
                                # 'x',
                                'y',
                                # 'z',
                                'current magnitude',
                                # 'current phase',
                             ],
                         N_start = 4,
                         N_stop = 4,
                         # weight_mask=weight_mask,
                         # method = 'L-BFGS-B'
                         )
    
    try:
        optim.run()
    finally:
        for k in optim.best_results.keys():
            result = optim.best_results[k]
            filename = os.path.join('Optimization Results RHCP','best array with {N} antenna and cost {cost}.dat'.format(N=k, cost=result.cost))
            with open(filename, mode='wb') as f:
                pickle.dump(result.working_array, f)
    
    array = optim.best_result.working_array
    print('final cost: {}'.format(optim.best_result.cost))
    print('working theta array have {N} antennas:'.format(N=len(array.antennas)))
    for i in range(len(array.antennas)):
        antenna = array.antennas[i]
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
    
    from App import App
    import ResultFrame
    import Result
    
    app = App()
    try:
        app.add_antenna(antenna_1_H)
        app.add_antenna(antenna_1_V)
        app.add_antenna(antenna_2_H)
        app.add_antenna(antenna_2_V)
        app.add_antenna(antenna_3_H)
        app.add_antenna(antenna_3_V)
        app.add_antenna(antenna_4_H)
        app.add_antenna(antenna_4_V)
        app.add_antenna(array)
        
        app.add_analysis(F)
        app.add_analysis(Ftheta)
        app.add_analysis(Fphi)
        app.add_analysis(Frhcp)
        app.add_analysis(Flhcp)
        
        tab = ResultFrame.ResultFrame(master=app.tabs)
        result = Result.Result(tab=tab,
                        name='Array RHCP',
                        antenna=array,analysis=F,
                        plot='2d Polar Patch')
        app.add_tab(tab)
        
        # Main application loop
        app.mainloop()
    except Exception as e:
        # If some error occur, destroy the application to close the window,
        # then show the error
        app.destroy()
        raise e