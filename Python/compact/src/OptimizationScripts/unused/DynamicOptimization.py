# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 01:38:53 2023

@author: Vitinho
"""

import numpy as np
import itertools

import Array
import Optimization

class DynamicOptimization:
    def __init__(self,
                 cost_function,
                 available_antennas,
                 target_antenna,
                 variables=['elevation'],
                 N_start = 1,
                 N_stop = 3,
                 method = 'L-BFGS-B',
                 disp=False,
                 **kw):
        self.cost_function=cost_function
        self.available_antennas=available_antennas
        self.target_antenna=target_antenna
        self.variables=variables
        self.N_start=N_start
        self.N_stop=N_stop
        self.method=method
        self.disp=disp
        self.optimization_arguments=kw
        
        self.best_overall_result = None
    
    def run(self):
        if not self.target_antenna.ok:
            self.target_antenna.evaluate()
        
        theta=self.target_antenna.theta.copy()
        phi=self.target_antenna.phi.copy()
        
        self.best_results = dict()
        
        self.number_of_optimizations = 0
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
                    antenna.set_position(y=np.random.rand()*0.15+i*0.5)
                    x_map.append(dict(
                        antenna=antenna,
                        variables=self.variables
                        ))
                
                optim = Optimization.Optimization(
                    cost_function=self.cost_function,
                    x_map=x_map,
                    method=self.method,
                    working_array=working_array,
                    target_antenna=self.target_antenna,
                    disp=self.disp,
                    # **self.kw,
                    )
                
                optim.run()
                
                self.number_of_optimizations += 1
                self.number_of_evaluations += optim.number_of_evaluations
                print('\tcost: {}'.format(optim.cost))
                
                if r in self.best_results.keys():
                    if optim.lowest_cost < self.best_results[r].cost:
                        self.best_results[r] = optim
                else:
                    self.best_results[r] = optim
                
                if self.best_overall_result is None:
                    self.best_overall_result = optim
                elif optim.lowest_cost < self.best_overall_result.cost:
                    self.best_overall_result = optim