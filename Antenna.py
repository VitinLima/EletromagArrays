# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 17:48:55 2023

@author: Vítor Lima Aguirra
"""

import pickle

import numpy as np
import csv
from scipy.interpolate import RegularGridInterpolator

from NumpyExpressionParser import NumpyExpressionParser as NEP
import MyMath
import AntennaEditorFrame

constants = dict()
constants['c'] = 299792458 # m/s
constants['f'] = 433e6 # Hz
constants['eta'] = 120*np.pi
constants['lam'] = constants['c']/constants['f'] # m
constants['w'] = 2*np.pi*constants['f'] # rad/s
constants['k'] = 2*np.pi/constants['lam'] # rad/m

class Antenna:
    EditorFrame = AntennaEditorFrame.AntennaEditorFrame
    def __init__(self, constants=None, name='new antenna',
                 current_mag=1, current_phase=0,
                 theta=np.linspace(0, 180, 21), phi=np.linspace(-180, 180, 21),
                 roll=0, elevation=0, azimuth=0,
                 x=0, y=0, z=0,
                 evaluate_as='ideal dipole'):
        # self.constants=constants
        self.name=name
        self.current_mag=current_mag
        self.current_phase=current_phase
        self.theta=theta
        self.phi=phi
        self.roll=roll
        self.elevation=elevation
        self.azimuth=azimuth
        self.x=x
        self.y=y
        self.z=z
        self.evaluate_as=evaluate_as
        
        self.mesh_phi,self.mesh_theta = np.meshgrid(np.radians(self.phi),np.radians(self.theta))
        self.shape = (self.theta.size, self.phi.size)
        self.F = np.zeros(self.shape)
        self.Fphi = np.zeros(self.shape, dtype=np.csingle)
        self.Ftheta = np.zeros(self.shape, dtype=np.csingle)
        self.listeners = []
        self.antenna_size = .5
        self.silent=False
        self.local_mesh_N_theta = 91
        self.local_mesh_N_phi = 91
        
        self.local_theta = np.radians(np.linspace(0,180,self.local_mesh_N_theta))
        self.local_phi = np.radians(np.linspace(-180,180,self.local_mesh_N_phi))
        
        self.evaluation_arguments = dict()
        self.evaluation_arguments['dipole length'] = .5
        self.evaluation_arguments['loop dipole area'] = .5
        self.evaluation_arguments['expression theta'] = '(cos(k*L*lam/2*cos(theta)) - cos(k*L*lam/2))/(sin(theta)+(sin(theta)==0))'
        self.evaluation_arguments['expression phi'] = 'S*k*sin(theta)'
        self.evaluation_arguments['isotropic on'] = 'theta'
        self.evaluation_arguments['file path'] = ''
        self.evaluation_arguments['force reload'] = False
        self.evaluation_arguments['load mesh from file'] = False
        
        self.evaluate_local_mesh()
        self.evaluate_R()
        self.evaluate_Rtheta()
        self.evaluate_Rphi()
        self.evaluate_hats()
        
        self.local_mesh_flag = False
        self.R_flag = False
        self.Relevation_flag = True
        self.Razimuth_flag = True
        self.Rtheta_flag = False
        self.Rphi_flag = False
        self.hats_flag = False
        self.LG_interp_mesh_flag = True
        self.local_field_flag = True
        self.ok = False
    
    def notify(self, caller, event):
        self.ok = False
        self.mark_update('"' + str(caller) +'" called notify with event "' + event + '"')
    
    def mark_update(self, event):
        if self.silent:
            return
        for l in self.listeners:
            # print(str(self) + ' notifying ' + str(l) + ' for ' + event)
            l.notify(self, event)
    
    def set_name(self, name):
        self.name = name
        self.mark_update('renamed')
    
    def set_evaluation_method(self, evaluation_method):
        self.evaluate_as = evaluation_method
        self.local_field_flag = True
        self.ok = False
    
    def set_orientation(self, roll=None, azimuth=None, elevation=None):
        if roll is not None:
            self.roll = roll
        if azimuth is not None:
            self.azimuth = azimuth
        if elevation is not None:
            self.elevation = elevation
        
        self.R_flag = True
        self.LG_interp_mesh_flag = True
        self.ok = False
    
    def set_position(self, x=None, y=None, z=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z
    
    def set_current(self, current_mag=None, current_phase=None):
        if current_mag is not None:
            self.current_mag = current_mag
        if current_phase is not None:
            self.current_phase = current_phase
        
        self.ok = False
    
    def resample(self,theta,phi):
        self.phi = phi
        self.theta = theta
        self.mesh_phi,self.mesh_theta = np.meshgrid(np.radians(self.phi),np.radians(self.theta))
        self.shape = (self.theta.size, self.phi.size)
        self.F = np.zeros(self.shape)
        self.Fphi = np.zeros(self.shape, dtype=np.csingle)
        self.Ftheta = np.zeros(self.shape, dtype=np.csingle)
        
        self.Relevation_flag = True
        self.Razimuth_flag = True
        self.Rtheta_flag = True
        self.Rphi_flag = True
        self.hats_flag = True
        self.LG_interp_mesh_flag = True
        self.ok = False
    
    def evaluate_local_mesh(self):
        self.local_mesh_flag = False
        
        self.local_mesh_phi,self.local_mesh_theta = np.meshgrid(self.local_phi,self.local_theta)
        self.local_shape = (self.local_theta.size, self.local_phi.size)
        
        ct = np.cos(self.local_mesh_theta)
        st = np.sin(self.local_mesh_theta)
        Rtheta = np.zeros((self.local_theta.size, self.local_phi.size, 3, 3))
        Rtheta[:,:,0,0] = ct
        Rtheta[:,:,0,2] = st
        Rtheta[:,:,2,0] = -st
        Rtheta[:,:,1,1] = 1
        Rtheta[:,:,2,2] = ct
        
        cp = np.cos(self.local_mesh_phi)
        sp = np.sin(self.local_mesh_phi)
        Rphi = np.zeros((self.local_theta.size, self.local_phi.size, 3, 3))
        Rphi[:,:,0,0] = cp
        Rphi[:,:,0,1] = -sp
        Rphi[:,:,1,0] = sp
        Rphi[:,:,1,1] = cp
        Rphi[:,:,2,2] = 1
        
        self.local_hat_k = np.zeros((self.local_theta.size, self.local_phi.size, 3))
        self.local_hat_theta = np.zeros_like(self.local_hat_k)
        self.local_hat_phi = np.zeros_like(self.local_hat_k)
        self.local_hat_k[:,:,2] = 1
        self.local_hat_theta[:,:,0] = 1
        self.local_hat_phi[:,:,1] = 1
        
        self.local_hat_k = MyMath.rotate(self.local_hat_k, Rtheta)
        self.local_hat_theta = MyMath.rotate(self.local_hat_theta, Rtheta)
        
        self.local_hat_k = MyMath.rotate(self.local_hat_k, Rphi)
        self.local_hat_theta = MyMath.rotate(self.local_hat_theta, Rphi)
        self.local_hat_phi = MyMath.rotate(self.local_hat_phi, Rphi)
        
    def evaluate_R(self):
        self.R_flag = False
        
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
        cr = np.cos(np.radians(self.roll))
        sr = np.sin(np.radians(self.roll))
        Rroll = np.zeros((3, 3))
        Rroll[0,0] = 1
        Rroll[1,1] = cr
        Rroll[1,2] = sr
        Rroll[2,1] = -sr
        Rroll[2,2] = cr
        self.R = np.zeros((1,1,3,3))
        self.R[0,0,:,:] = Rroll@Ralpha@Rbeta
    
    def evaluate_Rtheta(self):
        self.Rtheta_flag = False
        
        ct = np.cos(self.mesh_theta)
        st = np.sin(self.mesh_theta)
        self.Rtheta = np.zeros((self.theta.size, self.phi.size, 3, 3))
        self.Rtheta[:,:,0,0] = ct
        self.Rtheta[:,:,0,2] = st
        self.Rtheta[:,:,2,0] = -st
        self.Rtheta[:,:,1,1] = 1
        self.Rtheta[:,:,2,2] = ct
        
    def evaluate_Rphi(self):
        self.Rphi_flag = False
        
        cp = np.cos(self.mesh_phi)
        sp = np.sin(self.mesh_phi)
        self.Rphi = np.zeros((self.theta.size, self.phi.size, 3, 3))
        self.Rphi[:,:,0,0] = cp
        self.Rphi[:,:,0,1] = -sp
        self.Rphi[:,:,1,0] = sp
        self.Rphi[:,:,1,1] = cp
        self.Rphi[:,:,2,2] = 1
    
    def evaluate_hats(self):
        self.hats_flag = False
        
        self.hat_k = np.zeros((self.theta.size, self.phi.size, 3))
        self.hat_theta = np.zeros((self.theta.size, self.phi.size, 3))
        self.hat_phi = np.zeros((self.theta.size, self.phi.size, 3))
        self.hat_k[:,:,2] = 1
        self.hat_theta[:,:,0] = 1
        self.hat_phi[:,:,1] = 1
        
        self.hat_k = MyMath.rotate(self.hat_k, self.Rtheta)
        self.hat_theta = MyMath.rotate(self.hat_theta, self.Rtheta)
        
        self.hat_k = MyMath.rotate(self.hat_k, self.Rphi)
        self.hat_theta = MyMath.rotate(self.hat_theta, self.Rphi)
        self.hat_phi = MyMath.rotate(self.hat_phi, self.Rphi)
    
    def evaluate_LG_interp_mesh(self):
        # L - Local
        # G - Global
        # GL - Global on Local for vectors or Global to Local for matrices
        # LG - Local on Global for vectors or Local to Global for matrices
        
        self.LG_interp_mesh_flag = False
        
        GL_hat_k = MyMath.rotate(self.hat_k,self.R)
        GL_hat_theta = MyMath.rotate(self.hat_theta, self.R)
        
        GL_x = GL_hat_k[:,:,0]
        GL_y = GL_hat_k[:,:,1]
        GL_z = GL_hat_k[:,:,2]
        
        self.GL_interp_mesh_theta = np.arctan2(np.sqrt(GL_y*GL_y+GL_x*GL_x), GL_z)
        
        ids = (self.GL_interp_mesh_theta>3)+(self.GL_interp_mesh_theta<0.1)
        
        GL_x[ids] = GL_hat_theta[ids,0]
        GL_y[ids] = GL_hat_theta[ids,1]
        self.GL_interp_mesh_phi = np.arctan2(GL_y, GL_x)
        
        ct = np.cos(self.GL_interp_mesh_theta)
        st = np.sin(self.GL_interp_mesh_theta)
        Rtheta = np.zeros_like(self.Rtheta)
        Rtheta[:,:,0,0] = ct
        Rtheta[:,:,0,2] = st
        Rtheta[:,:,2,0] = -st
        Rtheta[:,:,1,1] = 1
        Rtheta[:,:,2,2] = ct
        
        cp = np.cos(self.GL_interp_mesh_phi)
        sp = np.sin(self.GL_interp_mesh_phi)
        Rphi = np.zeros_like(self.Rphi)
        Rphi[:,:,0,0] = cp
        Rphi[:,:,0,1] = -sp
        Rphi[:,:,1,0] = sp
        Rphi[:,:,1,1] = cp
        Rphi[:,:,2,2] = 1
        
        L_interp_hat_theta = np.zeros((self.theta.size, self.phi.size, 3))
        L_interp_hat_phi = np.zeros_like(L_interp_hat_theta)
        L_interp_hat_theta[:,:,0] = 1
        L_interp_hat_phi[:,:,1] = 1
        
        LG_R = np.swapaxes(self.R,2,3)
        self.LG_interp_hat_theta = MyMath.rotate(MyMath.rotate(MyMath.rotate(L_interp_hat_theta, Rtheta), Rphi), LG_R)
        self.LG_interp_hat_phi = MyMath.rotate(MyMath.rotate(MyMath.rotate(L_interp_hat_phi, Rtheta), Rphi), LG_R)
    
    def evaluate_local_field(self):
        self.local_field_flag = False
        
        self.local_Fphi = np.zeros(self.local_shape)
        self.local_Ftheta = np.zeros(self.local_shape)
        
        # try:
        if self.evaluate_as=='isotropic':
            if self.evaluation_arguments['isotropic on'] == 'both':
                self.local_Ftheta[:] = 0.7071067811865475 # 1/sqrt(2)
                self.local_Fphi[:] = 0.7071067811865475 # 1/sqrt(2)
            elif self.evaluation_arguments['isotropic on'] =='theta':
                self.local_Ftheta[:] = 1
                self.local_Fphi[:] = 0
            elif self.evaluation_arguments['isotropic on'] =='phi':
                self.local_Ftheta[:] = 0
                self.local_Fphi[:] = 1
        elif self.evaluate_as=='ideal dipole':
            # if 'dipole length' in self.evaluation_arguments.keys():
            self.ideal_dipole(self.evaluation_arguments['dipole length'])
            # else:
            #     raise Exception('Tried to calculate ideal dipole field without dipole length.')
        if self.evaluate_as=='ideal loop dipole':
            # if 'loop dipole area' in self.evaluation_arguments.keys():
            self.ideal_loop_dipole(self.evaluation_arguments['loop dipole area'])
            # else:
            #     raise Exception('Tried to calculate ideal dipole field without dipole length.')
        elif self.evaluate_as=='load file':
            # if 'file path' in self.evaluation_arguments.keys():
            self.load_file(self.evaluation_arguments['file path'])
            # else:
            #     raise Exception('Tried to load file without file path.')
        elif self.evaluate_as=='expressions':
            # if 'expression theta' in self.evaluation_arguments.keys() and 'expression phi' in self.evaluation_arguments.keys():
            self.eval_expression(self.evaluation_arguments['expression theta'],self.evaluation_arguments['expression phi'])
            # else:
            #     raise Exception('Tried to evaluate expression without expression.')
        # except Exception as e:
        #     print(e)
    
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
    
    def evaluate(self):
        if self.ok:
            return
        
        if self.local_mesh_flag:
            self.evaluate_local_mesh()
        if self.R_flag:
            self.evaluate_R()
        if self.Rtheta_flag:
            self.evaluate_Rtheta()
        if self.Rphi_flag:
            self.evaluate_Rphi()
        if self.hats_flag:
            self.evaluate_hats()
        if self.local_field_flag:
            self.evaluate_local_field()
        if self.LG_interp_mesh_flag:
            self.evaluate_LG_interp_mesh()
        
        fit_points = (self.local_theta, self.local_phi)
        interp_points = (self.GL_interp_mesh_theta, self.GL_interp_mesh_phi)
        
        values = self.local_Ftheta.copy()
        if values.dtype==np.dtype('complex64'):
            values = np.array(values,dtype=np.dtype('complex128'))
        interp = RegularGridInterpolator(fit_points, values, method='linear')
        Ftheta = interp(interp_points)
        
        values = self.local_Fphi.copy()
        if values.dtype==np.dtype('complex64'):
            values = np.array(values,dtype=np.dtype('complex128'))
        interp = RegularGridInterpolator(fit_points, values, method='linear')
        Fphi = interp(interp_points)
        
        self.Ftheta = Ftheta*(self.LG_interp_hat_theta*self.hat_theta).sum(2) + Fphi*(self.LG_interp_hat_phi*self.hat_theta).sum(2)
        self.Fphi = Ftheta*(self.LG_interp_hat_theta*self.hat_phi).sum(2) + Fphi*(self.LG_interp_hat_phi*self.hat_phi).sum(2)
        
        a = np.absolute(self.Fphi);
        b = np.absolute(self.Ftheta);
        self.F = np.sqrt(a*a + b*b);
        
        self.Frhcp = (self.Ftheta - 1j*self.Fphi)/MyMath.sqrt2
        self.Flhcp = (self.Ftheta + 1j*self.Fphi)/MyMath.sqrt2
        
        self.ok = True
        self.mark_update('evaluated')
    
    def ideal_dipole(self, L):
        st = np.sin(self.local_mesh_theta)
        ids = st != 0
        
        A = constants['k']*L*constants['lam']/2
        
        self.local_Ftheta[ids] = (np.cos(A*np.cos(self.local_mesh_theta[ids])) - np.cos(A))/st[ids]
    
    def ideal_loop_dipole(self, S):
        pass
    
    def load_file(self, file_path):
        if 'loaded file' in self.evaluation_arguments.keys():
            if self.evaluation_arguments['loaded file']==file_path and not self.evaluation_arguments['force reload']:
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
            Fphi = 4*np.pi*np.array(rEphi)/(1j*constants['eta']*constants['k'])
            Ftheta = 4*np.pi*np.array(rEtheta)/(1j*constants['eta']*constants['k'])
            idsphi = theta==theta[0]
            idstheta = phi==phi[0]
            phi = phi[idsphi]
            theta = theta[idstheta]
            if self.evaluation_arguments['load mesh from file']:
                self.local_phi = phi
                self.local_theta = theta
                self.local_mesh_flag = True
                self.local_shape = (self.local_theta.size, self.local_phi.size)
                
                self.local_Fphi = np.reshape(Fphi,(theta.size,phi.size))
                self.local_Ftheta = np.reshape(Ftheta,(theta.size,phi.size))
            else:
                fit_points = (theta, phi)
                interp_points = (self.local_mesh_theta, self.local_mesh_phi)
                
                values = np.reshape(Ftheta,(theta.size,phi.size))
                interp = RegularGridInterpolator(fit_points, values, method='linear')
                self.local_Ftheta = interp(interp_points)
                
                values = np.reshape(Fphi,(theta.size,phi.size))
                interp = RegularGridInterpolator(fit_points, values, method='linear')
                self.local_Fphi = interp(interp_points)
            
            self.evaluation_arguments['loaded file'] = file_path
            self.evaluation_arguments['force reload'] = False
    
    def eval_expression(self, expression_theta, expression_phi):
        new_vars = {
            'L': self.evaluation_arguments['dipole length'],
            'S': self.evaluation_arguments['loop dipole area'],
            'theta': self.local_mesh_theta,
            'phi': self.local_mesh_phi,
            'mesh_theta': self.local_mesh_theta,
            'mesh_phi': self.local_mesh_phi
        }
        for key in constants.keys():
            new_vars[key] = constants[key]
        self.local_Ftheta = NEP.eval(expression=expression_theta,variables=new_vars)
        self.local_Fphi = NEP.eval(expression=expression_phi,variables=new_vars)
        self.local_Ftheta = np.broadcast_to(self.local_Ftheta,self.local_shape)
        self.local_Fphi = np.broadcast_to(self.local_Fphi,self.local_shape)
    
    def copy(self):
        antenna = Antenna(constants=constants,name=self.name,
                          current_mag=self.current_mag,
                          current_phase=self.current_phase,
                          phi=self.phi.copy(),theta=self.theta.copy(),
                          elevation=self.elevation,azimuth=self.azimuth,roll=self.roll,
                          x=self.x,y=self.y,z=self.z,
                          evaluate_as=self.evaluate_as)
        
        antenna.evaluation_arguments = self.evaluation_arguments.copy()
        
        antenna.LG_interp_hat_theta = self.LG_interp_hat_theta.copy()
        antenna.LG_interp_hat_phi = self.LG_interp_hat_phi.copy()
        antenna.GL_interp_mesh_theta = self.GL_interp_mesh_theta.copy()
        antenna.GL_interp_mesh_phi = self.GL_interp_mesh_phi.copy()
        
        antenna.local_F = self.local_F.copy()
        antenna.local_Ftheta = self.local_Ftheta.copy()
        antenna.local_Fphi = self.local_Fphi.copy()
        antenna.local_Frhcp = self.local_Frhcp.copy()
        antenna.local_Flhcp = self.local_Flhcp.copy()
        antenna.F = self.F.copy()
        antenna.Ftheta = self.Ftheta.copy()
        antenna.Fphi = self.Fphi.copy()
        antenna.Frhcp = self.Frhcp.copy()
        antenna.Flhcp = self.Flhcp.copy()
        
        antenna.local_mesh_flag = self.local_mesh_flag
        antenna.R_flag = self.R_flag
        antenna.Rtheta_flag = self.Rtheta_flag
        antenna.Rphi_flag = self.Rphi_flag
        antenna.hats_flag = self.hats_flag
        antenna.local_field_flag = self.local_field_flag
        antenna.LG_interp_mesh_flag = self.LG_interp_mesh_flag
        antenna.ok = self.ok
        
        return antenna

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
    antenna.evaluate_as = antenna.load_file
    root = tk.Tk()
    root.geometry('0x0')
    file_path = tk.filedialog.askopenfilename(parent=root)
    root.destroy()
    if file_path!='':
        antenna.evaluation_arguments['file path'] = file_path
        antenna.evaluation_arguments['force reload'] = False
        antenna.evaluation_arguments['load mesh from file'] = True
        antenna.evaluate()
    
    def export_to_file(self, filename):
        with open(filename, mode='wb') as f:
            pickle.dump(self, f)