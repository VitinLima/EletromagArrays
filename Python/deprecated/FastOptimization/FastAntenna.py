# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 00:09:39 2023

@author: 160047412
"""

import numpy as np
import csv
from scipy.interpolate import RegularGridInterpolator

from NumpyExpressionParser import NumpyExpressionParser as NEP

class Antenna:
    def __init__(self, constants, name='new antenna', current=(1+0j),
                 theta=np.linspace(0, 180, 21), phi=np.linspace(-180, 180, 21),
                 elevation=0, azimuth=0,
                 x=0, y=0, z=0):
        self.constants=constants
        self.name=name
        self.current=current
        self.theta=theta
        self.phi=phi
        self.elevation=elevation
        self.azimuth=azimuth
        self.x=x
        self.y=y
        self.z=z
        
        self.mesh_phi,self.mesh_theta = np.meshgrid(np.radians(self.phi),np.radians(self.theta))
        self.shape = (self.theta.size, self.phi.size)
        self.F = np.zeros(self.shape)
        self.Fphi = np.zeros(self.shape, dtype=np.csingle)
        self.Ftheta = np.zeros(self.shape, dtype=np.csingle)
        
        self.antenna_size = .5
        
        self.evaluate_function = self.ideal_dipole
        self.eval_fun_args = dict()
        self.eval_fun_args['force reload'] = False
        self.eval_fun_args['load mesh from file'] = False
        self.eval_fun_args['dipole length'] = .5
        self.eval_fun_args['loop dipole area'] = .5
        
        self.evaluate_R()
        self.evaluate_Rtheta()
        self.evaluate_Rphi()
        self.evaluate_hats()
    
    def set_orientation(self, azimuth=None, elevation=None):
        if azimuth is not None:
            self.azimuth = azimuth
        if elevation is not None:
            self.elevation = elevation
        
        self.evaluate_R()
        self.evaluate_hats()
    
    def resample(self,theta,phi):
        self.phi = phi
        self.theta = theta
        self.mesh_phi,self.mesh_theta = np.meshgrid(np.radians(self.phi),np.radians(self.theta))
        self.shape = (self.theta.size, self.phi.size)
        self.F = np.zeros(self.shape)
        self.Fphi = np.zeros(self.shape, dtype=np.csingle)
        self.Ftheta = np.zeros(self.shape, dtype=np.csingle)
        
        self.evaluate_Rtheta()
        self.evaluate_Rphi()
        self.evaluate_hats()
    
    def evaluate_hats(self):
        self.hat_k = np.zeros((self.theta.size, self.phi.size, 3))
        self.hat_theta = np.zeros((self.theta.size, self.phi.size, 3))
        self.hat_phi = np.zeros((self.theta.size, self.phi.size, 3))
        self.hat_k[:,:,2] = 1
        self.hat_theta[:,:,0] = 1
        self.hat_phi[:,:,1] = 1
        
        self.hat_k = Antenna.rotate(self.hat_k, self.Rtheta)
        self.hat_theta = Antenna.rotate(self.hat_theta, self.Rtheta)
        
        self.hat_k = Antenna.rotate(self.hat_k, self.Rphi)
        self.hat_theta = Antenna.rotate(self.hat_theta, self.Rphi)
        self.hat_phi = Antenna.rotate(self.hat_phi, self.Rphi)
        
        R = np.swapaxes(self.R,2,3)
        self.local_hat_k = Antenna.rotate(self.hat_k, R)
        self.local_hat_theta = Antenna.rotate(self.hat_theta, R)
        self.local_hat_phi = Antenna.rotate(self.hat_phi, R)
        
    def evaluate_R(self):
        cp = np.cos(np.radians(self.azimuth))
        sp = np.sin(np.radians(self.azimuth))
        Rbeta = np.zeros((3, 3))
        Rbeta[0,0] = cp
        Rbeta[0,1] = sp
        Rbeta[1,0] = -sp
        Rbeta[1,1] = cp
        Rbeta[2,2] = 1
        ct = np.cos(np.radians(self.elevation))
        st = np.sin(np.radians(self.elevation))
        Ralpha = np.zeros((3, 3))
        Ralpha[0,0] = ct
        Ralpha[0,2] = -st
        Ralpha[2,0] = st
        Ralpha[1,1] = 1
        Ralpha[2,2] = ct
        self.R = np.zeros((1,1,3,3))
        self.R[0,0,:,:] = Ralpha@Rbeta
    
    def evaluate_Rtheta(self):
        ct = np.cos(self.mesh_theta)
        st = np.sin(self.mesh_theta)
        self.Rtheta = np.zeros((self.theta.size, self.phi.size, 3, 3))
        self.Rtheta[:,:,0,0] = ct
        self.Rtheta[:,:,0,2] = st
        self.Rtheta[:,:,2,0] = -st
        self.Rtheta[:,:,1,1] = 1
        self.Rtheta[:,:,2,2] = ct
        
    def evaluate_Rphi(self):
        cp = np.cos(self.mesh_phi)
        sp = np.sin(self.mesh_phi)
        self.Rphi = np.zeros((self.theta.size, self.phi.size, 3, 3))
        self.Rphi[:,:,0,0] = cp
        self.Rphi[:,:,0,1] = -sp
        self.Rphi[:,:,1,0] = sp
        self.Rphi[:,:,1,1] = cp
        self.Rphi[:,:,2,2] = 1
    
    def evaluate(self):
        
        self.Ftheta = self.local_Ftheta*(self.local_hat_theta*self.hat_theta).sum(2) + self.local_Fphi*(self.local_hat_phi*self.hat_theta).sum(2)
        self.Fphi = self.local_Ftheta*(self.local_hat_theta*self.hat_phi).sum(2) + self.local_Fphi*(self.local_hat_phi*self.hat_phi).sum(2)
        
        a = np.absolute(self.Fphi);
        b = np.absolute(self.Ftheta);
        self.F = np.sqrt(a*a + b*b);
        
        self.mark_update('evaluated')
    
    def evaluate_local_field(self):
        self.local_Ftheta = self.Ftheta.copy()
        self.local_Fphi = self.Fphi.copy()
    
        self.local_hat_k = Antenna.rotate(self.hat_k,self.R)
        
        local_x = self.local_hat_k[:,:,0]
        local_y = self.local_hat_k[:,:,1]
        local_z = self.local_hat_k[:,:,2]
        self.local_mesh_phi = np.arctan2(local_y, local_x)
        self.local_mesh_theta = np.arctan2(np.sqrt(local_y*local_y+local_x*local_x), local_z)
        
        ct = np.cos(self.local_mesh_theta)
        st = np.sin(self.local_mesh_theta)
        Rtheta = np.zeros_like(self.Rtheta)
        Rtheta[:,:,0,0] = ct
        Rtheta[:,:,0,2] = st
        Rtheta[:,:,2,0] = -st
        Rtheta[:,:,1,1] = 1
        Rtheta[:,:,2,2] = ct
        
        cp = np.cos(self.local_mesh_phi)
        sp = np.sin(self.local_mesh_phi)
        Rphi = np.zeros_like(self.Rphi)
        Rphi[:,:,0,0] = cp
        Rphi[:,:,0,1] = -sp
        Rphi[:,:,1,0] = sp
        Rphi[:,:,1,1] = cp
        Rphi[:,:,2,2] = 1
        
        self.local_hat_theta = np.zeros_like(self.local_hat_k)
        self.local_hat_phi = np.zeros_like(self.local_hat_k)
        self.local_hat_theta[:,:,0] = 1
        self.local_hat_phi[:,:,1] = 1
        R = np.swapaxes(self.R,2,3)
        self.local_hat_theta = self.rotate(self.rotate(self.rotate(self.local_hat_theta, Rtheta), Rphi), R)
        self.local_hat_phi = self.rotate(self.rotate(self.rotate(self.local_hat_phi, Rtheta), Rphi), R)
        
        try:
            if self.evaluate_function=='ideal_dipole':
                if 'dipole length' in self.eval_fun_args.keys():
                    self.ideal_dipole(self.eval_fun_args['dipole length'])
                else:
                    raise Exception('Tried to calculate ideal dipole field without dipole length.')
            if self.evaluate_function=='ideal_loop_dipole':
                if 'loop dipole area' in self.eval_fun_args.keys():
                    self.ideal_loop_dipole(self.eval_fun_args['loop dipole area'])
                else:
                    raise Exception('Tried to calculate ideal dipole field without dipole length.')
            elif self.evaluate_function=='load_file':
                if 'file path' in self.eval_fun_args.keys():
                    self.load_file(self.eval_fun_args['file path'])
                else:
                    raise Exception('Tried to load file without file path.')
            elif self.evaluate_function=='expression':
                if 'expression theta' in self.eval_fun_args.keys() and 'expression phi' in self.eval_fun_args.keys():
                    self.eval_expression(self.eval_fun_args['expression theta'],self.eval_fun_args['expression phi'])
                else:
                    raise Exception('Tried to evaluate expression without expression.')
        except Exception as e:
            print(e)
        
        a = np.absolute(self.local_Fphi);
        b = np.absolute(self.local_Ftheta);
        self.local_F = np.sqrt(a*a + b*b);
        max_magF = np.max(self.local_F);
        
        if max_magF>1e-6:
            self.local_F = self.local_F/max_magF;
            self.local_Ftheta = self.local_Ftheta/max_magF;
            self.local_Fphi = self.local_Fphi/max_magF;
    
    def ideal_dipole(self, L):
        st = np.sin(self.local_mesh_theta)
        ids = st != 0
        
        A = self.constants['k']*L*self.constants['lam']/2
        
        self.local_Fphi = np.zeros(self.shape)
        self.local_Ftheta = np.zeros(self.shape)
        self.local_Ftheta[ids] = (np.cos(A*np.cos(self.local_mesh_theta[ids])) - np.cos(A))/st[ids]
    
    def ideal_loop_dipole(self, S):
        pass
    
    def load_file(self, file_path):
        if 'loaded file' in self.eval_fun_args.keys():
            if self.eval_fun_args['loaded file']==file_path and not self.eval_fun_args['force reload']:
                return
        with open(file_path,'r') as f:
            reader = csv.reader(f)
            
            variations =[]
            phi = []
            theta = []
            rEphi = []
            rEtheta = []
            
            self.header = reader.__next__()
            for line in reader:
                variations.append(line[0])
                phi.append(float(line[1]))
                theta.append(float(line[2]))
                a = line[3].split()
                rEphi.append(float(a[0])*np.exp(1j*float(a[1])))
                a = line[4].split()
                rEtheta.append(float(a[0])*np.exp(1j*float(a[1])))
            
            phi = np.array(phi)
            theta = np.array(theta)
            Fphi = 4*np.pi*np.array(rEphi)/(1j*self.constants['eta']*self.constants['k'])
            Ftheta = 4*np.pi*np.array(rEtheta)/(1j*self.constants['eta']*self.constants['k'])
            idsphi = theta==theta[0]
            idstheta = phi==phi[0]
            phi = phi[idsphi]
            theta = theta[idstheta]
            if self.eval_fun_args['load mesh from file']:
                self.local_mesh_phi,self.local_mesh_theta = np.meshgrid(phi,theta)
                self.phi = np.degrees(phi)
                self.theta = np.degrees(theta)
                self.local_Fphi = np.reshape(Fphi,(theta.size,phi.size))
                self.local_Ftheta = np.reshape(Ftheta,(theta.size,phi.size))
                self.evaluate_Rtheta()
                self.evaluate_Rphi()
                self.evaluate_hats()
            else:
                fit_points = (theta, phi)
                interp_points = (self.local_mesh_theta, self.local_mesh_phi)
                
                values = np.reshape(Ftheta,(theta.size,phi.size))
                interp = RegularGridInterpolator(fit_points, values, method='linear')
                self.local_Ftheta = interp(interp_points)
                
                values = np.reshape(Fphi,(theta.size,phi.size))
                interp = RegularGridInterpolator(fit_points, values, method='linear')
                self.local_Fphi = interp(interp_points)
            
            self.eval_fun_args['loaded file'] = file_path
            self.eval_fun_args['force reload'] = False
    
    def eval_expression(self, expression_theta, expression_phi):
        new_vars = {
            'L': self.eval_fun_args['dipole length'],
            'S': self.eval_fun_args['loop dipole area'],
            'theta': self.local_mesh_theta,
            'phi': self.local_mesh_phi,
            'mesh_theta': self.local_mesh_theta,
            'mesh_phi': self.local_mesh_phi
        }
        for key in self.constants.keys():
            new_vars[key] = self.constants[key]
        self.local_Ftheta = NEP.eval(expression=expression_theta,variables=new_vars)
        self.local_Fphi = NEP.eval(expression=expression_phi,variables=new_vars)
        self.local_Ftheta = np.broadcast_to(self.local_Ftheta,self.shape)
        self.local_Fphi = np.broadcast_to(self.local_Fphi,self.shape)
    
    def copy(self):
        antenna = Antenna(constants=self.constants,name=self.name,
                              phi=self.phi.copy(),theta=self.theta.copy(),
                              elevation=self.elevation,azimuth=self.azimuth,
                              x=self.x,y=self.y,z=self.z)
        if self.evaluate_function==self.ideal_dipole:
            antenna.evaluate_function=antenna.ideal_dipole
            antenna.eval_fun_args['dipole length'] = self.eval_fun_args['dipole length']
        elif self.evaluate_function==self.ideal_loop_dipole:
            antenna.evaluate_function=antenna.ideal_loop_dipole
            antenna.eval_fun_args['loop dipole area'] = self.eval_fun_args['loop dipole area']
        elif self.evaluate_function==self.load_file:
            antenna.evaluate_function=antenna.load_file
            antenna.eval_fun_args['file path'] = self.eval_fun_args['file path']
            antenna.eval_fun_args['load mesh from file'] = self.eval_fun_args['load mesh from file']
            antenna.eval_fun_args['force reload'] = self.eval_fun_args['force reload']
        elif self.evaluate_function==self.eval_expression:
            antenna.evaluate_function=antenna.eval_expression
            antenna.eval_fun_args['expression theta'] = self.eval_fun_args['expression theta']
            antenna.eval_fun_args['expression phi'] = self.eval_fun_args['expression phi']
        antenna.F = self.F.copy()
        antenna.Ftheta = self.Ftheta.copy()
        antenna.Fphi = self.Fphi.copy()
        antenna.ok = self.ok
        
        return antenna
    
    @staticmethod
    def rotate(vec, R):
        new_vec = np.zeros_like(vec)
        R_swapped = R.swapaxes(2,3)
        new_vec[:,:,0] = (vec*R_swapped[:,:,:,0]).sum(2)
        new_vec[:,:,1] = (vec*R_swapped[:,:,:,1]).sum(2)
        new_vec[:,:,2] = (vec*R_swapped[:,:,:,2]).sum(2)
        return new_vec

if __name__=='__main__':
    import tkinter as tk
    import math
    
    constants = dict()
    constants['c'] = 299792458 # m/s
    constants['f'] = 433e6 # Hz
    constants['eta'] = 120*math.pi
    constants['lam'] = constants['c']/constants['f'] # m
    constants['w'] = 2*math.pi*constants['f'] # rad/s
    constants['k'] = 2*math.pi/constants['lam'] # rad/m
    
    antenna = Antenna(constants=constants,name='loaded antenna')
    antenna.evaluate_function = antenna.load_file
    root = tk.Tk()
    root.geometry('0x0')
    file_path = tk.filedialog.askopenfilename(parent=root)
    root.destroy()
    if file_path!='':
        antenna.eval_fun_args['file path'] = file_path
        antenna.eval_fun_args['force reload'] = False
        antenna.eval_fun_args['load mesh from file'] = True
        antenna.evaluate()
    