# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:19:19 2023

@author: 160047412
"""

import tkinter as tk
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

class ResultFrame(tk.Frame):
    available_plots = ['2d Graph','2d Contour','3d Surface','2d Polar Graph', '2d Polar Contour', '2d Polar Patch', '3d Polar Surface','3d Polar']
    def __init__(self,master=None,name='New result',
                 antenna=None,analysis=None,
                 # projection='3dpolar',
                 plot='3d Polar',**kw):
        tk.Frame.__init__(self, master, width=300, height=200, **kw)
        self.name=name
        self.antenna=antenna
        self.analysis=analysis
        self.plot=plot
        
        self.listeners = []
        self.ok = False
        
        if self.antenna is not None:
            self.antenna.listeners.append(self)
        if self.analysis is not None:
            self.analysis.listeners.append(self)
        
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.axes = None
        self.projection=None
        self.properties = dict()
        self.graphical_objects = None
        self.add_position = False
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)  # A tk.DrawingArea.
        self.canvas.draw()
        
        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        
        self.canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        self.canvas.mpl_connect("key_press_event", key_press_handler)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def notify(self, caller, event):
        self.ok = False
        self.mark_update('"' + str(caller) +'" called notify with event "' + event + '"')
    
    def mark_update(self, event):
        for l in self.listeners:
            print(str(self) + ' notifying ' + str(l) + ' for ' + event)
            l.notify(self)
    
    def add_axes(self, **kw):
        projection = None
        self.properties = dict()
        
        if self.projection==None:
            if self.plot=='2d Graph':
                self.projection = '2dcartesian'
            elif self.plot=='2d Contour':
                self.projection = '2dcartesian'
            elif self.plot=='3d Surface':
                self.projection = '3dcartesian'
            elif self.plot=='2d Polar Graph':
                self.projection = '2dpolar'
            elif self.plot=='2d Polar Contour':
                self.projection = '2dpolar'
            elif self.plot=='2d Polar Patch':
                self.projection = '2dpolar'
            elif self.plot=='3d Polar Surface':
                self.projection = '3dpolar'
            elif self.plot=='3d Polar':
                self.projection = '3dpolar'
        
        if self.projection=='2d' or self.projection=='2dcartesian':
            projection = None
            self.properties = {
                    'x label':'x',
                    'y label':'y',
                }
        elif self.projection=='3dpolar':
            projection='3d'
            self.properties = {
                    'x label':'x',
                    'y label':'y',
                    'z label':'z',
                }
        elif self.projection=='3d' or self.projection=='3dcartesian':
            projection='3d'
            self.properties = {
                    'x label':'x',
                    'y label':'y',
                    'z label':'z',
                }
        
        if self.axes is not None:
            self.axes.set_visible(False)
        self.axes = self.figure.add_subplot(projection=projection,**kw)
    
    def update_axes(self):
        # if self.projection == '2dpolar':
        #     thetas = [0, 45, 90, 135, 180]
        #     angles = np.linspace(0,2*np.pi,181)
        #     for theta in thetas:
        #         x = theta*np.cos(angles)
        #         y = theta*np.sin(angles)
        #         self.axes.plot(x,y,color='white')
        #     phis = np.radians([0, 45, 90, 135, 180, 225, 270, 315])
        #     angles = np.linspace(0,180,2)
        #     for phi in phis:
        #         x = angles*np.cos(phi)
        #         y = angles*np.sin(phi)
        #         self.axes.plot(x,y,color='white')
        if self.axes is not None:
            self.axes.autoscale(enable=True,tight=True)
            for k,v in zip(self.properties.keys(),self.properties.values()):
                if k=='x label':
                    self.axes.set_xlabel(v)
                elif k=='y label':
                    self.axes.set_ylabel(v)
                elif k=='z label':
                    self.axes.set_zlabel(v)
                elif k=='axis':
                    self.axes.axis(v)
        self.canvas.draw()
    
    def set_antenna(self, antenna):
        self.undraw()
        if self.antenna is not None:
            self.antenna.listeners.remove(self)
        self.antenna=antenna
        if self.antenna is not None:
            self.antenna.listeners.append(self)
        
    def set_analysis(self, analysis):
        self.undraw()
        if self.analysis is not None:
            self.analysis.listeners.append(self)
        self.analysis=analysis
        if self.analysis is not None:
            self.analysis.listeners.append(self)
    
    def set_plot(self, plot):
        self.plot = plot
        if self.plot=='2d Graph':
            self.projection = '2dcartesian'
        elif self.plot=='2d Contour':
            self.projection = '2dcartesian'
        elif self.plot=='3d Surface':
            self.projection = '3dcartesian'
        elif self.plot=='2d Polar Graph':
            self.projection = '2dpolar'
        elif self.plot=='2d Polar Contour':
            self.projection = '2dpolar'
        elif self.plot=='2d Polar Patch':
            self.projection = '2dpolar'
        elif self.plot=='3d Polar Surface':
            self.projection = '3dpolar'
        elif self.plot=='3d Polar':
            self.projection = '3dpolar'
    
    def update(self):
        if self.ok:
            return
        
        self.ok = True
        
        self.draw()
        
        self.mark_update('Draw')
    
    def draw(self):
        self.undraw()
        
        if self.antenna==None or self.analysis==None:
            return
        if not self.antenna.ok:
            return
        
        # if self.axes is None:
        #     if self.result_frame is not None:
        #         self.axes = self.result_frame.request_axes(projection=self.projection)
        #     else:
        #         return
        # elif self.result_frame is not None:
        #     if self.result_frame.query_projection(self.axes)!=self.projection:
        #         self.axes = self.result_frame.request_axes(projection=self.projection)
        #     else:
        #         return
        self.add_axes()
        
        
        if self.axes is not None:
            if self.plot=='2d Graph':
                self.draw_graph()
            elif self.plot=='2d Contour':
                self.draw_contourf()
            elif self.plot=='3d Surface':
                self.draw_surface()
            elif self.plot=='2d Polar Graph':
                self.draw_polar_graph()
            elif self.plot=='2d Polar Contour':
                self.draw_polar_contourf()
            elif self.plot=='2d Polar Patch':
                self.draw_polar_patch()
            elif self.plot=='3d Polar':
                self.draw_polar3d()
            elif self.plot=='3d Polar Surface':
                self.draw_polar_surface()
        
        self.update_axes()
        self.canvas.draw()
    
    def undraw(self):
        self.figure.clear()
        # if self.graphical_objects is not None:
        #     if str(type(self.graphical_objects))=="<class 'mpl_toolkits.mplot3d.art3d.Poly3DCollection'>":
        #         self.axes.collections.remove(self.graphical_objects)
        #     elif str(type(self.graphical_objects))=="<class 'matplotlib.contour.QuadContourSet'>":
        #         for c in self.graphical_objects.collections:
        #             c.remove()
        #     self.graphical_objects = None
    
    def draw_polar_contourf(self):
        field = self.analysis.evaluate_field(self.antenna)
        field[field<1e-3] = 0
        
        R = np.degrees(self.antenna.mesh_theta)
        
        x = R*np.cos(self.antenna.mesh_phi)
        y = R*np.sin(self.antenna.mesh_phi)
        
        self.graphical_objects = self.axes.contourf(x,y,field,10,cmap='jet')
    
    def draw_contourf(self):
        field = self.analysis.evaluate_field(self.antenna)
        field[field<1e-3] = 0
        
        x = self.antenna.mesh_phi.copy()
        y = self.antenna.mesh_theta.copy()
        self.graphical_objects = self.axes.contourf(x,y,field,10,cmap='jet')
    
    def draw_polar3d(self):
        field = self.analysis.evaluate_field(self.antenna)
        field[field<1e-3] = 0
        position = np.array([self.antenna.x,self.antenna.y,self.antenna.z])
        R = field[:,:,np.newaxis]*self.antenna.hat_k
    
        jet = plt.colormaps['jet']
        color = self.analysis.evaluate_color(self.antenna)
        if str(type(color))=="<class 'NoneType'>":
            color = field
        color_max = color.max()
        color_min = color.min()
        if color_max!=color_min:
            C = (color-color_min)/(color_max-color_min)
            rgb = jet(C)
        else:
            rgb = list(color.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:,:,3] = 1
            rgb[:,:,2] = 1
        if self.add_position:
            R += position
        self.graphical_objects = self.axes.plot_surface(R[:,:,0], R[:,:,1], R[:,:,2],
                              rstride=1, cstride=1, facecolors=rgb,
                              linewidth=0, antialiased=False)
        self.properties['axis'] = 'equal'
    
    def draw_surface(self):
        field = self.analysis.evaluate_field(self.antenna)
        field[field<1e-3] = 0
    
        jet = plt.colormaps['jet']
        color = self.analysis.evaluate_color(self.antenna)
        if str(type(color))=="<class 'NoneType'>":
            color = field
        color_max = color.max()
        color_min = color.min()
        if color_max!=color_min:
            C = (color-color_min)/(color_max-color_min)
            rgb = jet(C)
        else:
            rgb = list(color.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:,:,3] = 1
            rgb[:,:,2] = 1
        
        x = np.degrees(self.antenna.mesh_phi.copy())
        y = np.degrees(self.antenna.mesh_theta.copy())
        self.graphical_objects = self.axes.plot_surface(x, y, field,
                              rstride=1, cstride=1, facecolors=rgb,
                              linewidth=0, antialiased=False)
    
    def draw_polar_surface(self):
        field = self.analysis.evaluate_field(self.antenna)
        field[field<1e-3] = 0
    
        jet = plt.colormaps['jet']
        color = self.analysis.evaluate_color(self.antenna)
        if str(type(color))=="<class 'NoneType'>":
            color = field
        color_max = color.max()
        color_min = color.min()
        if color_max!=color_min:
            C = (color-color_min)/(color_max-color_min)
            rgb = jet(C)
        else:
            rgb = list(color.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:,:,3] = 1
            rgb[:,:,2] = 1
        
        R = np.degrees(self.antenna.mesh_theta.copy())
        
        x = R*np.cos(self.antenna.mesh_phi.copy())
        y = R*np.sin(self.antenna.mesh_phi.copy())
        
        self.graphical_objects = self.axes.plot_surface(x, y, field,
                              rstride=1, cstride=1, facecolors=rgb,
                              linewidth=0, antialiased=False)
    
    def draw_polar_patch(self):
        field = self.analysis.evaluate_field(self.antenna, in_dB=True)
        field[field<-30] = -30
        
        R = np.degrees(self.antenna.mesh_theta.copy())
        
        x = R*np.cos(self.antenna.mesh_phi.copy())
        y = R*np.sin(self.antenna.mesh_phi.copy())
    
        jet = plt.colormaps['jet']
        color = self.analysis.evaluate_color(self.antenna)
        if str(type(color))=="<class 'NoneType'>":
            color = field
        color_max = color.max()
        color_min = color.min()
        if color_max!=color_min:
            C = (color-color_min)/(color_max-color_min)
            rgb = jet(C)
        else:
            rgb = list(color.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:,:,3] = 1
            rgb[:,:,2] = 1
        
        self.graphical_objects = self.axes.pcolormesh(x, y, field,
                                                      shading='gouraud',
                                                      cmap='jet')
        plt.colorbar(self.graphical_objects,ax=self.axes)