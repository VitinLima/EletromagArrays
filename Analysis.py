# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 22:35:54 2023

@author: 160047412
"""

import numpy as np

from NumpyExpressionParser import NumpyExpressionParser as NEP
import Antenna

class Analysis:
    def __init__(self,name='New analysis',expression='F',color_expression=''):
        self.name=name
        self.expression=expression
        self.color_expression=color_expression
        
        self.listeners = []
        self.ok = True
    
    def mark_update(self, event):
        self.ok = False
        for l in self.listeners:
            # print(str(self) + ' notifying ' + str(l) + ' for ' + event)
            l.notify(self, event)
    
    def config(self,name=None,expression=None,color_expression=None):
        if name is not None:
            self.name=name
        if expression is not None:
            self.expression=expression
        if color_expression is not None:
            self.color_expression=color_expression
        
        self.mark_update('reconfigurated')
    
    def evaluate_field(self, antenna, force_eval=False, in_dB=False):
        field=None
        if str(type(self.expression))=="<class 'str'>":
            if self.expression=='F':
                field = antenna.F
            elif self.expression=='Ftheta':
                field = np.absolute(antenna.Ftheta)
            elif self.expression=='Fphi':
                field = np.absolute(antenna.Fphi)
            elif self.expression=='Frhcp':
                field = np.absolute(antenna.Frhcp)
            elif self.expression=='Flhcp':
                field = np.absolute(antenna.Flhcp)
            elif self.expression=='D':
                field = antenna.F
            elif self.expression=='Dtheta':
                field = antenna.Ftheta
            elif self.expression=='Dphi':
                field = antenna.Fphi
            elif self.expression=='rE':
                field = 1j*Antenna.constants['eta']*Antenna.constants['k']*antenna.F/(4*np.pi)
            elif self.expression=='rEtheta':
                field = 1j*Antenna.constants['eta']*Antenna.constants['k']*antenna.Ftheta/(4*np.pi)
            elif self.expression=='rEphi':
                field = 1j*Antenna.constants['eta']*Antenna.constants['k']*antenna.Fphi/(4*np.pi)
            else:
                new_vars = {
                    'F': antenna.F,
                    'Ftheta': antenna.Ftheta,
                    'Fphi': antenna.Fphi,
                    'Frhcp': antenna.Frhcp,
                    'Flhcp': antenna.Flhcp,
                    'L': antenna.evaluation_arguments['dipole length'],
                    'S': antenna.evaluation_arguments['loop dipole area'],
                    'theta': antenna.mesh_theta,
                    'phi': antenna.mesh_phi,
                    'mesh_theta': antenna.mesh_theta,
                    'mesh_phi': antenna.mesh_phi
                }
                for key in Antenna.constants.keys():
                    new_vars[key] = Antenna.constants[key]
                field = NEP.eval(expression=self.expression,variables=new_vars)
        # elif str(type(self.expression))=="<class 'Analysis.Analysis'>":
        #     pass
        if in_dB:
            return 20*np.log10(field)
        else:
            return field
    
    def evaluate_color(self, antenna, force_eval=False):
        color=None
        if str(type(self.color_expression))=="<class 'str'>":
            if self.color_expression=='':
                pass
            elif self.color_expression=='F':
                color = antenna.F
            elif self.color_expression=='Ftheta':
                color = np.absolute(antenna.Ftheta)
            elif self.color_expression=='Fphi':
                color = np.absolute(antenna.Fphi)
            elif self.color_expression=='D':
                color = antenna.F
            elif self.color_expression=='Dtheta':
                color = antenna.Ftheta
            elif self.color_expression=='Dphi':
                color = antenna.Fphi
            elif self.color_expression=='rE':
                color = 1j*Antenna.constants['eta']*Antenna.constants['k']*antenna.F/(4*np.pi)
            elif self.color_expression=='rEtheta':
                color = 1j*Antenna.constants['eta']*Antenna.constants['k']*antenna.Ftheta/(4*np.pi)
            elif self.color_expression=='rEphi':
                color = 1j*Antenna.constants['eta']*Antenna.constants['k']*antenna.Fphi/(4*np.pi)
            else:
                new_vars = {
                    'F': antenna.F,
                    'Ftheta': antenna.Ftheta,
                    'Fphi': antenna.Fphi,
                    'L': antenna.evaluation_arguments['dipole length'],
                    'S': antenna.evaluation_arguments['loop dipole area'],
                    'theta': antenna.mesh_theta,
                    'phi': antenna.mesh_phi,
                    'mesh_theta': antenna.mesh_theta,
                    'mesh_phi': antenna.mesh_phi
                }
                for key in Antenna.constants.keys():
                    new_vars[key] = Antenna.constants[key]
                color = NEP.eval(expression=self.color_expression,variables=new_vars)
        # elif str(type(self.expression))=="<class 'Analysis.Analysis'>":
        #     pass
        
        return color