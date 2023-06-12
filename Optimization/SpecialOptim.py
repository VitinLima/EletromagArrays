# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 01:38:53 2023

@author: Vitinho
"""

import numpy as np
import scipy.optimize
import itertools

import Array
import Optimization

class SpecialOptim:
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
        
        self.number_of_evaluations = 0
        for r in range(self.N_start,self.N_stop+1):
            for iterating_antennas in itertools.product(self.available_antennas, repeat=r):
                antennas = [antenna.copy() for antenna in iterating_antennas]
                working_array = Array.Array(theta=theta,phi=phi,
                                      antennas=antennas)
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
                optim = Optimization.Optimization(x_map=x_map,
                                     method=self.method,
                                     working_array=working_array,
                                     target_antenna=self.target_antenna,
                                     analyses=self.analyses,
                                     weight_mask=self.weight_mask,
                                     weights=self.weights,
                                     disp=self.disp)
                optim.run()
                self.number_of_evaluations += optim.number_of_evaluations
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

    from EletromagArrays.Package.Antenna import Antenna
    from EletromagArrays.Package.Analysis import Analysis
    import LoadDefaultAntennas
    
    theta=np.linspace(0, 180, 91)
    phi=np.linspace(-180, 180, 91)
    antenna_1,antenna_2,antenna_3,antenna_4 = LoadDefaultAntennas.load_default_antennas()
    
    F = Analysis.Analysis(name='F',expression='F')
    Ftheta = Analysis(name='Ftheta',expression='Ftheta',color_expression='')
    Fphi = Analysis.Analysis(name='Fphi',expression='Fphi',color_expression='')
    Frhcp = Analysis.Analysis(name='Frhcp',expression='Frhcp',color_expression='')
    Flhcp = Analysis.Analysis(name='Flhcp',expression='Flhcp',color_expression='')
    
    target_distribution_theta = Antenna.Antenna( name='Target theta',
                                  theta=theta.copy(),
                                  phi=phi.copy())
    target_distribution_theta.evaluate_as = 'expressions'
    target_distribution_theta.evaluation_arguments['expression theta'] = '(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
    target_distribution_theta.evaluation_arguments['expression phi'] = '0'
    target_distribution_theta.set_orientation(elevation=-90,azimuth=90)
    target_distribution_theta.evaluate()
    
    # weight_mask = np.ones(target_distribution_theta.shape)
    # weight_mask[target_distribution_theta.mesh_theta>np.pi/2] = 0.5

    optim_theta = SpecialOptim(
                         available_antennas = [
                                    # antenna_1,
                                    # antenna_2,
                                    antenna_3,
                                    antenna_4
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
                                'y',
                                # 'z',
                                'current magnitude',
                                'current phase',
                             ],
                         N_start = 2,
                         N_stop = 4,
                         # weight_mask=weight_mask,
                         # method = 'L-BFGS-B'
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
    
    antenna_1.set_orientation(roll=90)
    antenna_1.evaluate()
    antenna_2.set_orientation(roll=90)
    antenna_2.evaluate()
    antenna_3.set_orientation(roll=90)
    antenna_3.evaluate()
    antenna_4.set_orientation(roll=90)
    antenna_4.evaluate()
    
    target_distribution_phi = Antenna( name='Target phi',
                                  theta=theta.copy(),
                                  phi=phi.copy())
    target_distribution_phi.evaluate_as = 'expressions'
    target_distribution_phi.evaluation_arguments['expression theta'] = '0'
    target_distribution_phi.evaluation_arguments['expression phi'] = '(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
    target_distribution_phi.set_orientation(elevation=-90,azimuth=90)
    target_distribution_phi.evaluate()

    optim_phi = SpecialOptim(
                         available_antennas = [
                                    # antenna_1,
                                    # antenna_2,
                                    antenna_3,
                                    antenna_4
                             ],
                         analyses = [
                                Ftheta,
                                Fphi,
                             ],
                         # weights=[1],
                         target_antenna = target_distribution_phi,
                         variables=[
                                'elevation',
                                # 'azimuth',
                                'x',
                                # 'y',
                                # 'z',
                                'current magnitude',
                                'current phase',
                             ],
                         N_start = 2,
                         N_stop = 2,
                         # weight_mask=weight_mask,
                         method = 'L-BFGS-B'
                         )

    try:
        optim_phi.run()
    finally:
        for k in optim_phi.best_results.keys():
            result = optim_phi.best_results[k]
            filename = os.path.join('Optimization Results Phi','best array with {N} antenna and cost {cost}.dat'.format(N=k, cost=result.cost))
            with open(filename, mode='wb') as f:
                pickle.dump(result.working_array, f)

    array_phi = optim_phi.best_result.working_array
    print('final cost: {}'.format(optim_phi.best_result.cost))
    print('working phi array have {N} antennas:'.format(N=len(array_phi.antennas)))
    for i in range(len(array_phi.antennas)):
        antenna = array_phi.antennas[i]
        print('\tantenna {i}: '.format(i=i) + antenna.name)
        print('\t\televation: {e}'.format(e=antenna.elevation))
        print('\t\tazimuth: {a}'.format(a=antenna.azimuth))
        print('\t\troll: {a}'.format(a=antenna.roll))
        print('\t\tx: {x}'.format(x=antenna.x))
        print('\t\ty: {y}'.format(y=antenna.y))
        print('\t\tz: {z}'.format(z=antenna.z))
        print('\t\tcurrent magnitude: {magnitude}'.format(magnitude=antenna.current_mag))
        print('\t\tcurrent phase: {phase}'.format(phase=antenna.current_phase))
    
    array_rhcp = Array(name='Array RHCP',
                       antennas=[array_theta.copy(), array_phi.copy()],
                       theta=theta.copy(),phi=phi.copy())
    array_rhcp.antennas[1].set_position(y=0.5)
    array_rhcp.antennas[1].set_current(current_phase=-90)
    array_rhcp.evaluate()

    # x_map = []
    # for antenna in array_rhcp.antennas:
    #     x_map.append(dict(
    #         antenna=antenna,
    #         variables=[
    #                 # 'elevation',
    #                 # 'azimuth',
    #                 # 'roll',
    #                 # 'x',
    #                 # 'y',
    #                 # 'z',
    #                 'current magnitude',
    #                 'current phase',
    #             ]
    #         ))
        
    # target_distribution_rhcp = Antenna( name='Target RHCP',
    #                               theta=theta.copy(),
    #                               phi=phi.copy())
    # target_distribution_rhcp.evaluate_as = 'expressions'
    # target_distribution_rhcp.evaluation_arguments['expression theta'] = '(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
    # target_distribution_rhcp.evaluation_arguments['expression phi'] = '1j*(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
    # target_distribution_rhcp.set_orientation(elevation=-90,azimuth=90)
    # target_distribution_rhcp.evaluate()
    
    # optim_rhcp = Optimization(x_map=x_map,
    #                      working_array=array_rhcp,
    #                      target_antenna=target_distribution_rhcp,
    #                      # method='L_BFGS-',
    #                      analyses=[Frhcp, Flhcp],
    #                      # weight_mask=weight_mask
    #                      )
    # optim_rhcp.run()
    
    # os.system('shutdown /h')
    
    from EletromagArrays.Package.App import App
    from EletromagArrays.Package.Results.ResultFrame import ResultFrame
    
    app = App.App()
    try:
        app.add_antenna(array_theta)
        app.add_antenna(array_phi)
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