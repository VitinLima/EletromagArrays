#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 14:20:23 2023

@author: vitinho
"""

import time
import numpy as np
import scipy.optimize

# OPTIONS
save_graphs = True

class CustomOptimization:
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
                 x_map,
                 x0=None,
                 name='new optimization',
                 method='L-BFGS-B',
                 working_array=None,
                 target_antenna=None,
                 bounds=None,
                 options={
                     # 'disp':True,
                     'eps':0.01,
                     'gtol':0.1,
                     'xrtol':0.1,
                     'maxiter':30
                     },
                 disp=False):
        self.cost_function=cost_function
        self.x_map=x_map
        self.x0=x0
        self.name=name
        self.method=method
        self.working_array=working_array
        self.target_antenna=target_antenna
        self.bounds=bounds
        self.options=options
        self.disp=disp
        
        self.result = None
        self.cost = None
        self.x = []
        
        if self.x0 is None:
            self.get_x0_from_array()
    
    def get_x0_from_array(self):
        self.x0 = []
        for e in x_map:
            antenna = e['antenna']
            for variable in e['variables']:
                if variable=='x':
                    x0_element = antenna.x
                elif variable=='y':
                    x0_element = antenna.y
                elif variable=='z':
                    x0_element = antenna.z
                elif variable=='elevation':
                    x0_element = antenna.elevation/180 + 0.5
                elif variable=='azimuth':
                    x0_element = antenna.azimuth/360 + 0.5
                elif variable=='roll':
                    x0_element = antenna.roll/360 + 0.5
                elif variable=='current magnitude':
                    x0_element = antenna.current_magnitude
                elif variable=='current phase':
                    x0_element = antennas.current_phase/360 + 0.5
                self.x0.append(x0_element)
        N_2 = int(len(self.working_array.antennas)/2)
        if len(self.working_array.antennas)&1:
            n = 1
        else:
            n = 0
        for i in range(N_2):
            antenna_2 = self.working_array.antennas[n + i]
            antenna_1 = self.working_array.antennas[n + N_2 + i]
            antenna_2.set_position(x=antenna_1.x,
                                   y=-antenna_1.y,
                                   z=antenna_1.z)
            antenna_2.set_orientation(elevation=antenna_1.elevation,
                                      azimuth=(antenna_1.azimuth+360)%360-180,
                                      roll=antenna_1.roll)
            antenna_2.set_current(magnitude=antenna_1.current_magnitude,
                                  phase=180 + antenna_1.current_phase)
        
    def cost_function_helper(self, x, *args):
        self.number_of_evaluations += 1
        
        N_2 = int(len(self.working_array.antennas)/2)
        if len(self.working_array.antennas) & 1:
            k = 0
            i = 0
            for variable in self.x_map[0]['variables']:
                current_assertion = self.get_assertion(variable)
                current_assertion(self.working_array.antennas[0], x[k])
                k = k+1
            i = i+1
            n = 1
        else:
            n = 0
        k = 0
        i = 0
        for e in self.x_map:
            for variable in e['variables']:
                current_assertion = self.get_assertion(variable)
                current_assertion(self.working_array.antennas[n+i], x[k], 1)
                current_assertion(self.working_array.antennas[n+N_2+i], x[k], -1)
                k = k+1
            i = i+1
        
        for antenna in self.working_array.antennas:
            antenna.ok = False
        
        self.working_array.local_field_flag = True
        self.working_array.ok = False
        self.working_array.evaluate()
        
        cost = self.cost_function(
            self.target_antenna,
            self.working_array)
        if self.disp:
            print('evaluating with ' + str(x) + ' cost ' + str(cost))
            for i in range(len(self.working_array.antennas)):
                antenna = self.working_array.antennas[i]
                print('\tantenna {i}: '.format(i=i) + antenna.name)
                print('\t\televation: {e}'.format(
                    e=antenna.elevation))
                print('\t\tazimuth: {a}'.format(a=antenna.azimuth))
                print('\t\troll: {a}'.format(a=antenna.roll))
                print('\t\tx: {x}'.format(x=antenna.x))
                print('\t\ty: {y}'.format(y=antenna.y))
                print('\t\tz: {z}'.format(z=antenna.z))
                print('\t\tcurrent magnitude: {magnitude}'.format(
                    magnitude=antenna.current_magnitude))
                print('\t\tcurrent phase: {phase}'.format(
                    phase=antenna.current_phase))
        
        if self.cost is None:
            self.cost = cost
            self.x = x
        elif cost < self.cost:
            self.cost = cost
            self.x = x
        return cost
    
    def get_assertion(self, variable):
        if variable=='x':
            current_assertion = self.set_x
        elif variable=='y':
            current_assertion = self.set_y
        elif variable=='z':
            current_assertion = self.set_z
        elif variable=='elevation':
            current_assertion = self.set_elevation
        elif variable=='azimuth':
            current_assertion = self.set_azimuth
        elif variable=='roll':
            current_assertion = self.set_roll
        elif variable=='current magnitude':
            current_assertion = self.set_current_magnitude
        elif variable=='current phase':
            current_assertion = self.set_current_phase
        return current_assertion
    
    def run(self):
        if not self.target_antenna.ok:
            self.target_antenna.evaluate()
        self.start_time = time.time()
        
        self.working_x_map = []
        self.number_of_evaluations = 0
        self.result = scipy.optimize.minimize(
            fun=self.cost_function_helper,x0=self.x0,
            method=self.method,
            bounds=self.bounds,
            options=self.options)
        self.cost_function_helper(self.x)
        
        self.elapsed_time = time.time()-self.start_time
        
        if self.disp:
            print('elapsed time was ' + str(self.elapsed_time))
            print('number of evaluations was ' +
                  str(self.number_of_evaluations))
            print('final cost: {}'.format(self.cost))
            print('final array have {N} antennas:'.format(
                N=len(self.working_array.antennas)))
            for i in range(len(self.working_array.antennas)):
                antenna = self.working_array.antennas[i]
                print('\tantenna {i}: '.format(i=i) + antenna.name)
                print('\t\televation: {e}'.format(
                    e=antenna.elevation))
                print('\t\tazimuth: {a}'.format(a=antenna.azimuth))
                print('\t\troll: {a}'.format(a=antenna.roll))
                print('\t\tx: {x}'.format(x=antenna.x))
                print('\t\ty: {y}'.format(y=antenna.y))
                print('\t\tz: {z}'.format(z=antenna.z))
                print('\t\tcurrent magnitude: {magnitude}'.format(
                    magnitude=antenna.current_magnitude))
                print('\t\tcurrent phase: {phase}'.format(
                    phase=antenna.current_phase))
        
        return self.result
    
    def set_elevation(self, antenna,x, s=1):
        antenna.set_orientation(elevation=(x-0.5)*180)
    
    def set_azimuth(self, antenna,x, s=1):
        if s==1:
            antenna.set_orientation(azimuth=(x-0.5)*360)
        else:
            antenna.set_orientation(azimuth=180 + (x-0.5)*360)
    
    def set_roll(self, antenna,x, s=1):
        antenna.set_orientation(roll=(x-0.5)*360)
    
    def set_x(self, antenna,x, s=1):
        antenna.set_position(x=s*x)
    
    def set_y(self, antenna,y, s=1):
        antenna.set_position(y=s*y)
    
    def set_z(self, antenna,z, s=1):
        antenna.set_position(z=s*z)
    
    def set_current_magnitude(self, antenna,magnitude, s=1):
        antenna.set_current(magnitude=magnitude)
    
    def set_current_phase(self, antenna,phase, s=1):
        antenna.set_current(phase=(phase-0.5)*360)

def cost_function(target, array):
    cost = (np.abs(np.abs(target.Frhcp)-np.abs(array.Frhcp))*target.sin_mesh_theta).sum()
    cost += (np.abs(np.abs(target.Flhcp)-np.abs(array.Flhcp))*target.sin_mesh_theta).sum()
    
    return cost

import sys
import os
import header

import matplotlib.pyplot as plt
plt.close('all')

import pickle

print("Loading antennas")

import LoadHFSSYagis
antennas = LoadHFSSYagis.run(Ntheta=91,
                                                     Nphi=91)

print("Loading export results directory")

N = 8
export_directory = os.path.join(
    header.results_dir,
    'Optimization',
    'CustomOptimization')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)

print("Creating target distribution")

import Antenna
import Array

Ntheta=91
Nphi=181

theta=np.linspace(0, 180, Ntheta)
phi=np.linspace(-180, 180, Nphi)

target_antenna = Antenna.Antenna(
    name='Target Antenna',
    theta=theta.copy(),
    phi=phi.copy())
target_antenna.evaluate_as = 'expressions'
U1 = '(U(-pi/2,phi)-U(pi/2,phi))'
U2 = '(U(radians(60),theta)-U(radians(80),theta))'
U3 = '(U(radians(100),theta)-U(radians(120),theta))'
U4 = '('+U2+'+'+U3+')'
U5 = '(U(radians(80),theta)-U(radians(100),theta))'
target_antenna.evaluation_arguments['expression theta'] = \
    '0.1 - 0.9*1j*('+U1+'*'+U5+')'
target_antenna.evaluation_arguments['expression phi'] = \
    '0.1 + 0.9*('+U1+'*'+U5+')'
target_antenna.set_orientation(elevation=-90,azimuth=90)
target_antenna.evaluate()

print("Creating working array")

antennas = [antennas['hfss_yagi2EL'].copy() for a in range(N)]
initial_array = Array.Array(
    name='Initial array',
    theta=theta.copy(),
    phi=phi.copy(),
    antennas=antennas
    )
# k = -0.1
k = -1
N_2 = int(N/2)
if N&1:
    initial_array.antennas[0].set_position(
        # x=2*(np.random.rand()-0.5)*len(initial_array.antennas),
        # y=2*(np.random.rand()-0.5)*len(initial_array.antennas),
        x = 0,
        y = 0,
        z=0)
    initial_array.antennas[0].set_orientation(
        elevation=-90,
        azimuth=0,
        roll=0)
    initial_array.antennas[0].set_current(
        magnitude = 1,#/(2*i+1),
        phase = 0)
    n = 1
else:
    n = 0
for i in range(int(N/2)):
    # x=2*(np.random.rand()-0.5)*len(initial_array.antennas),
    # y=2*(np.random.rand()-0.5)*len(initial_array.antennas),
    x = 0
    y = i*0.5 + 0.25*(1-n)
    z = 0
    elevation = -90
    azimuth = 0
    roll = 90*(k/2+0.5)
    magnitude = 1#/(2*i+1)
    phase = 90*(k/2+0.5)
    initial_array.antennas[n+i].set_position(
        x = x,
        y = y,
        z = z)
    initial_array.antennas[n+i].set_orientation(
        elevation=elevation,
        azimuth=azimuth,
        roll=roll)
    initial_array.antennas[n+i].set_current(
        magnitude = magnitude,
        phase = phase)
    initial_array.antennas[n+N_2+i].set_position(
        x = x,
        y = -y,
        z = z)
    initial_array.antennas[n+N_2+i].set_orientation(
        elevation=elevation,
        azimuth=(azimuth+360)%360 - 180,
        roll=roll)
    initial_array.antennas[n+N_2+i].set_current(
        magnitude = magnitude,
        phase = (phase+360)%360 - 180)
    k = k*-1
initial_array.evaluate()

if save_graphs:
    print("Exporting initial state")
    
    import ExportResults
    
    ExportResults.run([
        initial_array,
        ], export_directory,
        fields=[
            'F',
            'Fref',
            'Fcross',
            'Frhcp',
            'Flhcp'
            ])

print("Optimizing")

working_array = initial_array.copy()

variables = [
    # 'x',
    # 'y',
    'elevation',
    # 'azimuth',
    # 'roll',
    'current magnitude',
    # 'current phase',
    ]
x_map = [
    dict(
        antenna = working_array.antennas[i],
        variables = variables,
        ) for i in range(int(N/2)+(N&1))
    ]

bounds_element = []
if 'x' in variables:
    bounds_element.append((0,10))
if 'y' in variables:
    bounds_element.append((0,10))
if 'z' in variables:
    bounds_element.append((0,10))
if 'elevation' in variables:
    bounds_element.append((0,1))
if 'azimuth' in variables:
    bounds_element.append((0,1))
if 'roll' in variables:
    bounds_element.append((0,1))
if 'current magnitude' in variables:
    bounds_element.append((0,None))
if 'current phase' in variables:
    bounds_element.append((0,1))

bounds = []
for i in range(int(N/2)+(N&1)):
    bounds += bounds_element

optim = CustomOptimization(
    cost_function=cost_function,
    x_map = x_map,
    target_antenna=target_antenna,
    working_array=working_array,
    disp=True,
    bounds=bounds,
    # method='Nelder-Mead',
    # method='Powell',
    # tol = 1,
    # options=dict(maxiter=300),
    )

result = optim.run()
final_array = optim.working_array

## Export result array with python module "pickle" for easy loading
# filename = os.path.join(
#     export_directory,
#     'Optimization with {N} antennas and cost {cost}.dat'.format(
#         N=len(optim.working_array.antennas),
#         cost=optim.result.fun))
# with open(filename, mode='wb') as f:
#     pickle.dump(optim, f)

print(result)

final_array.name = 'Result Array'

if save_graphs:
    print("Exporting results")
    
    ExportResults.run([
        initial_array,
        target_antenna,
        final_array,
        ], export_directory,
        fields=[
            'F',
            # 'Fref',
            # 'Fcross',
            'Frhcp',
            'Flhcp'
            ])
    
    import ExportTable
    
    initial_array.name = 'Arranjo inicial'
    final_array.name = 'Arranjo final otimizado'
    
    ExportTable.export_table(
        export_directory,
        arrays=[
            initial_array,
            final_array
            ],
        captions = [
            "Arranjo inicial",
            "Resultados da otimização de polarização linear " +
                "com custo final de {:.2f}".format(optim.cost)
            ])

initial_cost = cost_function(initial_array, target_antenna)
final_cost = cost_function(final_array, target_antenna)
print("Custo inicial: " + str(round(initial_cost*100)/100))
print("Custo final: " + str(round(final_cost*100)/100))
print("Melhora de " + str(round((initial_cost-final_cost)/initial_cost*10000)/100) + "%")

if __name__=="__main__":

    print("Starting visualization")

    import App
    import ResultFrame
    import Result

    app = App.App(antennas=[target_antenna, final_array])
    try:
        Ntheta = 91
        Nphi = 181
        field = 'F'
        plot = '2d Polar Patch'
        
        tab = ResultFrame.ResultFrame(master=app.tabs,name=field,
                                      columns=2,rows=1)
        Result.Result(tab=tab,
                      title='Result',
                      name='Result',
                      antenna=final_array,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=1,row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        Result.Result(tab=tab,
                      title='Target',
                      name='Target',
                      antenna=target_antenna,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=2,row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        app.add_tab(tab)
        
        field = 'Frhcp'
        plot = '2d Polar Patch'
        
        tab = ResultFrame.ResultFrame(master=app.tabs,name=field,
                                      columns=2,rows=1)
        Result.Result(tab=tab,
                      title='Result',
                      name='Result',
                      antenna=final_array,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=1,row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        Result.Result(tab=tab,
                      title='Target',
                      name='Target',
                      antenna=target_antenna,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=2,row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        app.add_tab(tab)
        
        field = 'Flhcp'
        plot = '2d Polar Patch'
        
        tab = ResultFrame.ResultFrame(master=app.tabs,name=field,
                                      columns=2,rows=1)
        Result.Result(tab=tab,
                      title='Result',
                      name='Result',
                      antenna=final_array,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=1,row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        Result.Result(tab=tab,
                      title='Target',
                      name='Target',
                      antenna=target_antenna,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=2,row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        app.add_tab(tab)
        
        # Main application loop
        app.mainloop()
    except Exception as e:
        # If some error occur, destroy the application to close
        # the window, then show the error
        app.destroy()
        raise e