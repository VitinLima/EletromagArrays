# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 00:43:16 2023

@author: 160047412
"""

import tkinter as tk
import numpy as np
from scipy.interpolate import griddata

import matplotlib.pyplot as plt

import Geometry.Geometry

class Result():
    available_plots = ['2d Graph','2d Contour','3d Surface','2d Polar Graph', '2d Polar Contour', '2d Polar Patch', '3d Polar Surface','3d Polar']
    available_fields = ['F', 'Ftheta', 'Fphi', 'Frhcp', 'Flhcp', 'Fref', 'Fcross', 'Ftheta-phi', 'Fref-cross']
    # plot_projections = ['2d', '2d', '2d', '3d', '2d', '2d', ]
    def __init__(self,tab,name='New result',title='Title',
                 antenna=None,analysis=None,
                 field='F',color='Color by magnitude',
                 plot='2d Polar Patch',
                 in_dB=True,
                 dynamic_scaling_dB=-30,
                 visible_flag=True,
                 axis_flag=True,
                 grid_flag=True,
                 xaxis_flag=True,
                 yaxis_flag=True,
                 ticks_flag=True,
                 preferred_position=None,
                 compare_fields=None,
                 reference_2d=Geometry.Geometry.ReferenceSystem()):
        self.name=name
        self.title=title
        self.tab=tab
        self.antenna=antenna
        self.analysis=analysis
        self.plot=plot
        self.field=field
        self.color=color
        self.in_dB=in_dB
        self.dynamic_scaling_dB=dynamic_scaling_dB
        self.visible_flag=visible_flag
        self.axis_flag=axis_flag
        self.grid_flag=grid_flag
        self.xaxis_flag=xaxis_flag
        self.yaxis_flag=yaxis_flag
        self.ticks_flag=ticks_flag
        self.preferred_position=preferred_position
        self.compare_fields=compare_fields
        self.reference_2d=reference_2d
        
        self.colorbar_label = ''
        self.listeners = []
        self.ok = False
        
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
        
        self.custom_draw = None
        
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
                                              projection='polar',
                                              preferred_position=self.preferred_position,
                                              **kw)
        elif self.plot=='2d Polar Contour':
            self.projection = '2dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='polar',
                                              preferred_position=self.preferred_position,
                                              **kw)
        elif self.plot=='2d Polar Patch':
            self.projection = '2dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='polar',
                                              preferred_position=self.preferred_position,
                                              **kw)
        elif self.plot=='2d Polar Patch Type 2':
            self.projection = '2dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='polar',
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
        # if self.projection == '2dpolar':
        #     if not self.axis_flag:
        #         thetas = np.sin(np.radians(np.array([10, 45, 60, 90])))
        #         angles = np.linspace(0,2*np.pi,181)
        #         for theta in thetas:
        #             x = theta*np.cos(angles)
        #             y = theta*np.sin(angles)
        #             self.axes.plot(x,y,color='#aaaaaa',linewidth=0.3)
        #         phis = np.radians([0, 45, 90, 135, 180, 225, 270, 315])
        #         angles = np.sin(np.radians(np.linspace(10,90,2)))
        #         for phi in phis:
        #             x = angles*np.cos(phi)
        #             y = angles*np.sin(phi)
        #             self.axes.plot(x,y,color='#aaaaaa',linewidth=0.3)
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
        self.axes.set_visible(self.visible_flag)
        self.axes.axis(self.axis_flag)
        self.axes.grid(self.grid_flag)
        self.axes.get_xaxis().set_visible(self.xaxis_flag)
        self.axes.get_yaxis().set_visible(self.yaxis_flag)
        if not self.ticks_flag:
            self.axes.xaxis.set_ticklabels([])
            self.axes.yaxis.set_ticklabels([])
        if self.projection=='2dpolar':
            self.axes.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, -3*np.pi/4, -np.pi/2, -np.pi/4])
    
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
    
    def get_field(self, antenna=None):
        if antenna==None:
            antenna=self.antenna
        
        if self.field=='F':
            field = antenna.F
        elif self.field=='Ftheta':
            field = antenna.Ftheta
        elif self.field=='Fphi':
            field = antenna.Fphi
        elif self.field=='Frhcp':
            field = antenna.Frhcp
        elif self.field=='Flhcp':
            field = antenna.Flhcp
        else:
            F = np.array([antenna.Fx, antenna.Fy, antenna.Fz]).swapaxes(0, 1).swapaxes(1, 2)
            polarization_matrix = self.polarization_matrix(antenna.mesh_theta, antenna.mesh_phi)
            E = np.squeeze(polarization_matrix@F[:,:,:,np.newaxis])
            
            hat_i_ref, hat_i_cross = self.reference_polarization(antenna.mesh_theta, antenna.mesh_phi)
            
            if self.field=='Fref':
                field = np.multiply(E, hat_i_ref).sum(2)
            elif self.field=='Fcross':
                field = np.multiply(E, hat_i_cross).sum(2)
            elif self.field=='Fref-Fcross':
                Fref = np.abs(np.multiply(E, hat_i_ref).sum(2))
                Fcross = np.abs(np.multiply(E, hat_i_cross).sum(2))
                field = np.sqrt(Fref*Fref + Fcross*Fcross)
            elif self.field=='Ftheta-Fphi':
                Ftheta = np.abs(antenna.Ftheta)
                Fphi = np.abs(antenna.Fphi)
                field = np.sqrt(Ftheta*Ftheta + Fphi*Fphi)
        
        # field_phase = np.degrees(np.angle(field))
        field_phase = np.angle(field)
        field_mag = np.absolute(field)
        if self.in_dB:
            field_mag = 20*np.log10(field_mag)
            field_mag[field_mag < self.dynamic_scaling_dB] = self.dynamic_scaling_dB
            self.colorbar_label = '[dB]'
        # if self.field=='dnp.log10(antenna.F)
        
        if self.color == 'Color by magnitude':
            color=field_mag
        elif self.color == 'Color by phase':
            color=field_phase
            self.colorbar_label = '[deg]'
        # color = self.analysis.evaluate_color(antenna)
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
        elif self.plot=='2d Polar Patch Type 2':
            self.projection = '2dpolar'
        elif self.plot=='3d Polar Surface':
            self.projection = '3dpolar'
        elif self.plot=='3d Polar':
            self.projection = '3dpolar'
        elif self.plot=='custom':
            self.projection = self.custom_projection
    
    def update(self):
        if self.ok:
            return
        
        self.ok = True
        
        # self.draw()
        
        # self.tab.request_repaint()
        self.mark_update('Draw')
    
    def draw(self):
        # self.undraw()
        
        if self.plot=='custom':
            self.custom_draw(self, self.tab)
            return
        
        if self.antenna==None and self.plot != 'custom':
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
            elif self.plot=='2d Polar Patch Type 2':
                self.draw_polar_patch_type_2()
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
    
    def get_2d_field(self, points):
        field,color = self.get_field()
        
        thetas = np.zeros((181))
        phis = np.zeros((181))
        for i in range(points.shape[0]):
            point = self.reference_2d.R@points[i,:]
            x = point[0]
            y = point[1]
            z = point[2]
            thetas[i] = np.arctan2(np.sqrt(y*y+x*x), z)
            phis[i] = np.arctan2(y, x)
        
        thetas = np.degrees(thetas)
        phis = np.degrees(phis)
        fit_points = np.ndarray((len(thetas),2))
        fit_points[:,0] = thetas
        fit_points[:,1]= phis
        
        interp_thetas = np.degrees(self.antenna.mesh_theta).flatten()
        interp_phis = np.degrees(self.antenna.mesh_phi).flatten()
        interp_points = np.ndarray((len(interp_thetas),2))
        interp_points[:,0] = interp_thetas
        interp_points[:,1] = interp_phis
        
        values = field.flatten()
        if values.dtype==np.dtype('complex64'):
            values = np.array(values,dtype=np.dtype('complex128'))
        field = griddata(interp_points, values, fit_points, method='linear')
        
        return field
    
    def interpolate_field(mesh_theta, mesh_phi, field):
        i_theta = np.linspace(0, 180, 21)
        i_phi = np.linspace(-180,180, 21)
    
    def draw_graph(self):
        angles = np.radians(np.linspace(-180,180,181))
        points = np.zeros((len(angles),3))
        points[:,0] = np.cos(angles)
        points[:,1] = np.sin(angles)
        
        field = self.get_2d_field(points)
        
        self.graphical_objects = self.axes.plot(angles, field)
    
    def draw_polar_graph(self):
        angles = np.radians(np.linspace(-180,180,181))
        points = np.zeros((len(angles),3))
        points[:,0] = np.cos(angles)
        points[:,1] = np.sin(angles)
        
        field = self.get_2d_field(points)
        # min_field = np.min(field)
        # if min_field < 0:
        #     field -= min_field
        
        # points = field[:,np.newaxis]*points
        
        self.graphical_objects = self.axes.plot(angles, field)
    
    def draw_polar_contourf(self):
        field,color = self.get_field()
        
        # R = np.degrees(self.antenna.mesh_theta)
        
        # x = R*np.cos(self.antenna.mesh_phi)
        # y = R*np.sin(self.antenna.mesh_phi)
        
        self.graphical_objects = self.axes.contourf(self.antenna.mesh_phi,
                                                    np.degrees(self.antenna.mesh_theta),
                                                    field,10,cmap='jet')
    
    def draw_contourf(self):
        field,color = self.get_field()
        
        x = self.antenna.mesh_phi
        y = self.antenna.mesh_theta
        
        self.graphical_objects = self.axes.contourf(x,y,field,10,cmap='jet')
    
    def draw_polar3d(self):
        field,color = self.get_field()
        
        # interp_theta_deg = np.linspace(0,180,61)
        # interp_phi_deg = np.linspace(-180,180,61)
        
        # interp_mesh_phi_deg,interp_mesh_theta_deg = np.meshgrid(interp_phi_deg,interp_theta_deg)
        
        # interp_mesh_theta_rad = np.pi*interp_mesh_theta_deg/180
        # interp_mesh_phi_rad = np.pi*interp_mesh_phi_deg/180
        
        # ct = np.cos(interp_mesh_theta_rad)
        # st = np.sin(interp_mesh_theta_rad)
        # cp = np.cos(interp_mesh_phi_rad)
        # sp = np.sin(interp_mesh_phi_rad)
        # interp_hat_k = np.zeros((len(interp_theta_deg), len(interp_phi_deg), 3))
        # interp_hat_k[:,:,0] = st*cp
        # interp_hat_k[:,:,1] = st*sp
        # interp_hat_k[:,:,2] = ct
        
        # field = self.antenna.interpolate_at(interp_mesh_theta_deg, interp_mesh_phi_deg, field)
        
        position = np.array([self.antenna.x,self.antenna.y,self.antenna.z])
        min_field = np.min(field)
        if min_field < 0:
            field -= min_field
        R = field[:,:,np.newaxis]*self.antenna.hat_k
        # R = field[:,:,np.newaxis]*interp_hat_k
    
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
        field,color = self.get_field()
        
        interp_x = np.linspace(0,90,21)
        interp_y = np.linspace(-180,180,21)
        
        interp_mesh_x,interp_mesh_y = np.meshgrid(interp_x,interp_y)
        
        field = self.antenna.interpolate_at(interp_mesh_x, interp_mesh_y, field)
    
        jet = plt.colormaps['jet']
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
        
        # x = np.degrees(self.antenna.mesh_phi)
        # y = np.degrees(self.antenna.mesh_theta)
        self.graphical_objects = self.axes.plot_surface(interp_mesh_x, interp_mesh_y, field,
                                                        rstride=1, cstride=1, facecolors=rgb,
                                                        linewidth=0, antialiased=False)
    
    def draw_polar_surface(self):
        field,color = self.get_field()
        
        interp_theta_deg = np.linspace(0,90,21)
        interp_phi_deg = np.linspace(-180,180,21)
        
        interp_mesh_phi_deg,interp_mesh_theta_deg = np.meshgrid(interp_phi_deg,interp_theta_deg)
        
        field = self.antenna.interpolate_at(interp_mesh_theta_deg, interp_mesh_phi_deg, field)
    
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
        
        # R = np.sin(self.antenna.mesh_theta.copy())
        
        # x = R*np.cos(self.antenna.mesh_phi)
        # y = R*np.sin(self.antenna.mesh_phi)
        
        self.graphical_objects = self.axes.plot_surface(np.radians(interp_mesh_phi_deg),
                                                        np.sin(np.radians(interp_mesh_theta_deg)),
                                                        field,
                                                        rstride=1, cstride=1, facecolors=rgb,
                                                        linewidth=0, antialiased=False)
    
    def draw_polar_patch(self):
        field,color = self.get_field()
        
        interp_theta_deg = np.linspace(0,90,21)
        interp_phi_deg = np.linspace(-180,180,21)
        
        interp_mesh_phi_deg,interp_mesh_theta_deg = np.meshgrid(interp_phi_deg,interp_theta_deg)
        
        color = self.antenna.interpolate_at(interp_mesh_theta_deg, interp_mesh_phi_deg, color)
        
        if self.color=='Color by magnitude':
            cmap = 'jet'
        elif self.color=='Color by phase':
            cmap = 'twilight'
        
        color_max = color.max()
        color_min = color.min()
        if color_max!=color_min:
            C = (color-color_min)/(color_max-color_min)
            rgb = plt.colormaps[cmap](C)
        else:
            rgb = list(color.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:,:,3] = 1
            rgb[:,:,2] = 1
        
        self.graphical_objects = self.axes.pcolormesh(np.radians(interp_mesh_phi_deg),
                                                      np.sin(np.radians(interp_mesh_theta_deg)),
                                                      color,
                                                      shading='gouraud',
                                                      cmap=cmap)
        plt.colorbar(self.graphical_objects,ax=self.axes,label=self.colorbar_label)
        self.axes.set_title(self.title)
    
    def draw_polar_patch_type_2(self):
        field,color = self.get_field()
        
        if self.color=='Color by magnitude':
            cmap = 'jet'
        elif self.color=='Color by phase':
            cmap = 'twilight'
        
        color_max = color.max()
        color_min = color.min()
        if color_max!=color_min:
            C = (color-color_min)/(color_max-color_min)
            rgb = plt.colormaps[cmap](C)
        else:
            rgb = list(color.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:,:,3] = 1
            rgb[:,:,2] = 1
        
        # i_phi, i_theta, i_c = self.interpolate_field(self.antenna.mesh_phi, self.antenna.mesh_theta, color)
        
        self.graphical_objects = self.axes.pcolormesh(self.antenna.mesh_phi,
                                                      self.antenna.mesh_theta,
                                                      color,
                                                      shading='gouraud',
                                                      cmap=cmap)
        plt.colorbar(self.graphical_objects,ax=self.axes,label=self.colorbar_label)
        self.axes.set_title(self.title)
    
    def result_menu(self,tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Results', justify='left',
                  relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='edit',command=self.on_result_ppp).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='update',command=self.on_update_result).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='delete',command=self.on_delete_obj).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)