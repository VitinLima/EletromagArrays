# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 00:11:14 2023

@author: 160047412
"""

import numpy as np
import scipy.optimize
import itertools

from Array import Array
from Optimization import Optimization

class SpecialOptim:
    def __init__(self,constants):
        self.constants=constants
        self.available_antennas = []
        self.analyses = []
        self.weights = None
        self.target_antenna = None
        # self.N_arrays = 30
        self.start_with_N_antennas = 2
        self.N_antennas = 2
        # self.N_iterations = 40
        self.method='BFGS'
    
    def run(self):
        if self.target_antenna==None or self.analyses==[]:
            return
        
        self.best_result = None
        if not self.target_antenna.ok:
            self.target_antenna.evaluate()
        
        theta=self.target_antenna.theta.copy()
        phi=self.target_antenna.phi.copy()
        
        for r in range(self.start_with_N_antennas,self.N_antennas+1):
            for iterating_antennas in itertools.product(self.available_antennas, repeat=r):
                antennas = [antenna.copy() for antenna in iterating_antennas]
                working_array = Array(constants=self.constants,
                                      theta=theta,phi=phi,
                                      antennas=antennas)
                working_array.current_mirror = True
                working_array.y_symmetry = True
                working_array.y_mirror = True
                working_array.x_mirror = True
                print('optimizing with {} antennas:'.format(r))
                print('\t'+str([antenna.name for antenna in antennas]))
                x_map = []
                for i in range(len(antennas)):
                    antenna = antennas[i]
                    antenna.elevation=-90
                    antenna.x = i*0.5
                    x_map.append(dict(
                        antenna=antenna,
                        variables=[
                            'elevation',
                            'azimuth',
                            # 'x',
                            # 'y',
                            # 'z'
                            ]
                        ))
                optim = Optimization(x_map=x_map,
                                     method=self.method,
                                     working_array=working_array,
                                     target_antenna=self.target_antenna,
                                     analyses=self.analyses)
                optim.run()
                print('\tcost: {}'.format(optim.cost))
                if self.best_result is None:
                    self.best_result = optim
                elif optim.cost < self.best_result.cost:
                    self.best_result = optim

if __name__=='__main__':
    import os
    
    from Antenna import Antenna
    from Analysis import Analysis
    
    constants = dict()
    constants['c'] = 299792458 # m/s
    constants['f'] = 433e6 # Hz
    constants['eta'] = 120*np.pi
    constants['lam'] = constants['c']/constants['f'] # m
    constants['w'] = 2*np.pi*constants['f'] # rad/s
    constants['k'] = 2*np.pi/constants['lam'] # rad/m
    
    antennas_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
    
    theta=np.linspace(0, 180, 91)
    phi=np.linspace(-180, 180, 91)
    dip = Antenna(constants,name='Dipole',
                  theta=theta.copy(),phi=phi.copy())
    # antenna_path = os.path.join(antennas_dir, 'antenna-Dipole.csv')
    # dip.evaluate_function = dip.load_file
    # dip.eval_fun_args['file path'] = antenna_path
    dip.set_orientation(elevation=0,azimuth=90)
    
    yagi2 = Antenna(constants,name='Yagi 2 elements',
                    theta=theta.copy(),phi=phi.copy())
    antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-2Elements.csv')
    yagi2.evaluate_function = yagi2.load_file
    yagi2.eval_fun_args['file path'] = antenna_path
    yagi2.set_orientation(elevation=-90,azimuth=0)
    
    yagi3 = Antenna(constants,name='Yagi 3 elements',
                    theta=theta.copy(),phi=phi.copy())
    antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-3Elements.csv')
    yagi3.evaluate_function = yagi3.load_file
    yagi3.eval_fun_args['file path'] = antenna_path
    yagi3.set_orientation(elevation=-90,azimuth=0)
    
    yagi4 = Antenna(constants,name='Yagi 4 elements',
                              theta=theta.copy(),phi=phi.copy())
    antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-4Elements.csv')
    yagi4.evaluate_function = yagi4.load_file
    yagi4.eval_fun_args['file path'] = antenna_path
    yagi4.set_orientation(elevation=-90,azimuth=0)
    
    t = Antenna(name='target',constants=constants,
                theta=theta.copy(),phi=phi.copy())
    t.evaluate_function = t.eval_expression
    t.eval_fun_args['expression theta'] = '(U(radians(-70),phi)-U(radians(70),phi))*(U(radians(60),theta)-U(radians(120),theta))'
    # t.eval_fun_args['expression theta'] = 'U(radians(10),phi)'
    # t.eval_fun_args['expression theta'] = 'sin(theta)*sin(phi/2)'
    t.eval_fun_args['expression phi'] = '0'
    t.set_orientation(elevation=-90,azimuth=90)
    
    t.evaluate()
    
    analysisF = Analysis(name='F',expression='F')
    
    optim = SpecialOptim(constants=constants)
    optim.target_antenna = t
    optim.analyses = [analysisF]
    optim.available_antennas = [
        dip,
        yagi2,
        yagi3,
        yagi4
        ]
    optim.N_antennas=4
    optim.start_with_N_antennas = 2
    # optim.method = 'BFGS'
    
    import tkinter as tk
    from tkinter import ttk
    
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
    from matplotlib.backend_bases import key_press_handler
    
    from Result import Result
    
    def on_btn():
        optim.run()
        
        w = optim.best_result.working_array
        print('final cost: {}'.format(optim.best_result.cost))
        print('working array have {N} antennas:'.format(N=len(w.antennas)))
        for i in range(len(w.antennas)):
            antenna = w.antennas[i]
            print('\tantenna {i}: '.format(i=i) + antenna.name)
            print('\t\televation: {e}'.format(e=antenna.elevation))
            print('\t\tazimuth: {a}'.format(a=antenna.azimuth))
            print('\t\tx: {x}'.format(x=antenna.x))
            print('\t\ty: {y}'.format(y=antenna.y))
            print('\t\tz: {z}'.format(z=antenna.z))
        
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        canvas_2 = FigureCanvasTkAgg(figure, master=fr2)
        canvas_2.draw()
        toolbar = NavigationToolbar2Tk(canvas_2, fr2, pack_toolbar=False)
        toolbar.update()
        canvas_2.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        canvas_2.mpl_connect("key_press_event", key_press_handler)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas_2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        ax_2 = figure.add_subplot(projection='3d')
        ax_2.set_xlabel('x')
        ax_2.set_ylabel('y')
        ax_2.set_zlabel('z')
        result_2 = Result(antenna=w,analysis=analysisF,axes=ax_2)
        result_2.update()
        ax_2.axis('equal')
        canvas_2.draw()
    
    root = tk.Tk()
    tk.Button(master=root,text='continue',command=on_btn).pack(side='top')
    fr1 = ttk.Labelframe(master=root,text='array 1')
    fr2 = ttk.LabelFrame(master=root,text='array 2')
    fr1.pack(side='left',fill='both')
    fr2.pack(side='left',fill='both')
    
    figure = plt.Figure(figsize=(5, 4), dpi=100)
    
    canvas_1 = FigureCanvasTkAgg(figure, master=fr1)
    canvas_1.draw()
    toolbar = NavigationToolbar2Tk(canvas_1, fr1, pack_toolbar=False)
    toolbar.update()
    canvas_1.mpl_connect(
        "key_press_event", lambda event: print(f"you pressed {event.key}"))
    canvas_1.mpl_connect("key_press_event", key_press_handler)
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas_1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    ax_1 = figure.add_subplot()
    ax_1.set_xlabel('x')
    ax_1.set_ylabel('y')
    result_1 = Result(antenna=t,analysis=analysisF,axes=ax_1)
    result_1.update()
    ax_1.axis('equal')
    canvas_1.draw()
    
    root.mainloop()