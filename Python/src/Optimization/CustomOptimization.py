#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 14:20:23 2023

@author: vitinho
"""

import time
import numpy as np
import scipy.optimize

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
                 x0,
                 x_map=None,
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
        
    def cost_function_helper(self, x, *args):
        self.number_of_evaluations += 1
        
        cost = self.cost_function(x, self.target_antenna, self.working_array)
        if self.disp:
            print('evaluating with ' + str(x) + ' cost ' + str(cost))
        
        if self.cost is None:
            self.cost = cost
            self.x = x
        elif cost < self.cost:
            self.cost = cost
            self.x = x
        return cost
    
    def run(self):
        if not self.target_antenna.ok:
            self.target_antenna.evaluate()
        self.start_time = time.time()
        
        self.working_x_map = []
        self.number_of_evaluations = 0
        self.result = scipy.optimize.minimize(fun=self.cost_function_helper,x0=self.x0,
                                    method=self.method,
                                    bounds=self.bounds,
                                    options=self.options)
        self.cost_function_helper(self.x)
        
        self.elapsed_time = time.time()-self.start_time
        
        if self.disp:
            print('elapsed time was ' + str(self.elapsed_time))
            print('number of evaluations was ' + str(self.number_of_evaluations))
            print('final cost: {}'.format(self.cost))
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

if __name__=="__main__":
    def set_elevation(antenna,x):
        antenna.set_orientation(elevation=(x-0.5)*180)
    
    def set_azimuth(antenna,x):
        antenna.set_orientation(azimuth=(x-0.5)*360)
    
    def set_roll(antenna,x):
        antenna.set_orientation(roll=(x-0.5)*360)
    
    def set_x(antenna,x):
        antenna.set_position(x=x)
    
    def set_y(antenna,y):
        antenna.set_position(y=y)
    
    def set_z(antenna,z):
        antenna.set_position(z=z)
    
    def set_current_magnitude(antenna,magnitude):
        antenna.set_current(magnitude=magnitude)
    
    def set_current_phase(antenna,phase):
        antenna.set_current(phase=(phase-0.5)*180)
    
    def cost_function(x, target, array):
        cost = np.abs(np.abs(target.Frhcp)-np.abs(array.Frhcp)).sum()
        cost += np.abs(np.abs(target.Flhcp)-np.abs(array.Flhcp)).sum()
        
        if len(array.antennas) & 1:
            N = int(len(array.antennas)/2)
            k = 1
            array.antennas[N].set_current(magnitude=x[0])
            for i in range(1,N+1):
                array.antennas[N + k].set_current(magnitude=x[i])
                array.antennas[N - k].set_current(magnitude=x[i])
                k = k+1
            # k = 1
            # for i in range(1,N+1):
            #     array.antennas[N + k].set_orientation(elevation=-90*x[N+i])
            #     array.antennas[N - k].set_orientation(elevation=-90*(1-x[N+i]))
            #     k = k+1
        else:
            N = int(len(array.antennas)/2)
            k = 0
            # print(N)
            # print(" " + str(len(array.antennas)))
            for i in range(0,N):
                # print("  " + str(i) + " " + str(N+k) + " " + str(N-1-k))
                array.antennas[N + k].set_current(magnitude=x[i])
                array.antennas[N-1 - k].set_current(magnitude=x[i])
                k = k+1
            # k = 1
            # for i in range(0,N):
            #     array.antennas[N + k].set_orientation(elevation=-90*x[N+i])
            #     array.antennas[N-1 - k].set_orientation(elevation=-90*(1-x[N+i]))
            #     k = k+1
        
        for antenna in array.antennas:
            antenna.ok = False
        
        array.local_field_flag = True
        array.ok = False
        array.evaluate()
        
        return cost
    
    import sys
    import os
    path = os.path.split(os.path.split(__file__)[0])[0]
    sys.path.insert(0, path)
    
    import matplotlib.pyplot as plt
    plt.close('all')

    import pickle

    print("Loading antennas")

    import Scripts.AntennasLoaders.LoadHFSSYagis
    antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(Ntheta=91, Nphi=91)

    print("Loading export results directory")

    N = 30
    export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/CustomOptimizationCircular' + str(N)
    if not os.path.exists(export_directory):
        os.mkdir(export_directory)

    print("Creating target distribution")

    # import numpy as np

    import Antenna
    import Array

    Ntheta=91
    Nphi=181

    theta=np.linspace(0, 180, Ntheta)
    phi=np.linspace(-180, 180, Nphi)

    target_antenna = Antenna.Antenna(
        name='Target RHCP',
        theta=theta.copy(),
        phi=phi.copy())
    target_antenna.evaluate_as = 'expressions'
    U1 = '(U(-pi/2,phi)-U(pi/2,phi))'
    U2 = '(U(radians(60),theta)-U(radians(80),theta))'
    U3 = '(U(radians(100),theta)-U(radians(120),theta))'
    U4 = '('+U2+'+'+U3+')'
    U5 = '(U(radians(80),theta)-U(radians(100),theta))'
    target_antenna.evaluation_arguments['expression theta'] = '0.1 - 0.9*1j*('+U1+'*'+U5+')'
    target_antenna.evaluation_arguments['expression phi'] = '0.1 + 0.9*('+U1+'*'+U5+')'
    target_antenna.set_orientation(elevation=-90,azimuth=90)
    target_antenna.evaluate()

    print("Creating working array")

    antennas = [antennas['hfss_yagi2EL'].copy() for a in range(N)]
    working_array = Array.Array(
        name='Initial array',
        theta=theta.copy(),
        phi=phi.copy(),
        antennas=antennas
        )
    # k = -0.1
    for i in range(len(working_array.antennas)):
        working_array.antennas[i].set_position(
            # x=2*(np.random.rand()-0.5)*len(working_array.antennas),
            # y=2*(np.random.rand()-0.5)*len(working_array.antennas),
            x = 0,
            y = i*0.5,
            z=0)
        working_array.antennas[i].set_orientation(
            elevation=-90,
            azimuth=0,
            roll=90*(np.cos(np.pi*i)/2+0.5))
        working_array.antennas[i].set_current(
            magnitude = 1/(2*i+1),
            phase = 90*(np.cos(np.pi*i)/2+0.5))
        # k = k*-1
    working_array.evaluate()
    
    if N & 1:
        bounds = [
            (-10,10) for i in range(int(N/2)+1)
            ]
        # + [
        #     (0,1) for i in range(int(N/2))
        #     ]
        x0 = [working_array.antennas[i].current_magnitude for i in range(int(N/2)+1)]
        # + [0.5 for i in range(int(N/2))]
    else:
        bounds = [
            (-10,10) for i in range(int(N/2))
            ]
        # + [
        #     (0,1) for i in range(int(N/2))
        #     ]
        x0 = [working_array.antennas[i].current_magnitude for i in range(int(N/2))]
        # + [0.5 for i in range(int(N/2))]

    print("Exporting initial state")

    import Scripts.ExportResults

    Scripts.ExportResults.run([
        working_array,
        ], export_directory,
        fields=[
            'F',
            'Fref',
            'Fcross',
            'Frhcp',
            'Flhcp'
            ])

    print("Optimizing")

    optim = CustomOptimization(
        cost_function=cost_function,
        x0 = x0,
        target_antenna=target_antenna,
        working_array=working_array,
        x_map = [
            dict(
                antenna=working_array.antennas[i],
                variables = [
                    # 'x',
                    # 'y',
                    'elevation',
                    # 'azimuth',
                    # 'roll',
                    'current magnitude',
                    # 'current phase',
                    ],
                ) for i in range(len(working_array.antennas))
            ],
        disp=True,
        bounds=bounds,
        # method='Nelder-Mead',
        # method='Powell',
        # tol = 1,
        # options=dict(maxiter=300),
        )
    result = optim.run()
    
    filename = os.path.join(export_directory,'Optimization with {N} antennas and cost {cost}.dat'.format(N=len(optim.working_array.antennas), cost=optim.result.fun))
    with open(filename, mode='wb') as f:
        pickle.dump(optim, f)

    working_array = optim.working_array
    print(result)

    target_antenna.name = 'Target Antenna'
    working_array.name = 'Result Array'

    print("Exporting results")

    Scripts.ExportResults.run([
        target_antenna,
        working_array,
        ], export_directory,
        fields=[
            # 'F',
            # 'Fref',
            # 'Fcross',
            'Frhcp',
            'Flhcp'
            ])

    print("Starting visualization")

    import App
    import ResultFrame
    import Result

    app = App.App(antennas=[target_antenna, working_array])
    try:
        Ntheta = 91
        Nphi = 181
        field = 'F'
        plot = '2d Polar Patch'
        
        tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
        Result.Result(tab=tab,
                      title='Result',
                      name='Result F',
                      antenna=working_array,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=1,row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        Result.Result(tab=tab,
                      title='Target',
                      name='Target F',
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
        
        tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
        Result.Result(tab=tab,
                      title='Result',
                      name='Result RHCP',
                      antenna=working_array,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=1,row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        Result.Result(tab=tab,
                      title='Target',
                      name='Target RHCP',
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
        
        tab = ResultFrame.ResultFrame(master=app.tabs,name=field,columns=2,rows=1)
        Result.Result(tab=tab,
                      title='Result',
                      name='Result LHCP',
                      antenna=working_array,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=1,row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        Result.Result(tab=tab,
                      title='Target',
                      name='Target LHCP',
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
        # If some error occur, destroy the application to close the window,
        # then show the error
        app.destroy()
        raise e