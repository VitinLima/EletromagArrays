# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 00:09:51 2023

@author: 160047412
"""

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from Antenna import Antenna
import scope_fields

class Array(Antenna):
    def __init__(self, constants, name='new array', current=(1+0j),
                 theta=np.linspace(0, 180, 21), phi=np.linspace(-180, 180, 21),
                 elevation=0, azimuth=0,
                 x=0, y=0, z=0,
                 antennas=None):
        Antenna.__init__(self, constants=constants, name=name, current=current, phi=phi, theta=theta, elevation=elevation, azimuth=azimuth, x=x, y=y, z=z)
        
        if antennas is not None:
            self.antennas = antennas
        else:
            self.antennas = []
        self.x_mirror = False
        self.y_mirror= False
        self.z_mirror= False
        self.current_mirror= False
        self.x_symmetry= False
        self.y_symmetry= False
        self.z_symmetry= False
    
    def add_antenna(self, antenna):
        self.antennas.append(antenna)
        antenna.listeners.append(self)
        self.mark_update('antenna added')
    
    def evaluate(self):
        if self.ok:
            return
        
        if len(self.antennas)==0:
            return
        
        self.Ftheta[:,:] = 0
        self.Fphi[:,:] = 0
        
        for antenna in self.antennas:
            antenna.evaluate()
            
            # hat_k = antenna.rotate(Antenna.rotate(self.hat_k,self.R), antenna.R)
            # hat_theta = antenna.rotate(Antenna.rotate(self.hat_theta,self.R), antenna.R)
            # hat_phi = antenna.rotate(Antenna.rotate(self.hat_phi,self.R), antenna.R)
            
            # x = hat_k[:,:,0]
            # y = hat_k[:,:,1]
            # z = hat_k[:,:,2]
            # local_mesh_phi = np.arctan2(y, x)
            # local_mesh_theta = np.arctan2(np.sqrt(y*y+x*x), z)
            
            # ct = np.cos(local_mesh_theta)
            # st = np.sin(local_mesh_theta)
            # Rtheta = np.zeros_like(self.Rtheta)
            # Rtheta[:,:,0,0] = ct
            # Rtheta[:,:,0,2] = st
            # Rtheta[:,:,2,0] = -st
            # Rtheta[:,:,1,1] = 1
            # Rtheta[:,:,2,2] = ct
            
            # cp = np.cos(local_mesh_phi)
            # sp = np.sin(local_mesh_phi)
            # Rphi = np.zeros_like(self.Rphi)
            # Rphi[:,:,0,0] = cp
            # Rphi[:,:,0,1] = -sp
            # Rphi[:,:,1,0] = sp
            # Rphi[:,:,1,1] = cp
            # Rphi[:,:,2,2] = 1
            
            # local_hat_theta = np.zeros_like(hat_theta)
            # local_hat_phi = np.zeros_like(hat_phi)
            # local_hat_theta[:,:,0] = 1
            # local_hat_phi[:,:,1] = 1
            # local_hat_theta = self.rotate(self.rotate(local_hat_theta, Rtheta), Rphi)
            # local_hat_phi = self.rotate(self.rotate(local_hat_phi, Rtheta), Rphi)
            
            fit_points = (np.radians(antenna.theta), np.radians(antenna.phi))
            interp_points = (self.mesh_theta, self.mesh_phi)
            
            values = antenna.Ftheta
            if values.dtype==np.dtype('complex64'):
                values = np.array(values,dtype=np.dtype('complex128'))
            interp = RegularGridInterpolator(fit_points, values, method='linear')
            Ftheta = interp(interp_points)
            
            values = antenna.Fphi
            if values.dtype==np.dtype('complex64'):
                values = np.array(values,dtype=np.dtype('complex128'))
            interp = RegularGridInterpolator(fit_points, values, method='linear')
            Fphi = interp(interp_points)
            
            # Ftheta = local_Ftheta*(local_hat_theta*hat_theta).sum(2) + local_Fphi*(local_hat_phi*hat_theta).sum(2)
            # Fphi = local_Ftheta*(local_hat_theta*hat_phi).sum(2) + local_Fphi*(local_hat_phi*hat_phi).sum(2)
            
            x = antenna.x
            y = antenna.y
            z = antenna.z
            current = antenna.current
            
            p0 = np.array([x,y,z]).reshape((1,1,3))
            Af = current*np.exp(1j*self.constants['k']*(self.hat_k*p0).sum(2))
            total_Ftheta = Af*Ftheta
            total_Fphi = Af*Fphi
            
            if np.abs(antenna.x)>0.2 and self.x_symmetry:
                s_Ftheta,s_Fphi = self.symmetry_function(Ftheta=Ftheta,Fphi=Fphi)
                p1 = np.array([-x,y,z]).reshape((1,1,3))
                s_Af = current*np.exp(1j*self.constants['k']*(self.hat_k*p1).sum(2))
                total_Ftheta += s_Af*s_Ftheta
                total_Fphi += s_Af*s_Fphi
            if np.abs(antenna.y)>0.2 and self.y_symmetry:
                s_Ftheta,s_Fphi = self.symmetry_function(Ftheta=Ftheta,Fphi=Fphi)
                p1 = np.array([x,-y,z]).reshape((1,1,3))
                s_Af = current*np.exp(1j*self.constants['k']*(self.hat_k*p1).sum(2))
                total_Ftheta += s_Af*s_Ftheta
                total_Fphi += s_Af*s_Fphi
            if np.abs(antenna.z)>0.2 and self.z_symmetry:
                s_Ftheta,s_Fphi = self.symmetry_function(Ftheta=Ftheta,Fphi=Fphi)
                p1 = np.array([x,y,-z]).reshape((1,1,3))
                s_Af = current*np.exp(1j*self.constants['k']*(self.hat_k*p1).sum(2))
                total_Ftheta += s_Af*s_Ftheta
                total_Fphi += s_Af*s_Fphi
            
            self.Ftheta += total_Ftheta
            self.Fphi += total_Fphi
        
        # Normalize electric fields
        a = np.absolute(self.Fphi);
        b = np.absolute(self.Ftheta);
        self.F = np.sqrt(a*a + b*b);
        max_magF = np.max(self.F);
          
        if max_magF>1e-6:
            self.F /= max_magF;
            self.Fphi /= max_magF;
            self.Ftheta /= max_magF;
        
        self.ok = True
        self.mark_update('evaluated')
    
    def symmetry_function(self,Ftheta,Fphi):
        s_hat_k = self.hat_k.copy()
        
        if self.x_mirror:
            s_hat_k[:,:,0] = s_hat_k[:,:,0]*-1
        elif self.y_mirror:
            s_hat_k[:,:,0] = s_hat_k[:,:,0]*-1
        elif self.z_mirror:
            s_hat_k[:,:,2] = s_hat_k[:,:,2]*-1
        
        s_x = s_hat_k[:,:,0]
        s_y = s_hat_k[:,:,1]
        s_z = s_hat_k[:,:,2]
        s_mesh_phi = np.arctan2(s_y, s_x)
        s_mesh_theta = np.arctan2(np.sqrt(s_y*s_y+s_x*s_x), s_z)
        
        fit_points = (np.radians(self.theta), np.radians(self.phi))
        interp_points = (s_mesh_theta, s_mesh_phi)
        
        values = Ftheta.copy()
        if values.dtype==np.dtype('complex64'):
            values = np.array(values,dtype=np.dtype('complex128'))
        interp = RegularGridInterpolator(fit_points, values, method='linear',bounds_error=False,fill_value=None)
        s_Ftheta = interp(interp_points)
        
        values = Fphi.copy()
        if values.dtype==np.dtype('complex64'):
            values = np.array(values,dtype=np.dtype('complex128'))
        interp = RegularGridInterpolator(fit_points, values, method='linear',bounds_error=False,fill_value=None)
        s_Fphi = interp(interp_points)
        
        if self.current_mirror:
            return -s_Ftheta,-s_Fphi
        else:
            return s_Ftheta,s_Fphi