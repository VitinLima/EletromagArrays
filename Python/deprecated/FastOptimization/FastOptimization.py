# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 00:09:57 2023

@author: 160047412
"""

import numpy as np
import scipy.optimize

class Optimization:
    def __init__(self,x_map=[],
                 name='new optimization',method='L-BFGS-B',
                 working_array=None,target_antenna=None,
                 analyses=[],weights=None,
                 options={'disp':True,
                           # 'eps':1,
                          # 'gtol':1,
                          # 'xrtol':0.1,
                          # 'maxiter':30
                          }):
        self.name=name
        self.method=method
        self.working_array=working_array
        self.target_antenna=target_antenna
        self.analyses = analyses
        self.weights = weights
        self.x_map = x_map
        self.options=options
        
        self.result = None
        
        self.state = 'up to date'
        self.listeners = []
    
    def assert_variables(self, x):
        for entry,x_val in zip(self.working_x_map,x):
            # print(x_obj['obj'])
            entry['v_cb'](entry['antenna'],x_val)
            entry['antenna'].evaluate_R()
            entry['antenna'].evaluate_hats()
            # x_obj['obj'].ok = False
        # for d in self.x_map:
        
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
            C = analysis.evaluate_field(self.working_array) - evaluated_analysis
            total_cost += weights*(C*C.conj()).sum()
        # print('evaluated with ' + str(x) + ' cost ' + str(total_cost))
        self.cost = total_cost
        return total_cost
    
    def run(self):
        if self.working_array==None or self.target_antenna==None or self.x_map==None or self.analyses==[]:
            return
        
        if not self.target_antenna.ok:
            self.target_antenna.evaluate()
        
        if self.weights is None:
            self.weights=np.ones((len(self.analyses)))
        
        self.evaluated_analyses = [analysis.evaluate_field(self.target_antenna) for analysis in self.analyses]
        self.working_x_map = []
        x=[]
        bounds=[]
        for entry in self.x_map:
            antenna = entry['antenna']
            for variable in entry['variables']:
                if variable=='elevation':
                    v_cb=self.set_elevation
                    x.append((antenna.elevation/360)+0.5)
                    bounds.append((0,1))
                elif variable=='azimuth':
                    v_cb=self.set_azimuth
                    x.append((antenna.azimuth/360)+0.5)
                    bounds.append((0,1))
                elif variable=='x':
                    v_cb=self.set_x
                    x.append(antenna.x/3)
                    bounds.append((None,None))
                elif variable=='y':
                    v_cb=self.set_y
                    x.append(antenna.y/3)
                    bounds.append((None,None))
                elif variable=='z':
                    v_cb=self.set_z
                    x.append(antenna.z/3)
                    bounds.append((None,None))
                self.working_x_map.append(dict(
                    antenna=antenna,
                    v_cb=v_cb
                    ))
        self.result = scipy.optimize.minimize(fun=self.cost_function,x0=np.array(x),
                                    method=self.method,
                                    bounds=bounds,
                                    options=self.options)
    def set_elevation(self,antenna,x):
        antenna.elevation = (x-0.5)*180
    
    def set_azimuth(self,antenna,x):
        antenna.azimuth = (x-0.5)*180
    
    def set_x(self,antenna,x):
        antenna.x = 3*x
    
    def set_y(self,antenna,y):
        antenna.y = 3*y
    
    def set_z(self,antenna,z):
        antenna.z = 3*z

if __name__=='__main__':
    # import matplotlib.pyplot as plt
    
    from Antenna import Antenna
    from Array import Array
    from Analysis import Analysis
    from Result import Result
    
    constants = dict()
    constants['c'] = 299792458 # m/s
    constants['f'] = 433e6 # Hz
    constants['eta'] = 120*np.pi
    constants['lam'] = constants['c']/constants['f'] # m
    constants['w'] = 2*np.pi*constants['f'] # rad/s
    constants['k'] = 2*np.pi/constants['lam'] # rad/m
    
    theta=np.linspace(0, 180, 91)
    phi=np.linspace(-180, 180, 91)
    antenna = Antenna(constants,name='Ideal Dipole',
                      theta=theta.copy(), phi=phi.copy(),
                      elevation=0,azimuth=0)
    
    working_array = Array(constants,name='Array 1',
                      theta=theta.copy(), phi=phi.copy())
    working_array.add_antenna(antenna)
    working_array.add_antenna(antenna.copy())
    # working_array.antennas[1].x=1.7
    # working_array.add_antenna(antenna.copy())
    working_array.evaluate()
    
    target_antenna = Array(constants,name='Array 2',
                      theta=theta.copy(), phi=phi.copy())
    target_antenna.add_antenna(antenna.copy())
    target_antenna.add_antenna(antenna.copy())
    # target_antenna.add_antenna(antenna.copy())
    # target_antenna.antennas[0].set_orientation(elevation=35)
    target_antenna.antennas[1].set_orientation(elevation=25)
    target_antenna.antennas[1].x=0.5
    # target_antenna.antennas[2].set_orientation(elevation=30,azimuth=-10)
    target_antenna.evaluate()
    
    analysisF = Analysis(name='F',expression='F')
    aFtheta = Analysis(name='Ftheta',expression='Ftheta')
    aFphi = Analysis(name='Fphi',expression='Fphi')
    
    x_map = []
    # x_map.append({
    #     'obj':working_array.antennas[0],
    #     'variables':['elevation','x']})
    x_map.append({
        'obj':working_array.antennas[1],
        'variables':['elevation','x']})
    optim = Optimization(x_map=x_map,
                          working_array=working_array,target_antenna=target_antenna,
                          analyses=[aFtheta,aFphi],
                          options={'disp':True,'eps':0.0001})
    
    
    
    import tkinter as tk
    from tkinter import ttk
    from threading import Thread
    
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
    from matplotlib.backend_bases import key_press_handler
    
    def btn_command():
        print('optimizing')
        # antenna = working_array.antennas[0]
        # antenna.elevation=45
        # antenna.evaluate_R()
        # antenna.evaluate_hats()
        # antenna.ok = False
        # antenna.evaluate()
        optim.run()
        print('array 1')
        for antenna in working_array.antennas:
            print('elevation: {e}'.format(e=antenna.elevation))
            print('azimuth: {a}'.format(a=antenna.azimuth))
            print('x: {x}'.format(x=antenna.x))
        print('array 2')
        for antenna in target_antenna.antennas:
            print('elevation: {e}'.format(e=antenna.elevation))
            print('azimuth: {a}'.format(a=antenna.azimuth))
            print('x: {x}'.format(x=antenna.x))
        result_1.update()
        canvas_1.draw()
        result_2.update()
        canvas_2.draw()
    
    root = tk.Tk()
    tk.Button(master=root,text='optimize',command=btn_command).pack(side='top')
    # tabs = ttk.Notebook(master=root)
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
    
    ax_1 = figure.add_subplot(projection='3d')
    ax_1.set_xlabel('x')
    ax_1.set_ylabel('y')
    ax_1.set_zlabel('z')
    result_1 = Result(antenna=working_array,analysis=analysisF,axes=ax_1)
    result_1.update()
    ax_1.axis('equal')
    canvas_1.draw()
    
    
    
    
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
    result_2 = Result(antenna=target_antenna,analysis=analysisF,axes=ax_2)
    result_2.update()
    ax_2.axis('equal')
    canvas_2.draw()
    
    # thread = Thread(target=root.mainloop)
    # thread.start()
    root.mainloop()