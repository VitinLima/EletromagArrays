# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 15:08:48 2023

@author: Vitinho
"""

import time
import numpy as np
import scipy.optimize

class Optimization:
    methods = [
        'Nelder-Mead',
        'Powell',
        'CG',
        'BFGS',
        'Newton-CG',
        'L-BFGS-B',
        'TNC',
        'COBYLA',
        'SLSQP',
        'trust-ngc',
        'trust-exact',
        'trust-krylov'
        ]
    def __init__(self,
                 cost_function,
                 x_map=None,
                 name='new optimization',
                 method='L-BFGS-B',
                 working_array=None,target_antenna=None,
                 # analyses=None,weights=None,
                 weight_mask=1,
                 options={
                     # 'disp':True,
                     'eps':0.01,
                     'gtol':0.1,
                     'xrtol':0.1,
                     'maxiter':30
                     },
                 disp=False):
        self.cost_function=cost_function
        self.name=name
        self.method=method
        self.working_array=working_array
        self.target_antenna=target_antenna
        self.x_map=x_map
        self.options=options
        self.disp=disp
        
        self.sensitivity_x = 1
        self.sensitivity_y = 1
        self.sensitivity_z = 1
        
        self.result = None
        self.lowest_cost = None
        self.lowest_x = None
        
        self.state = 'up to date'
        self.listeners = []
    
    def assert_variables(self, x):
        for entry,x_val in zip(self.working_x_map,x):
            entry['v_cb'](entry['antenna'],x_val)
            entry['antenna'].ok = False
        
        self.working_array.local_field_flag = True
        self.working_array.ok = False
        self.working_array.evaluate()
        self.number_of_evaluations += 1
        
    def cost_function_helper(self, x, *args):
        self.assert_variables(x)
        
        self.cost = self.cost_function(self.target_antenna, self.working_array)
        if self.disp:
            print('evaluating with ' + str(x) + ' cost ' + str(self.cost))
        
        if self.lowest_cost is None:
            self.lowest_cost = self.cost
            self.lowest_x = x
        elif self.cost < self.lowest_cost:
            self.lowest_cost = self.cost
            self.lowest_x = x
        return self.cost
    
    def run(self):
        if not self.target_antenna.ok:
            self.target_antenna.evaluate()
        self.start_time = time.time()
        
        self.working_x_map = []
        x=[]
        bounds=[]
        for entry in self.x_map:
            antenna = entry['antenna']
            for variable in entry['variables']:
                if variable=='elevation':
                    v_cb=self.set_elevation
                    x.append((antenna.elevation/180)+0.5)
                    bounds.append((0.0,1.0))
                elif variable=='azimuth':
                    v_cb=self.set_azimuth
                    x.append((antenna.azimuth/360)+0.5)
                    bounds.append((0.0,1.0))
                elif variable=='roll':
                    v_cb=self.set_roll
                    x.append((antenna.roll/360)+0.5)
                    bounds.append((0.0,1.0))
                elif variable=='x':
                    v_cb=self.set_x
                    x.append(antenna.x/self.sensitivity_x)
                    bounds.append((None,None))
                elif variable=='y':
                    v_cb=self.set_y
                    x.append(antenna.y/self.sensitivity_y)
                    bounds.append((None,None))
                elif variable=='z':
                    v_cb=self.set_z
                    x.append(antenna.z/self.sensitivity_z)
                    bounds.append((None,None))
                elif variable=='current magnitude':
                    v_cb=self.set_current_magnitude
                    x.append(antenna.current_magnitude)
                    bounds.append((0.0,None))
                elif variable=='current phase':
                    v_cb=self.set_current_phase
                    x.append((antenna.current_phase/360)+0.5)
                    bounds.append((0.0,1.0))
                self.working_x_map.append(dict(
                    antenna=antenna,
                    v_cb=v_cb
                    ))
        self.number_of_evaluations = 0
        self.result = scipy.optimize.minimize(fun=self.cost_function_helper,x0=np.array(x),
                                    method=self.method,
                                    bounds=bounds,
                                    options=self.options)
        self.cost = self.result.fun
        self.x = self.result.x
        self.assert_variables(self.result.x)
        
        self.elapsed_time = time.time()-self.start_time
        
        if self.disp:
            print('elapsed time was ' + str(self.elapsed_time))
            print('number of evaluations was ' + str(self.number_of_evaluations))
            print('final cost: {}'.format(self.result.fun))
            print('final array have {N} antennas:'.format(N=len(self.working_array.antennas)))
            for i in range(len(self.working_array.antennas)):
                antenna = self.working_array.antennas[i]
                print('\tantenna {i}: '.format(i=i) + antenna.name)
                print('\t\televation: {e}'.format(e=antenna.elevation))
                print('\t\tazimuth: {a}'.format(a=antenna.azimuth))
                print('\t\troll: {a}'.format(a=antenna.roll))
                print('\t\tx: {x}'.format(x=antenna.x))
                print('\t\ty: {y}'.format(y=antenna.y))
                print('\t\tz: {z}'.format(z=antenna.z))
                print('\t\tcurrent magnitude: {magnitude}'.format(magnitude=antenna.current_magnitude))
                print('\t\tcurrent phase: {phase}'.format(phase=antenna.current_phase))
        
        return self.result
    
    def set_elevation(self,antenna,x):
        antenna.set_orientation(elevation=(x-0.5)*180)
    
    def set_azimuth(self,antenna,x):
        antenna.set_orientation(azimuth=(x-0.5)*360)
    
    def set_roll(self,antenna,x):
        antenna.set_orientation(roll=(x-0.5)*360)
    
    def set_x(self,antenna,x):
        antenna.set_position(x=self.sensitivity_x*x)
    
    def set_y(self,antenna,y):
        antenna.set_position(y=self.sensitivity_y*y)
    
    def set_z(self,antenna,z):
        antenna.set_position(z=self.sensitivity_z*z)
    
    def set_current_magnitude(self,antenna,magnitude):
        antenna.set_current(magnitude=magnitude)
    
    def set_current_phase(self,antenna,phase):
        antenna.set_current(phase=(phase-0.5)*180)