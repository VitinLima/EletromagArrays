# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 15:08:48 2023

@author: 160047412
"""

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
    def __init__(self,x_map=None,
                 name='new optimization',
                 method='L-BFGS-B',
                 working_array=None,target_antenna=None,
                 analyses=None,weights=None,
                 weight_mask=1,
                 options={
                     # 'disp':True,
                     'eps':0.01,
                     'gtol':0.1,
                     'xrtol':0.1,
                     'maxiter':30
                     },
                 disp=False):
        self.name=name
        self.method=method
        self.working_array=working_array
        self.target_antenna=target_antenna
        self.analyses=analyses
        self.weights=weights
        self.weight_mask=weight_mask
        self.x_map=x_map
        self.options=options
        self.disp=disp
        
        self.result = None
        
        self.state = 'up to date'
        self.listeners = []
    
    def assert_variables(self, x):
        for entry,x_val in zip(self.working_x_map,x):
            # print(x_obj['obj'])
            entry['v_cb'](entry['antenna'],x_val)
            # entry['antenna'].ok = False
        
        self.working_array.local_field_flag = True
        self.working_array.ok = False
        self.working_array.evaluate()
    
    def iter_callback(self, xk, state=None):
        print('cost: {}'.format(self.cost))
        if self.cost<1:
            return True
        else:
            return False
    
    def cost_function(self, x, *args):
        self.assert_variables(x)
        
        total_cost = 0
        for analysis,weights,evaluated_analysis in zip(self.analyses,self.weights,self.evaluated_analyses):
            C = self.weight_mask*(np.abs(analysis.evaluate_field(self.working_array)) - evaluated_analysis)
            total_cost += weights*np.abs(C).sum()
        if self.disp:
            print('evaluated with ' + str(x) + ' cost ' + str(total_cost))
        self.cost = total_cost
        return total_cost
    
    def run(self):
        if self.working_array==None or self.target_antenna==None or self.x_map==None or self.analyses==None:
            return
        
        if not self.target_antenna.ok:
            self.target_antenna.evaluate()
        
        if self.weights is None:
            self.weights=np.ones((len(self.analyses)))
        
        self.evaluated_analyses = [np.abs(analysis.evaluate_field(self.target_antenna)) for analysis in self.analyses]
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
                    x.append(antenna.x/3)
                    bounds.append((0.0,None))
                elif variable=='y':
                    v_cb=self.set_y
                    x.append(antenna.y/3)
                    bounds.append((0.0,None))
                elif variable=='z':
                    v_cb=self.set_z
                    x.append(antenna.z/3)
                    bounds.append((0.0,None))
                elif variable=='current magnitude':
                    v_cb=self.set_current_magnitude
                    x.append(antenna.current_mag)
                    bounds.append((None,None))
                elif variable=='current phase':
                    v_cb=self.set_current_phase
                    x.append((antenna.current_phase/360)+0.5)
                    bounds.append((0.0,1.0))
                self.working_x_map.append(dict(
                    antenna=antenna,
                    v_cb=v_cb
                    ))
        self.result = scipy.optimize.minimize(fun=self.cost_function,x0=np.array(x),
                                    method=self.method,
                                    bounds=bounds,
                                    options=self.options)
    
    def set_elevation(self,antenna,x):
        antenna.set_orientation(elevation=(x-0.5)*180)
    
    def set_azimuth(self,antenna,x):
        antenna.set_orientation(azimuth=(x-0.5)*360)
    
    def set_roll(self,antenna,x):
        antenna.set_orientation(roll=(x-0.5)*360)
    
    def set_x(self,antenna,x):
        antenna.set_position(x=3*x)
    
    def set_y(self,antenna,y):
        antenna.set_position(y=3*y)
    
    def set_z(self,antenna,z):
        antenna.set_position(z=3*z)
    
    def set_current_magnitude(self,antenna,magnitude):
        antenna.set_current(current_mag=magnitude)
    
    def set_current_phase(self,antenna,phase):
        antenna.set_current(current_phase=(phase-0.5)*180)

if __name__=='__main__':
    import os
    
    from Antenna import Antenna
    from Array import Array
    from Analysis import Analysis
    
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
    
    target_distribution = Antenna(constants, name='Project target',
                                  theta=theta.copy(),
                                  phi=phi.copy())
    target_distribution.evaluate_as = 'expressions'
    target_distribution.evaluation_arguments['expression theta'] = '(U(-pi/2,phi)-U(pi/2,phi))*(U(radians(80),theta)-U(radians(100),theta))'
    target_distribution.evaluation_arguments['expression phi'] = '0'
    target_distribution.set_orientation(elevation=-90,azimuth=90)
    target_distribution.evaluate()
    
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
    
    target_antenna = antenna_2.copy()
    target_antenna.set_orientation(elevation=-50,
                                   azimuth=40
                                   )
    target_antenna.evaluate()
    
    working_array = Array(constants=constants,
                          theta=theta,phi=phi)
    working_array.add_antenna(antenna_2.copy())
    working_array.antennas[0].set_orientation(elevation=-90)
    
    x_map = []
    x_map.append(dict(
        antenna=working_array.antennas[0],
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
    optim = Optimization(x_map=x_map,
                         working_array=working_array,
                         target_antenna=target_antenna,
                         analyses=[Ftheta])
    
    import tkinter as tk
    
    from ResultFrame import ResultFrame
    
    def on_btn():
        optim.run()
        
        print('final cost: {}'.format(optim.cost))
        print('working array have {N} antennas:'.format(N=len(working_array.antennas)))
        for i in range(len(working_array.antennas)):
            antenna = working_array.antennas[i]
            print('\tantenna {i}: '.format(i=i) + antenna.name)
            print('\t\televation: {e}'.format(e=antenna.elevation))
            print('\t\tazimuth: {a}'.format(a=antenna.azimuth))
            # print('\t\tx: {x}'.format(x=antenna.x))
            # print('\t\ty: {y}'.format(y=antenna.y))
            # print('\t\tz: {z}'.format(z=antenna.z))
        
        result = ResultFrame(master=root,name='Array F',
                    antenna=working_array,analysis=F,
                    plot='2d Polar Patch')
        result.pack(side='left',fill='both')
        result.update()
    
    root = tk.Tk()
    tk.Button(master=root,text='continue',command=on_btn).pack(side='top')

    result = ResultFrame(master=root,name='Target F',
                antenna=target_antenna,analysis=F,
                plot='2d Polar Patch')
    result.pack(side='left',fill='both')
    result.update()
    
    root.mainloop()