# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 00:43:16 2023

@author: 160047412
"""

import tkinter as tk
import numpy as np
from scipy.interpolate import griddata

# import matplotlib as mpl
import matplotlib.pyplot as plt

import Geometry.Geometry

# font = {
        # 'family':'normal',
        # 'weight':'bold',
#         'size':12}
# mpl.rc('font', **font)


class Result():
    available_plots = ['2d Graph',
                       '2d Contour',
                       '3d Surface',
                       '2d Polar Graph',
                       '2d Polar Contour',
                       '2d Polar Patch',
                       '3d Polar Surface',
                       '3d Polar']
    available_fields = ['F',
                        'Ftheta',
                        'Fphi',
                        'Frhcp',
                        'Flhcp',
                        'Fref',
                        'Fcross',
                        'Ftheta-phi',
                        'Fref-cross']
    # plot_projections = ['2d', '2d', '2d', '3d', '2d', '2d', ]

    def __init__(self, tab, name='New result', title='Title',
                 antenna=None, analysis=None,
                 field='F', color='Color by magnitude',
                 plot='2d Polar Patch',
                 in_dB=True,
                 dynamic_scaling_dB=-30,
                 visible_flag=True,
                 axis_flag=True,
                 grid_flag=True,
                 xaxis_flag=True,
                 yaxis_flag=True,
                 ticks_flag=True,
                 xticks=None,
                 yticks=None,
                 zticks=None,
                 xtick_labels=None,
                 ytick_labels=None,
                 ztick_labels=None,
                 xlabel=None,
                 ylabel=None,
                 zlabel=None,
                 add_colorbar=True,
                 colorbar_min=-30,
                 colorbar_max=0,
                 position=None,
                 column=1, row=1,
                 compare_fields=None,
                 view_camera=None,
                 Ntheta=21,
                 Nphi=21,
                 Nx=21,
                 Ny=21,
                 reference_2d=Geometry.Geometry.ReferenceSystem()):
        self.name = name
        self.title = title
        self.tab = tab
        self.antenna = antenna
        self.analysis = analysis
        self.plot = plot
        self.field = field
        self.color = color
        self.in_dB = in_dB
        self.dynamic_scaling_dB = dynamic_scaling_dB
        self.visible_flag = visible_flag
        self.axis_flag = axis_flag
        self.grid_flag = grid_flag
        self.xaxis_flag = xaxis_flag
        self.yaxis_flag = yaxis_flag
        self.ticks_flag = ticks_flag
        self.xticks = xticks
        self.yticks = yticks
        self.zticks = zticks
        self.xtick_labels = xtick_labels
        self.ytick_labels = ytick_labels
        self.ztick_labels = ztick_labels
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.zlabel = zlabel
        self.add_colorbar = add_colorbar
        self.colorbar_min = colorbar_min
        self.colorbar_max = colorbar_max
        self.position = position
        self.column = column
        self.row = row
        self.compare_fields = compare_fields
        self.view_camera = view_camera
        self.reference_2d = reference_2d
        self.Ntheta = Ntheta
        self.Nphi = Nphi
        self.Nx = Nx
        self.Ny = Ny
        self.labelsize = 20

        self.colorbar_label = ''
        self.listeners = []
        self.ok = False

        self.domain = None

        if self.antenna is not None:
            self.antenna.listeners.append(self)

        self.axes = None
        self.projection = None
        self.properties = dict()
        self.graphical_objects = None
        self.translate = False

        self.custom_draw = None

        self.tab.add_result(self)

    def notify(self, caller, event):
        self.ok = False

    def mark_update(self, event):
        for l in self.listeners:
            l.notify(self, event)

    def get_axes(self, **kw):
        self.properties = dict()

        if self.plot == '2d Graph':
            self.projection = '2dcartesian'
            self.axes = self.tab.request_axes(requester=self,
                                              projection=None,
                                              position=self.position,
                                              column=self.column,
                                              row=self.row,
                                              **kw)
            self.properties = {
                'x label': 'x',
                'y label': 'y',
            }
        elif self.plot == '2d Contour':
            self.projection = '2dcartesian'
            self.axes = self.tab.request_axes(requester=self,
                                              projection=None,
                                              position=self.position,
                                              column=self.column,
                                              row=self.row,
                                              **kw)
            self.properties = {
                'x label': 'x',
                'y label': 'y',
            }
        elif self.plot == '3d Surface':
            self.projection = '3dcartesian'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='3d',
                                              position=self.position,
                                              column=self.column,
                                              row=self.row,
                                              **kw)
            self.properties = {
                'x label': 'x',
                'y label': 'y',
                'z label': 'z',
            }
        elif self.plot == '2d Polar Graph':
            self.projection = '2dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='polar',
                                              position=self.position,
                                              column=self.column,
                                              row=self.row,
                                              **kw)
        elif self.plot == '2d Polar Contour':
            self.projection = '2dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='polar',
                                              position=self.position,
                                              column=self.column,
                                              row=self.row,
                                              **kw)
        elif self.plot == '2d Polar Patch':
            self.projection = '2dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='polar',
                                              position=self.position,
                                              column=self.column,
                                              row=self.row,
                                              **kw)
        elif self.plot == '2d Polar Patch Type 2':
            self.projection = '2dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='polar',
                                              position=self.position,
                                              column=self.column,
                                              row=self.row,
                                              **kw)
        elif self.plot == '3d Polar Surface':
            self.projection = '3dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='3d',
                                              position=self.position,
                                              column=self.column,
                                              row=self.row,
                                              **kw)
            self.properties = {
                'x label': 'x',
                'y label': 'y',
                'z label': 'z',
            }
        elif self.plot == '3d Polar':
            self.projection = '3dpolar'
            self.axes = self.tab.request_axes(requester=self,
                                              projection='3d',
                                              position=self.position,
                                              column=self.column,
                                              row=self.row,
                                              **kw)
            self.properties = {
                'x label': 'x',
                'y label': 'y',
                'z label': 'z',
            }

    def update_axes(self):
        # pass
        # if self.axes is not None:
        #     self.axes.autoscale(enable=True, tight=True)
        #     for k, v in zip(self.properties.keys(),
        #                     self.properties.values()):
        #         if k == 'x label':
        #             self.axes.set_xlabel(v)
        #         elif k == 'y label':
        #             self.axes.set_ylabel(v)
        #         elif k == 'z label':
        #             self.axes.set_zlabel(v)
        #         elif k == 'axis':
        #             self.axes.axis(v)
        # self.axes.set_visible(self.visible_flag)
        # self.axes.grid(self.grid_flag)
        # self.axes.get_xaxis().set_visible(self.xaxis_flag)
        # self.axes.get_yaxis().set_visible(self.yaxis_flag)
        # if not self.ticks_flag:
        #     self.axes.xaxis.set_ticklabels([])
        #     self.axes.yaxis.set_ticklabels([])
        if self.view_camera is not None:
            self.axes.view_init(elev=self.view_camera[0],azim=self.view_camera[1],roll=self.view_camera[2])
        self.axes.axis(self.axis_flag)
        if self.xticks is not None:
            self.axes.set_xticks(self.xticks)
        if self.yticks is not None:
            self.axes.set_yticks(self.yticks)
        if self.zticks is not None:
            self.axes.set_zticks(self.zticks)
        if self.xtick_labels is not None:
            self.axes.set_xticklabels(self.xtick_labels)
        if self.ytick_labels is not None:
            self.axes.set_yticklabels(self.ytick_labels)
        if self.ztick_labels is not None:
            self.axes.set_zticklabels(self.ztick_labels)
        if self.xlabel is not None:
            self.axes.set_xlabel(self.xlabel)
        if self.ylabel is not None:
            self.axes.set_ylabel(self.ylabel)
        if self.zlabel is not None:
            self.axes.set_zlabel(self.zlabel)
        if self.projection == '2dpolar':
            self.axes.grid(False)
            self.axis = []
            r = np.array([0, 90])
            degree_sign = u"\N{DEGREE SIGN}"
            for angle in [0,
                  np.pi/4,
                  np.pi/2,
                  3*np.pi/4,
                  np.pi,
                  -3*np.pi/4,
                  -np.pi/2,
                  -np.pi/4]:
                self.axis.append(self.axes.plot(np.array([angle, angle]), r, 'w', linewidth=0.3))
            a = np.linspace(0, 2*np.pi, 360)
            for radius in self.radius_ticks:
                self.axis.append(self.axes.plot(a, radius*np.ones_like(a), 'w', linewidth=0.3))
            self.axes.set_rticks(self.radius_ticks)
            self.axes.set_yticklabels([str(i) + degree_sign for i in self.radius_ticks])
            # self.axes.set_yticklabels(['$22.5^\circ$', '$45^\circ$', '$66.5^\circ$', '$90^\circ$'])
            # self.axes.set_ylabel(r"$\theta$")
            # self.axes.set_xlabel(r"$\phi$")

    def reference_polarization(self, theta, phi):
        sp = np.sin(phi)
        cp = np.cos(phi)
        st = np.sin(theta)
        ct = np.cos(theta)
        hat_i_ref_x = - (1 - ct)*sp*cp
        hat_i_ref_y = (1 - sp*sp*(1 - ct))
        hat_i_ref_z = - st*sp
        hat_i_ref = np.array([hat_i_ref_x,
                              hat_i_ref_y,
                              hat_i_ref_z]).swapaxes(
            0, 1).swapaxes(1, 2)

        hat_i_cross_x = (1 - cp*cp*(1-ct))
        hat_i_cross_y = - (1-ct)*sp*cp
        hat_i_cross_z = - st*cp
        hat_i_cross = np.array([hat_i_cross_x,
                                hat_i_cross_y,
                                hat_i_cross_z]
                               ).swapaxes(
                                   0, 1).swapaxes(1, 2)

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
        return matrix.swapaxes(0, 2).swapaxes(1, 3)

    def get_field(self, antenna=None, field=None):
        if antenna is None:
            antenna = self.antenna
        if field is None:
            field = self.field

        if field == 'F':
            field = antenna.F
        elif field == 'Ftheta':
            field = antenna.Ftheta
        elif field == 'Fphi':
            field = antenna.Fphi
        elif field == 'Frhcp':
            field = antenna.Frhcp
        elif field == 'Flhcp':
            field = antenna.Flhcp
        else:
            F = np.array([antenna.Fx, antenna.Fy, antenna.Fz]
                         ).swapaxes(0, 1).swapaxes(1, 2)
            polarization_matrix = self.polarization_matrix(
                antenna.mesh_theta, antenna.mesh_phi)
            E = np.squeeze(polarization_matrix@F[:, :, :, np.newaxis])

            hat_i_ref, hat_i_cross = self.reference_polarization(
                antenna.mesh_theta, antenna.mesh_phi)

            if field == 'Fref':
                field = np.multiply(E, hat_i_ref).sum(2)
            elif field == 'Fcross':
                field = np.multiply(E, hat_i_cross).sum(2)
            elif field == 'Fref-Fcross':
                Fref = np.abs(np.multiply(E, hat_i_ref).sum(2))
                Fcross = np.abs(np.multiply(E, hat_i_cross).sum(2))
                field = np.sqrt(Fref*Fref + Fcross*Fcross)
            elif field == 'Ftheta-Fphi':
                Ftheta = np.abs(antenna.Ftheta)
                Fphi = np.abs(antenna.Fphi)
                field = np.sqrt(Ftheta*Ftheta + Fphi*Fphi)

        # field_phase = np.degrees(np.angle(field))
        field_phase = np.angle(field)
        field_mag = np.absolute(field)
        if self.in_dB:
            field_mag = 20*np.log10(field_mag)
            field_mag[field_mag <
                      self.dynamic_scaling_dB] = self.dynamic_scaling_dB
            self.colorbar_label = '[dB]'

        if self.color == 'Color by magnitude':
            color = field_mag
        elif self.color == 'Color by phase':
            color = field_phase
            self.colorbar_label = '[deg]'
        # color = self.analysis.evaluate_color(antenna)
        # if str(type(color))=="<class 'NoneType'>":
        #     color = field
        return field, color

    def set_antenna(self, antenna):
        # self.undraw()
        if self.antenna is not None:
            self.antenna.listeners.remove(self)
        self.antenna = antenna
        if self.antenna is not None:
            self.antenna.listeners.append(self)
        self.ok = False

    # def set_analysis(self, analysis):
    #     # self.undraw()
    #     if self.analysis is not None:
    #         self.analysis.listeners.append(self)
    #     self.analysis = analysis
    #     if self.analysis is not None:
    #         self.analysis.listeners.append(self)
    #     self.ok = False

    def set_field(self, field):
        self.field = field
        self.ok = False

    def set_color(self, color):
        self.color = color
        self.ok = False

    def set_plot(self, plot):
        self.plot = plot
        if self.plot == '2d Graph':
            self.projection = '2dcartesian'
        elif self.plot == '2d Contour':
            self.projection = '2dcartesian'
        elif self.plot == '3d Surface':
            self.projection = '3dcartesian'
        elif self.plot == '2d Polar Graph':
            self.projection = '2dpolar'
        elif self.plot == '2d Polar Contour':
            self.projection = '2dpolar'
        elif self.plot == '2d Polar Patch':
            self.projection = '2dpolar'
        elif self.plot == '2d Polar Patch Type 2':
            self.projection = '2dpolar'
        elif self.plot == '3d Polar Surface':
            self.projection = '3dpolar'
        elif self.plot == '3d Polar':
            self.projection = '3dpolar'
        elif self.plot == 'custom':
            self.projection = self.custom_projection
        self.ok = False
    
    def set_position(self, position=None, row=None, column=None):
        self.position = position
        self.row = row
        self.column = column
        self.ok = False

    def update(self):
        if self.ok:
            return

        # self.draw()

        self.tab.request_repaint()
        self.mark_update('Draw')
        
        self.ok = True

    def draw(self):
        # self.undraw()

        if self.plot == 'custom':
            self.custom_draw(self, self.tab)
            return

        if self.antenna is None and self.plot != 'custom':
            return
        if not self.antenna.ok:
            return

        self.get_axes()

        if self.axes is not None:
            if self.plot == '2d Graph':
                self.draw_graph()
            elif self.plot == '2d Contour':
                self.draw_contourf()
            elif self.plot == '3d Surface':
                self.draw_surface()
            elif self.plot == '2d Polar Graph':
                self.draw_polar_graph()
            elif self.plot == '2d Polar Contour':
                self.draw_polar_contourf()
            elif self.plot == '2d Polar Patch':
                self.draw_polar_patch()
            elif self.plot == '2d Polar Patch Type 2':
                self.draw_polar_patch_type_2()
            elif self.plot == '3d Polar':
                self.draw_polar3d()
            elif self.plot == '3d Polar Surface':
                self.draw_polar_surface()

        self.update_axes()
        # print("Updating result " + str(self) + " " + self.plot)

    def get_2d_field(self, points):
        field, color = self.get_field()

        thetas = np.zeros((181))
        phis = np.zeros((181))
        for i in range(points.shape[0]):
            point = self.reference_2d.R@points[i, :]
            x = point[0]
            y = point[1]
            z = point[2]
            thetas[i] = np.arctan2(np.sqrt(y*y+x*x), z)
            phis[i] = np.arctan2(y, x)

        thetas = np.degrees(thetas)
        phis = np.degrees(phis)
        fit_points = np.ndarray((len(thetas), 2))
        fit_points[:, 0] = thetas
        fit_points[:, 1] = phis

        interp_thetas = np.degrees(self.antenna.mesh_theta).flatten()
        interp_phis = np.degrees(self.antenna.mesh_phi).flatten()
        interp_points = np.ndarray((len(interp_thetas), 2))
        interp_points[:, 0] = interp_thetas
        interp_points[:, 1] = interp_phis

        values = field.flatten()
        if values.dtype == np.dtype('complex64'):
            values = np.array(values, dtype=np.dtype('complex128'))
        field = griddata(interp_points,
                         values,
                         fit_points,
                         method='linear')

        return field

    def draw_graph(self):
        angles = np.radians(np.linspace(-180, 180, 181))
        points = np.zeros((len(angles), 3))
        points[:, 0] = np.cos(angles)
        points[:, 1] = np.sin(angles)

        field = self.get_2d_field(points)

        self.graphical_objects = self.axes.plot(angles, field)

    def draw_polar_graph(self):
        angles = np.radians(np.linspace(-180, 180, 181))
        points = np.zeros((len(angles), 3))
        points[:, 0] = np.cos(angles)
        points[:, 1] = np.sin(angles)

        field = self.get_2d_field(points)

        self.graphical_objects = self.axes.plot(angles, field)

    def draw_polar_contourf(self):
        field, color = self.get_field()

        self.graphical_objects = self.axes.contourf(
            self.antenna.mesh_phi,
            np.degrees(self.antenna.mesh_theta),
            field, 10, cmap='jet')

    def draw_contourf(self):
        field, color = self.get_field()

        x = self.antenna.mesh_phi
        y = self.antenna.mesh_theta

        self.graphical_objects = self.axes.contourf(
            x, y, field, 10, cmap='jet')

    def draw_polar3d(self):
        field, color = self.get_field()

        position = np.array([self.antenna.x,
                             self.antenna.y,
                             self.antenna.z])
        min_field = np.min(field)
        if min_field < 0:
            field -= min_field
        R = field[:, :, np.newaxis]*self.antenna.hat_k

        jet = plt.colormaps['jet']
        color_max = color.max()
        color_min = color.min()
        if color_max != color_min:
            C = (color-color_min)/(color_max-color_min)
            rgb = jet(C)
        else:
            rgb = list(color.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:, :, 3] = 1
            rgb[:, :, 2] = 1
        if self.translate:
            R += position
        self.graphical_objects = self.axes.plot_surface(
            R[:, :, 0], R[:, :, 1], R[:, :, 2],
            rstride=1, cstride=1, facecolors=rgb,
            linewidth=0, antialiased=False)
        self.properties['axis'] = 'equal'

    def draw_surface(self):
        field, color = self.get_field()

        interp_x = np.linspace(0, 90, self.Nx)
        interp_y = np.linspace(-180, 180, self.Ny)

        interp_mesh_x, interp_mesh_y = np.meshgrid(interp_x, interp_y)

        field = self.antenna.interpolate_at(
            interp_mesh_x, interp_mesh_y, field)

        jet = plt.colormaps['jet']
        if str(type(color)) == "<class 'NoneType'>":
            color = field
        color_max = color.max()
        color_min = color.min()
        if color_max != color_min:
            C = (color-color_min)/(color_max-color_min)
            rgb = jet(C)
        else:
            rgb = list(color.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:, :, 3] = 1
            rgb[:, :, 2] = 1

        self.graphical_objects = self.axes.plot_surface(
            interp_mesh_x, interp_mesh_y, field,
            rstride=1, cstride=1, facecolors=rgb,
            linewidth=0, antialiased=False)

    def draw_polar_surface(self):
        field, color = self.get_field()

        interp_theta_deg = np.linspace(0, 90, self.Ntheta)
        interp_phi_deg = np.linspace(-180, 180, self.Nphi)

        interp_mesh_phi_deg, interp_mesh_theta_deg = np.meshgrid(
            interp_phi_deg, interp_theta_deg)

        field = self.antenna.interpolate_at(
            interp_mesh_theta_deg, interp_mesh_phi_deg, field)

        jet = plt.colormaps['jet']
        color_max = color.max()
        color_min = color.min()
        if color_max != color_min:
            C = (color-color_min)/(color_max-color_min)
            rgb = jet(C)
        else:
            rgb = list(color.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:, :, 3] = 1
            rgb[:, :, 2] = 1

        self.graphical_objects = self.axes.plot_surface(
            np.radians(interp_mesh_phi_deg),
            np.sin(np.radians(interp_mesh_theta_deg)),
            field,
            rstride=1, cstride=1, facecolors=rgb,
            linewidth=0, antialiased=False)

    def draw_polar_patch(self):
        field, color = self.get_field()

        interp_theta_deg = np.linspace(0, 90, self.Ntheta)
        interp_phi_deg = np.linspace(-180, 180, self.Nphi)

        interp_mesh_phi_deg, interp_mesh_theta_deg = np.meshgrid(
            interp_phi_deg, interp_theta_deg)

        color = self.antenna.interpolate_at(
            interp_mesh_theta_deg, interp_mesh_phi_deg, color)

        if self.color == 'Color by magnitude':
            cmap = 'jet'
            self.graphical_objects = self.axes.pcolormesh(
                np.radians(interp_mesh_phi_deg),
                90*np.sin(np.radians(interp_mesh_theta_deg)),
                color,
                # norm=norm,
                shading='gouraud',
                cmap=cmap,
                vmin=self.colorbar_min,
                vmax=self.colorbar_max)
            plt.colorbar(self.graphical_objects, ax=self.axes,
                          label=self.colorbar_label, extend='both',
                          pad=0.1)
                           # boundaries=[self.colorbar_min, self.colorbar_max])
        elif self.color == 'Color by phase':
            cmap = 'twilight'
            self.graphical_objects = self.axes.pcolormesh(
                np.radians(interp_mesh_phi_deg),
                90*np.sin(np.radians(interp_mesh_theta_deg)),
                180*color/np.pi,
                # norm=norm,
                shading='gouraud',
                cmap=cmap,
                vmin=-180,
                vmax=180)
            plt.colorbar(self.graphical_objects, ax=self.axes,
                          label=self.colorbar_label, extend='both',
                          # anchor=(0.0, 0.7),
                          pad=0.1)
                           # boundaries=[self.colorbar_min, self.colorbar_max])

        # color_max = color.max()
        # color_min = color.min()
        # if color_max != color_min:
        #     C = (color-color_min)/(color_max-color_min)
        #     rgb = plt.colormaps[cmap](C)
        # else:
        #     rgb = list(color.shape)
        #     rgb.append(4)
        #     rgb = np.zeros(tuple(rgb))
        #     rgb[:, :, 3] = 1
        #     rgb[:, :, 2] = 1
        
        # norm = mpl.colors.BoundaryNorm(boundaries=[self.colorbar_min, self.colorbar_max], ncolors=256)
        self.axes.set_title(self.title)
        self.radius_ticks = [22.5, 45, 66.5, 90]

    def draw_polar_patch_type_2(self):
        field, color = self.get_field()

        if self.color == 'Color by magnitude':
            cmap = 'jet'
        elif self.color == 'Color by phase':
            cmap = 'twilight'

        color_max = color.max()
        color_min = color.min()
        if color_max != color_min:
            C = (color-color_min)/(color_max-color_min)
            rgb = plt.colormaps[cmap](C)
        else:
            rgb = list(color.shape)
            rgb.append(4)
            rgb = np.zeros(tuple(rgb))
            rgb[:, :, 3] = 1
            rgb[:, :, 2] = 1

        self.graphical_objects = self.axes.pcolormesh(
            self.antenna.mesh_phi,
            self.antenna.mesh_theta,
            color,
            shading='gouraud',
            cmap=cmap)
        plt.colorbar(self.graphical_objects, ax=self.axes,
                     label=self.colorbar_label)
        self.axes.set_title(self.title)

    def result_menu(self, tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Results', justify='left',
                 relief='solid', borderwidth=0).pack(
                     ipadx=1, fill=tk.BOTH)
        tk.Button(master=new_menu, text='edit',
                  command=self.on_result_ppp).pack(
                      ipadx=1, fill=tk.BOTH)
        tk.Button(master=new_menu, text='update',
                  command=self.on_update_result).pack(
                      ipadx=1, fill=tk.BOTH)
        tk.Button(master=new_menu, text='delete',
                  command=self.on_delete_obj).pack(
                      ipadx=1, fill=tk.BOTH)
        new_menu.pack(ipadx=1)
