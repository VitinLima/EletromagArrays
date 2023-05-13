# -*- coding: utf-8 -*-
"""
Created on Sat May 13 13:46:04 2023

@author: 160047412
"""

import tkinter as tk
import numpy as np

import matplotlib.pyplot as plt

class FieldResult():
    available_plots = ['2d Graph','2d Contour','3d Surface','2d Polar Graph', '2d Polar Contour', '2d Polar Patch', '3d Polar Surface','3d Polar']
    available_fields = ['F', 'Ftheta', 'Fphi', 'Frhcp', 'Flhcp', 'Fref', 'Fcross', 'Fc']
    # plot_projections = ['2d', '2d', '2d', '3d', '2d', '2d', ]
    def __init__(self,tab,name='New result',
                 antenna=None,analysis=None,
                 field='F',color='Color by magnitude',
                 # projection='3dpolar',
                 plot='2d Polar Patch',
                 in_dB=True,
                 dynamic_scaling_dB=-30,
                 hide_axis=False,
                 preferred_position=None):
        self.name=name
        self.tab=tab
        self.antenna=antenna
        self.analysis=analysis
        self.plot=plot
        self.field=field
        self.color=color
        self.in_dB=in_dB
        self.dynamic_scaling_dB=dynamic_scaling_dB
        self.hide_axis=hide_axis
        self.preferred_position=preferred_position
        
        self.listeners = []
        self.ok = False
        
        self.reference_plane_X = 0.0
        self.reference_plane_Y = 0.0
        self.reference_plane_Z = 1.0
        self.domain = None
        
        if self.antenna is not None:
            self.antenna.listeners.append(self)
        if self.analysis is not None:
            self.analysis.listeners.append(self)
        
        self.axes = None
        self.projection=None
        self.properties = dict()
        self.graphical_objects = None
        self.translate = False
        
        self.tab.add_result(self)
    
    def notify(self, caller, event):
        self.ok = False
        # self.mark_update('"' + str(caller) +'" called notify with event "' + event + '"')
    
    def mark_update(self, event):
        for l in self.listeners:
            # print(str(self) + ' notifying ' + str(l) + ' for ' + event)
            l.notify(self, event)
    
    def get_axes(self, **kw):
        self.properties = dict()
        
        if self.plot=='2d Graph':
            self.projection = '2dcartesian'
            self.axes = self.tab.request_axes(requester=self,
                                              projection=None,
                                              preferred_position=self.preferred_position,
                                              **kw)
            self.properties = {
                    'x label':'x',
                    'y label':'y',
                }
        elif self.plot=='2d Contour':
            self.projection = '2dcartesian'
            self.axes = self.tab.request_axes(requester=self,
                                              projection=None,
                                              preferred_position=self.preferred_position,
                                              **kw)
            self.properties = {
                    'x label':'x',
                    'y label':'y',
                }
        elif self.plot=='3d Surface':
            self.projection = '3dcartesian'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='3d',
                                              preferred_position=self.preferred_position,
                                              **kw)
            self.properties = {
                    'x label':'x',
                    'y label':'y',
                    'z label':'z',
                }
        elif self.plot=='2d Polar Graph':
            self.projection = '2dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection=None,
                                              preferred_position=self.preferred_position,
                                              **kw)
        elif self.plot=='2d Polar Contour':
            self.projection = '2dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection=None,
                                              preferred_position=self.preferred_position,
                                              **kw)
        elif self.plot=='2d Polar Patch':
            self.projection = '2dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection=None,
                                              preferred_position=self.preferred_position,
                                              **kw)
        elif self.plot=='3d Polar Surface':
            self.projection = '3dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='3d',
                                              preferred_position=self.preferred_position,
                                              **kw)
            self.properties = {
                    'x label':'x',
                    'y label':'y',
                    'z label':'z',
                }
        elif self.plot=='3d Polar':
            self.projection = '3dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='3d',
                                              preferred_position=self.preferred_position,
                                              **kw)
            self.properties = {
                    'x label':'x',
                    'y label':'y',
                    'z label':'z',
                }
    
    def update_axes(self):
        if self.projection == '2dpolar':
            if not self.hide_axis:
                thetas = np.sin(np.radians(np.array([10, 45, 60, 90])))
                angles = np.linspace(0,2*np.pi,181)
                for theta in thetas:
                    x = theta*np.cos(angles)
                    y = theta*np.sin(angles)
                    self.axes.plot(x,y,color='#aaaaaa',linewidth=0.3)
                phis = np.radians([0, 45, 90, 135, 180, 225, 270, 315])
                angles = np.sin(np.radians(np.linspace(10,90,2)))
                for phi in phis:
                    x = angles*np.cos(phi)
                    y = angles*np.sin(phi)
                    self.axes.plot(x,y,color='#aaaaaa',linewidth=0.3)
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
    
    def reference_polarization(self, theta, phi):
        sp = np.sin(phi)
        cp = np.cos(phi)
        st = np.sin(theta)
        ct = np.cos(theta)
        hat_i_ref_x = - (1 - ct)*sp*cp
        hat_i_ref_y = (1 - sp*sp*(1 - ct))
        hat_i_ref_z = - st*sp
        hat_i_ref = np.array([hat_i_ref_x, hat_i_ref_y, hat_i_ref_z]).swapaxes(0, 1).swapaxes(1, 2)
        
        hat_i_cross_x = (1 - cp*cp*(1-ct))
        hat_i_cross_y = - (1-ct)*sp*cp
        hat_i_cross_z = - st*cp
        hat_i_cross = np.array([hat_i_cross_x, hat_i_cross_y, hat_i_cross_z]).swapaxes(0, 1).swapaxes(1, 2)
        
        return hat_i_ref, hat_i_cross
    
    def polarization_matrix(self, theta, phi):
        sp = np.sin(phi)
        cp = np.cos(phi)
        st = np.sin(theta)
        ct = np.cos(theta)
        
        a_11 = 1 - st*st*cp*cp
        a_12 = - st*st*sp*cp
        a_13 = - st*ct*cp
        a_21 = - st*st*sp*cp
        a_22 = 1 - st*st*sp*sp
        a_23 = - st*ct*sp
        a_31 = - st*ct*cp
        a_32 = - st*ct*sp
        a_33 = 1 - ct*ct
        matrix = np.array([[a_11, a_12, a_13],
                       [a_21, a_22, a_23],
                       [a_31, a_32, a_33]])
        return matrix.swapaxes(0,2).swapaxes(1,3)
    
    def get_field(self):
        if self.field=='F':
            field = self.antenna.F
        elif self.field=='Ftheta':
            field = self.antenna.Ftheta
        elif self.field=='Fphi':
            field = self.antenna.Fphi
        elif self.field=='Frhcp':
            field = self.antenna.Frhcp
        elif self.field=='Flhcp':
            field = self.antenna.Flhcp
        else:
            F = np.array([self.antenna.Fx, self.antenna.Fy, self.antenna.Fz]).swapaxes(0, 1).swapaxes(1, 2)
            polarization_matrix = self.polarization_matrix(self.antenna.mesh_theta, self.antenna.mesh_phi)
            E = np.squeeze(polarization_matrix@F[:,:,:,np.newaxis])
            
            hat_i_ref, hat_i_cross = self.reference_polarization(self.antenna.mesh_theta, self.antenna.mesh_phi)
            
            if self.field=='Fref':
                field = np.multiply(E, hat_i_ref).sum(2)
            elif self.field=='Fcross':
                field = np.multiply(E, hat_i_cross).sum(2)
            elif self.field=='Fc':
                Fref = np.abs(np.multiply(E, hat_i_ref).sum(2))
                Fcross = np.abs(np.multiply(E, hat_i_cross).sum(2))
                field = np.sqrt(Fref*Fref + Fcross*Fcross) - self.antenna.F
        
        field_phase = np.angle(field)
        field = np.absolute(field)
        if self.in_dB:
            field = 20*np.log10(field)
            field[field<self.dynamic_scaling_dB] = self.dynamic_scaling_dB
        # if self.field=='dnp.log10(self.antenna.F)
        
        if self.color == 'Color by magnitude':
            color=field
        elif self.color == 'Color by phase':
            color=field_phase
        # color = self.analysis.evaluate_color(self.antenna)
        # if str(type(color))=="<class 'NoneType'>":
        #     color = field
        return field,color
    
    def set_antenna(self, antenna):
        # self.undraw()
        if self.antenna is not None:
            self.antenna.listeners.remove(self)
        self.antenna=antenna
        if self.antenna is not None:
            self.antenna.listeners.append(self)
        self.ok = False
        
    def set_analysis(self, analysis):
        # self.undraw()
        if self.analysis is not None:
            self.analysis.listeners.append(self)
        self.analysis=analysis
        if self.analysis is not None:
            self.analysis.listeners.append(self)
        self.ok = False
    
    def set_field(self, field):
        self.field=field
        self.ok = False
    
    def set_color(self, color):
        self.color=color
        self.ok = False
    
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
        
        # self.draw()
        
        # self.tab.request_repaint()
        self.mark_update('Draw')
    
    def draw(self):
        # self.undraw()
        
        if self.antenna==None:
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
        self.get_axes()
        
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
        # self.tab.canvas.draw()
    
    # def undraw(self):
    #     self.figure.clear()
    #     # if self.graphical_objects is not None:
    #     #     if str(type(self.graphical_objects))=="<class 'mpl_toolkits.mplot3d.art3d.Poly3DCollection'>":
    #     #         self.axes.collections.remove(self.graphical_objects)
    #     #     elif str(type(self.graphical_objects))=="<class 'matplotlib.contour.QuadContourSet'>":
    #     #         for c in self.graphical_objects.collections:
    #     #             c.remove()
    #     #     self.graphical_objects = None
    
    def draw_polar_contourf(self):
        field,color = self.get_field()
        
        R = np.degrees(self.antenna.mesh_theta)
        
        x = R*np.cos(self.antenna.mesh_phi)
        y = R*np.sin(self.antenna.mesh_phi)
        
        self.graphical_objects = self.axes.contourf(x,y,field,10,cmap='jet')
    
    def draw_contourf(self):
        field,color = self.get_field()
        
        x = self.antenna.mesh_phi
        y = self.antenna.mesh_theta
        
        self.graphical_objects = self.axes.contourf(x,y,field,10,cmap='jet')
    
    def draw_polar3d(self):
        field,color = self.get_field()
        position = np.array([self.antenna.x,self.antenna.y,self.antenna.z])
        R = field[:,:,np.newaxis]*self.antenna.hat_k
    
        jet = plt.colormaps['jet']
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
        if self.translate:
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
        
        x = np.degrees(self.antenna.mesh_phi)
        y = np.degrees(self.antenna.mesh_theta)
        self.graphical_objects = self.axes.plot_surface(x, y, field,
                              rstride=1, cstride=1, facecolors=rgb,
                              linewidth=0, antialiased=False)
    
    def draw_polar_surface(self):
        field,color = self.get_field()
    
        jet = plt.colormaps['jet']
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
        
        R = np.sin(self.antenna.mesh_theta.copy())
        
        x = R*np.cos(self.antenna.mesh_phi)
        y = R*np.sin(self.antenna.mesh_phi)
        
        self.graphical_objects = self.axes.plot_surface(x, y, field,
                              rstride=1, cstride=1, facecolors=rgb,
                              linewidth=0, antialiased=False)
    
    def draw_polar_patch(self):
        field,color = self.get_field()
        
        R = np.sin(self.antenna.mesh_theta.copy())
        
        x = R*np.cos(self.antenna.mesh_phi)
        y = R*np.sin(self.antenna.mesh_phi)
        
        jet = plt.colormaps['jet']
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
        
        self.graphical_objects = self.axes.pcolormesh(x, y, color,
                                                      shading='gouraud',
                                                      cmap='jet')
        plt.colorbar(self.graphical_objects,ax=self.axes)
        self.axes.set_title(self.name)
    
    def result_menu(self,tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Results', justify='left',
                  relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='edit',command=self.on_result_ppp).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='update',command=self.on_update_result).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='delete',command=self.on_delete_obj).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)