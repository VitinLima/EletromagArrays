# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 17:49:39 2023

@author: 160047412
"""

import numpy as np
from scipy.interpolate import RegularGridInterpolator

import Antenna
import MyMath
import ArrayEditorFrame
# import scope_fields

# constants, name='new array',
#              current_mag=1,current_phase=0,
#              theta=np.linspace(0, 180, 21), phi=np.linspace(-180, 180, 21),
#              elevation=0, azimuth=0,
#              x=0, y=0, z=0,
            
# constants=constants, name=name, current_mag=current_mag, current_phase=current_phase, phi=phi, theta=theta, elevation=elevation, azimuth=azimuth, x=x, y=y, z=z

class Array(Antenna.Antenna):
    EditorFrame = ArrayEditorFrame.ArrayEditorFrame
    def __init__(self, constants=None, antennas=None,
                 x_mirror=False,
                 y_mirror=False,
                 z_mirror=False,
                 current_mirror=False,
                 azimuth_symmetry=False, **kw):
        if 'name' not in kw.keys():
            kw['name'] = 'new array'
        Antenna.Antenna.__init__(self, **kw)
        
        if antennas is not None:
            self.antennas = antennas
        else:
            self.antennas = []
        self.x_mirror=x_mirror
        self.y_mirror=y_mirror
        self.z_mirror=z_mirror
        self.current_mirror=current_mirror
        self.azimuth_symmetry=azimuth_symmetry
    
    def set_symmetry(self,
                        x_mirror=None,
                        y_mirror=None,
                        z_mirror=None,
                        current_mirror=None,
                        azimuth_symmetry=None):
        if x_mirror is not None:
            self.x_mirror=x_mirror
        if y_mirror is not None:
            self.y_mirror=y_mirror
        if z_mirror is not None:
            self.z_mirror=z_mirror
        if current_mirror is not None:
            self.current_mirror=current_mirror
        if azimuth_symmetry is not None:
            self.azimuth_symmetry=azimuth_symmetry
        
        self.local_field_flag = True
    
    def add_antenna(self, antenna):
        self.antennas.append(antenna)
        antenna.listeners.append(self)
        self.mark_update('antenna added')
    
    def evaluate_local_field(self):
        if len(self.antennas)==0:
            return
        
        self.local_field_flag = False
        
        self.local_Fphi = np.zeros(self.local_shape)
        self.local_Ftheta = np.zeros(self.local_shape)
        
        for antenna in self.antennas:
            antenna.evaluate()
            
            # fit_points = (antenna.theta, antenna.phi)
            # interp_points = (np.degrees(self.local_mesh_theta), np.degrees(self.local_mesh_phi))
            
            # values = antenna.Ftheta
            # if values.dtype==np.dtype('complex64'):
            #     values = np.array(values,dtype=np.dtype('complex128'))
            # interp = RegularGridInterpolator(fit_points, values, method='linear')
            # Ftheta = interp(interp_points)
            Ftheta = antenna.interpolate_at(np.degrees(self.local_mesh_theta), np.degrees(self.local_mesh_phi), antenna.Ftheta)
            
            # values = antenna.Fphi
            # if values.dtype==np.dtype('complex64'):
            #     values = np.array(values,dtype=np.dtype('complex128'))
            # interp = RegularGridInterpolator(fit_points, values, method='linear')
            # Fphi = interp(interp_points)
            Fphi = antenna.interpolate_at(np.degrees(self.local_mesh_theta), np.degrees(self.local_mesh_phi), antenna.Fphi)
            
            x = antenna.x
            y = antenna.y
            z = antenna.z
            phase = np.radians(antenna.current_phase)
            current = antenna.current_mag*(np.cos(phase) + 1j*np.sin(phase))
            
            p0 = Antenna.constants['lam']*np.array([x,y,z]).reshape((1,1,3))
            Af = current*np.exp(1j*Antenna.constants['k']*(self.local_hat_k*p0).sum(2))
            
            self.local_Ftheta = self.local_Ftheta + Af*Ftheta
            self.local_Fphi = self.local_Fphi + Af*Fphi
            # self.local_Ftheta = Af*Ftheta
            # self.local_Fphi = Af*Fphi
    
        a = np.absolute(self.local_Fphi);
        b = np.absolute(self.local_Ftheta);
        self.local_F = np.sqrt(a*a + b*b);
        max_magF = np.max(self.local_F);
        
        if max_magF>1e-6:
            self.local_F = self.local_F/max_magF;
            self.local_Ftheta = self.local_Ftheta/max_magF;
            self.local_Fphi = self.local_Fphi/max_magF;
        
        self.local_Frhcp = (self.local_Ftheta - 1j*self.local_Fphi)/MyMath.sqrt2
        self.local_Flhcp = (self.local_Ftheta + 1j*self.local_Fphi)/MyMath.sqrt2
    
    def symmetry_function(self,Ftheta,Fphi):
        s_hat_k = self.local_hat_k.copy()
        s_hat_phi = self.local_hat_phi.copy()
        
        if self.azimuth_symmetry:
            s_hat_k[:,:,0] = s_hat_k[:,:,0]*-1
            s_hat_k[:,:,1] = s_hat_k[:,:,1]*-1
            s_hat_phi[:,:,0] = s_hat_phi[:,:,0]*-1
            s_hat_phi[:,:,1] = s_hat_phi[:,:,1]*-1
        
        s_x = s_hat_k[:,:,0]
        s_y = s_hat_k[:,:,1]
        s_z = s_hat_k[:,:,2]
        
        s_mesh_theta = np.arctan2(np.sqrt(s_y*s_y+s_x*s_x), s_z)
        
        # ids1 = s_mesh_theta>3*np.pi/4
        # ids2 = s_mesh_theta<np.pi/4
        
        # s_x[ids1] = s_hat_phi[ids1,1]
        # s_y[ids1] = -s_hat_phi[ids1,0]
        # s_x[ids2] = s_hat_phi[ids2,1]
        # s_y[ids2] = s_hat_phi[ids2,0]
        s_mesh_phi = np.arctan2(s_y, s_x)
        
        fit_points = (self.local_theta, self.local_phi)
        interp_points = (s_mesh_theta, s_mesh_phi)
        
        values = Ftheta.copy()
        if values.dtype==np.dtype('complex64'):
            values = np.array(values,dtype=np.dtype('complex128'))
        interp = RegularGridInterpolator(fit_points, values, method='linear',bounds_error=True,fill_value=None)
        s_Ftheta = interp(interp_points)
        
        values = Fphi.copy()
        if values.dtype==np.dtype('complex64'):
            values = np.array(values,dtype=np.dtype('complex128'))
        interp = RegularGridInterpolator(fit_points, values, method='linear',bounds_error=True,fill_value=None)
        s_Fphi = interp(interp_points)
        
        if self.current_mirror:
            return -s_Ftheta,-s_Fphi
        else:
            return s_Ftheta,s_Fphi
    
    def copy(self):
        antennas = [antenna.copy() for antenna in self.antennas]
        array = Array(name=self.name,
                            x_mirror=self.x_mirror,
                            y_mirror=self.y_mirror,
                            z_mirror=self.z_mirror,
                            current_mirror=self.current_mirror,
                            azimuth_symmetry=self.azimuth_symmetry,
                            antennas=antennas,
                            current_mag=self.current_mag,
                            current_phase=self.current_phase,
                            phi=self.phi.copy(),theta=self.theta.copy(),
                            elevation=self.elevation,azimuth=self.azimuth,roll=self.roll,
                            x=self.x,y=self.y,z=self.z)
        
        array.LG_interp_hat_theta = self.LG_interp_hat_theta.copy()
        array.LG_interp_hat_phi = self.LG_interp_hat_phi.copy()
        array.GL_interp_mesh_theta = self.GL_interp_mesh_theta.copy()
        array.GL_interp_mesh_phi = self.GL_interp_mesh_phi.copy()
        
        array.local_F = self.local_F.copy()
        array.local_Ftheta = self.local_Ftheta.copy()
        array.local_Fphi = self.local_Fphi.copy()
        array.local_Frhcp = self.local_Frhcp.copy()
        array.local_Flhcp = self.local_Flhcp.copy()
        array.F = self.F.copy()
        array.Ftheta = self.Ftheta.copy()
        array.Fphi = self.Fphi.copy()
        array.Frhcp = self.Frhcp.copy()
        array.Flhcp = self.Flhcp.copy()
        
        array.local_mesh_flag = self.local_mesh_flag
        array.R_flag = self.R_flag
        array.Rtheta_flag = self.Rtheta_flag
        array.Rphi_flag = self.Rphi_flag
        array.hats_flag = self.hats_flag
        array.local_field_flag = self.local_field_flag
        array.LG_interp_mesh_flag = self.LG_interp_mesh_flag
        array.ok = self.ok
        
        return array