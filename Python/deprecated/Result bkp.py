# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 17:49:04 2023

@author: 160047412
"""

import tkinter as tk
import numpy as np

# import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure

class ResultFrame(tk.Frame):
    def __init__(self,master=None,name='New result',**kw):
        tk.Frame.__init__(self, master, width=300, height=200, **kw)

class ResultAxes:
    pass

class Result(tk.Frame):
    def __init__(self,master=None,name='New result',antenna=None,analysis=None,**kw):
        tk.Frame.__init__(self, master, width=300, height=200, **kw)
        self.name=name
        self.antenna=antenna
        self.analysis=analysis
        
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        # self.ax = self.fig.add_subplot()
        self.ax = None
        self.axes_list = []
        
        # self.t = np.arange(0, 3, .01)
        # self.ax = self.fig.add_subplot()
        # self.line, = self.ax.plot(self.t, 2 * np.sin(2 * np.pi * self.t))
        # self.ax.set_xlabel("time [s]")
        # self.ax.set_ylabel("f(t)")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.canvas.draw()
        
        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        
        self.canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        self.canvas.mpl_connect("key_press_event", key_press_handler)
        
        # self.slider_update = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL,
        #                               command=self.update_frequency, label="Frequency [Hz]")

        # Packing order is important. Widgets are processed sequentially and if there
        # is no space left, because the window is too small, they are not displayed.
        # The canvas is rather flexible in its size, so we pack it last which makes
        # sure the UI controls are displayed as long as possible.
        # self.slider_update.pack(side=tk.BOTTOM)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.state = 'up to date'
        self.listeners = []
    
    def update_frequency(self, new_val):
        # retrieve frequency
        f = float(new_val)
        
        # update data
        y = 2 * np.sin(2 * np.pi * f * self.t)
        self.line.set_data(self.t, y)
        
        # required to update canvas and attached toolbar!
        self.canvas.draw()
    
    def add_subplot(self):
        if self.antenna==None or self.analysis==None:
            return
        self.ax = self.fig.add_subplot(projection='3d')
        self.axes_list.append(self.ax)
        self.canvas.draw()
    
    def draw_3dpolar(self):
        if self.antenna==None or self.analysis==None:
            return
        field = self.analysis.evaluate(self.antenna)
        field[field<1e-3] = 0
        R = field[:,:,np.newaxis]*self.antenna.hat_k

        jet = plt.colormaps['jet']
        field_max = field.max()
        field_min = field.min()
        if field_max!=field_min:
            C = (field-field_min)/(field_max-field_min)
            rgb = jet(C)
        else:
            rgb = list(field.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
        self.ax.plot_surface(R[:,:,0], R[:,:,1], R[:,:,2], rstride=1, cstride=1, facecolors=rgb,
                                linewidth=0, antialiased=False)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')
        self.ax.axis('equal')
        self.canvas.draw()

if __name__=='__main__':
    from Antenna import Antenna
    from Analysis import Analysis
    
    constants = dict()
    constants['c'] = 299792458 # m/s
    constants['f'] = 433e6 # Hz
    constants['eta'] = 120*np.pi
    constants['lam'] = constants['c']/constants['f'] # m
    constants['w'] = 2*np.pi*constants['f'] # rad/s
    constants['k'] = 2*np.pi/constants['lam'] # rad/m
    
    root = tk.Tk()
    root.wm_title("Embedding in Tk")
    result = Result(master=root,antenna=Antenna(constants=constants),analysis=Analysis())
    result.pack()
    result.add_subplot()
    result.draw_3dpolar()
    result.fig.clear()
    result.add_subplot()
    result.draw_3dpolar()
    root.mainloop()