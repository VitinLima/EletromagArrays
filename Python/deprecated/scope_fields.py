# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 19:05:35 2023

@author: 160047412
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

import tkinter as tk
from tkinter import ttk
import numpy as np

def scope_fields(hat_k, Fphis, Fthetas):

    root = tk.Toplevel()
    
    for Fphi,Ftheta in zip(Fphis,Fthetas):
        fr1 = ttk.Labelframe(master=root,text='array 1')
        fr1.pack(side='left',fill='both')
        
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
        
        # a = np.absolute(Fphi);
        # b = np.absolute(Ftheta);
        # F = np.sqrt(a*a + b*b);
        field = np.absolute(Ftheta)
        # field = np.absolute(Fphi)
        
        R = field[:,:,np.newaxis]*hat_k
        
        jet = plt.colormaps['jet']
        # C = field
        # C = np.angle(Fphi)
        C = np.angle(Ftheta)
        C_max = C.max()
        C_min = C.min()
        if C_max!=C_min:
            C = (C-C_min)/(C_max-C_min)
            rgb = jet(C)
        else:
            rgb = list(C.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:,:,3] = 1
            rgb[:,:,2] = 1
            
        
        ax_1.plot_surface(R[:,:,0], R[:,:,1], R[:,:,2],
                              rstride=1, cstride=1, facecolors=rgb,
                              linewidth=0, antialiased=False)
        
        ax_1.axis('equal')
        
        canvas_1.draw()
        
    root.mainloop()
    
    # fr2 = ttk.LabelFrame(master=root,text='array 2')
    # fr2.pack(side='left',fill='both')
    
    # figure = plt.Figure(figsize=(5, 4), dpi=100)
    # canvas_2 = FigureCanvasTkAgg(figure, master=fr2)
    # canvas_2.draw()
    # toolbar = NavigationToolbar2Tk(canvas_2, fr2, pack_toolbar=False)
    # toolbar.update()
    # canvas_2.mpl_connect(
    #     "key_press_event", lambda event: print(f"you pressed {event.key}"))
    # canvas_2.mpl_connect("key_press_event", key_press_handler)
    # toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    # canvas_2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    # ax_2 = figure.add_subplot(projection='3d')
    # ax_2.set_xlabel('x')
    # ax_2.set_ylabel('y')
    # ax_2.set_zlabel('z')
    
    # a = np.absolute(s_Fphi);
    # b = np.absolute(s_Ftheta);
    # F = np.sqrt(a*a + b*b);
    # field = np.absolute(F)
    # R = field[:,:,np.newaxis]*self.hat_k
    
    # jet = plt.colormaps['jet']
    # field_max = field.max()
    # field_min = field.min()
    # if field_max!=field_min:
    #     C = (field-field_min)/(field_max-field_min)
    #     rgb = jet(C)
    # else:
    #     rgb = list(field.shape)
    #     rgb.append(4)
    #     rgb = np.zeros(tuple(rgb))
    #     rgb[:,:,3] = 1
    #     rgb[:,:,2] = 1
        
    
    # ax_2.plot_surface(R[:,:,0], R[:,:,1], R[:,:,2],
    #                       rstride=1, cstride=1, facecolors=rgb,
    #                       linewidth=0, antialiased=False)
    
    # ax_2.axis('equal')
    
    # canvas_2.draw()