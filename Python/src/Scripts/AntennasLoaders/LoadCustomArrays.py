# -*- coding: utf-8 -*-
"""
Created on Wed May 24 22:41:12 2023

@author: 160047412
"""

import numpy as np

import AntennasLoaders.LoadHFSSYagis

import Array

def run(elevation=0, azimuth=0, roll=0, Ntheta=91, Nphi=91, antennas_dict=None):
    theta=np.linspace(0, 90, Ntheta)
    phi=np.linspace(-180, 180, Nphi)
    
    if antennas_dict==None:
        antennas_dict=AntennasLoaders.LoadHFSSYagis.run(Ntheta=Ntheta,Nphi=Nphi)
    
    hfss_yagi3EL = antennas_dict['hfss_yagi3EL']
    hfss_yagi3EL_V = antennas_dict['hfss_yagi3EL_V']
    
    array_H = Array.Array(name='Optimized Array H',
                          theta=theta,
                          phi=phi,
                          antennas=[hfss_yagi3EL.copy() for i in range(4)])
    array_H.antennas[0].set_current(magnitude=-1)
    array_H.antennas[0].set_orientation(azimuth=180)
    array_H.antennas[1].set_current(magnitude=-1)
    array_H.antennas[1].set_orientation(azimuth=180)
    array_H.evaluate()
    
    array_V = Array.Array(name='Optimized Array V',
                          theta=theta,
                          phi=phi,
                          antennas=[hfss_yagi3EL_V.copy() for i in range(4)])
    array_V.antennas[0].set_current(magnitude=-1)
    array_V.antennas[0].set_orientation(azimuth=180)
    array_V.antennas[1].set_current(magnitude=-1)
    array_V.antennas[1].set_orientation(azimuth=180)
    array_V.evaluate()
    
    array_RHCP = Array.Array(name='Optimized Array RHCP',
                          theta=theta,
                          phi=phi,
                          antennas=[hfss_yagi3EL_V.copy(),
                                    hfss_yagi3EL.copy(),
                                    hfss_yagi3EL_V.copy(),
                                    hfss_yagi3EL.copy(),])
    array_RHCP.antennas[0].set_current(magnitude=-1)
    array_RHCP.antennas[0].set_orientation(azimuth=180)
    array_RHCP.antennas[1].set_current(magnitude=-1)
    array_RHCP.antennas[1].set_orientation(azimuth=180)
    array_RHCP.evaluate()
    
    antennas_dict['array_H']=array_H
    antennas_dict['array_V']=array_V
    antennas_dict['array_RHCP']=array_RHCP
    
    return antennas_dict