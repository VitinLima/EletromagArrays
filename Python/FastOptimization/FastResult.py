# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 00:10:50 2023

@author: 160047412
"""

import tkinter as tk
import numpy as np

import matplotlib.pyplot as plt

from ResultFrame import ResultFrame

class Result:
    def __init__(self,name='New result',antenna=None,analysis=None,result_frame=None,axes=None):
        self.name=name
        self.antenna=antenna
        self.analysis=analysis
        self.result_frame=result_frame
        
        self.listeners = []
        self.ok = False
        self.projection='2dpolar'
        self.plot = 'Polar Patch'
        self.axes = None
        self.graphical_objects = None
        self.add_position = False
        
        if self.antenna is not None:
            self.antenna.listeners.append(self)
        if self.analysis is not None:
            self.analysis.listeners.append(self)
        
        if self.result_frame is not None:
            self.result_frame.add_result(self)
        elif axes is not None:
            self.axes = axes
    
    def notify(self, caller, event):
        self.ok = False
        self.mark_update('"' + str(caller) +'" called notify with event "' + event + '"')
    
    def mark_update(self, event):
        for l in self.listeners:
            # print(str(self) + ' notifying ' + str(l) + ' for ' + event)
            l.notify(self)
    
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
    
    def set_result_frame(self, result_frame):
        self.undraw()
        if self.result_frame is not None:
            self.result_frame.remove_result(self)
        self.result_frame = result_frame
        if self.result_frame is not None:
            self.result_frame.add_result(self)
            self.axes = self.result_frame.request_axes(projection=self.projection)
    
    def set_axes(self, axes):
        self.undraw()
        if self.result_frame is not None:
            self.result_frame.remove_result(self)
            self.result_frame = None
        self.axes = axes
    
    def set_plot(self, plot):
        self.plot = plot
        if self.plot=='Graph':
            self.projection = '2dcartesian'
        elif self.plot=='Contour':
            self.projection = '2dcartesian'
        elif self.plot=='Surface':
            self.projection = '3dcartesian'
        elif self.plot=='Polar Graph':
            self.projection = '2dpolar'
        elif self.plot=='Polar Contour':
            self.projection = '2dpolar'
        elif self.plot=='Polar 3D':
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
        
        true = False
        false = True
        request_new_axes = not false
        if self.axes is None:
            if self.result_frame is not None:
                self.axes = self.result_frame.request_axes(projection=self.projection)
            else:
                return
        elif self.result_frame is not None:
            if self.result_frame.query_projection(self.axes)!=self.projection:
                self.axes = self.result_frame.request_axes(projection=self.projection)
            else:
                return
        
        if self.axes is not None:
            if self.plot=='Graph':
                self.draw_graph()
            elif self.plot=='Contour':
                self.draw_contourf()
            elif self.plot=='Surface':
                self.draw_surface()
            elif self.plot=='Polar Graph':
                self.draw_polar_graph()
            elif self.plot=='Polar Contour':
                self.draw_polar_contourf()
            elif self.plot=='Polar 3D':
                self.draw_polar3d()
            elif self.plot=='Polar Surface':
                self.draw_polar_surface()
            elif self.plot=='Polar Patch':
                self.draw_polar_patch()
        
        if self.result_frame is not None:
            self.result_frame.update_axes(self.axes)
    
    def undraw(self):
        if self.graphical_objects is not None:
            if str(type(self.graphical_objects))=="<class: 'mpl_toolkits.mplot3d.art3d.Poly3DCollection'>":
                self.axes.collections.remove(self.graphical_objects)
            elif str(type(self.graphical_objects))=="<class 'matplotlib.contour.QuadContourSet'>":
                for c in self.graphical_objects.collections:
                    c.remove()
            self.graphical_objects = None
    
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
        
        x = self.antenna.mesh_phi.copy()
        y = self.antenna.mesh_theta.copy()
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
        field = self.analysis.evaluate_field(self.antenna)
        field[field<1e-3] = 0

        # jet = plt.colormaps['jet']
        # color = self.analysis.evaluate_color(self.antenna)
        # if str(type(color))=="<class 'NoneType'>":
        #     color = field
        # color_max = color.max()
        # color_min = color.min()
        # if color_max!=color_min:
        #     C = (color-color_min)/(color_max-color_min)
        #     rgb = jet(C)
        # else:
        #     rgb = list(color.shape)
        #     rgb.append(4)
        #     rgb = np.zeros(tuple(rgb))
        #     rgb[:,:,3] = 1
        #     rgb[:,:,2] = 1
        
        R = np.degrees(self.antenna.mesh_theta.copy())
        
        x = R*np.cos(self.antenna.mesh_phi.copy())
        y = R*np.sin(self.antenna.mesh_phi.copy())
        
        self.graphical_objects = self.axes.pcolormesh(x, y, field,
                                                      cmap='jet')

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
    
    antenna = Antenna(constants=constants)
    analysis = Analysis()
    
    root = tk.Tk()
    root.wm_title("Embedding in Tk")
    fr = ResultFrame(master=root)
    fr.pack()
    fr.add_axes(projection='3d')
    result = Result(frame=fr,antenna=antenna,analysis=analysis)
    result.update()
    fr.canvas.draw()
    
    antenna.set_orientation(elevation=45,azimuth=27)
    result.update()
    fr.canvas.draw()
    
    root.mainloop()