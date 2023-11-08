# -*- coding: utf-8 -*-
"""
Created on Wed May 24 22:46:38 2023

@author: 160047412
"""

import sys
import os
import ImportAntennasPath
home_directory = ImportAntennasPath.home_directory
antennas_dir = ImportAntennasPath.antennas_dir

import numpy as np

import Scripts.AntennasLoaders.LoadHFSSYagis

import Array

def run(elevation=0, azimuth=0, roll=0,
        Ntheta=91, Nphi=91,
        antennas_dict=None):
    
    theta=np.linspace(0, 180, Ntheta)
    phi=np.linspace(-180, 180, Nphi)
    
    if antennas_dict==None:
        antennas_dict=Scripts.AntennasLoaders.LoadHFSSYagis.run(
            Ntheta=Ntheta,
            Nphi=Nphi)
    
    hfss_yagi4EL = antennas_dict['hfss_yagi4EL']
    
    array_validation_1Y4EL = Array.Array(name='1Y-4EL',
                                          theta=theta,
                                          phi=phi,
                                          antennas=[
                                              hfss_yagi4EL.copy(),
                                              ])
    array_validation_1Y4EL.antennas[0].set_orientation(
        roll=0,
        elevation=0,
        azimuth=0)
    array_validation_1Y4EL.antennas[0].set_position(x=0, y=0, z=0)
    array_validation_1Y4EL.evaluate()
    
    array_validation_2Y4EL = Array.Array(name='2Y-4EL',
                                          theta=theta,
                                          phi=phi,
                                          antennas=[
                                              hfss_yagi4EL.copy(),
                                              hfss_yagi4EL.copy(),
                                              ])
    array_validation_2Y4EL.antennas[0].set_orientation(
        roll=0,
        elevation=0,
        azimuth=0)
    array_validation_2Y4EL.antennas[0].set_position(x=0, y=0, z=0)
    array_validation_2Y4EL.antennas[1].set_orientation(
        roll=0,
        elevation=0,
        azimuth=45)
    array_validation_2Y4EL.antennas[1].set_position(x=0, y=1.5, z=0)
    array_validation_2Y4EL.evaluate()
    
    array_validation_3Y4EL = Array.Array(name='3Y-4EL',
                                          theta=theta,
                                          phi=phi,
                                          antennas=[
                                              hfss_yagi4EL.copy(),
                                              hfss_yagi4EL.copy(),
                                              hfss_yagi4EL.copy(),
                                              ])
    array_validation_3Y4EL.antennas[0].set_orientation(
        roll=0,
        elevation=0,
        azimuth=0)
    array_validation_3Y4EL.antennas[0].set_position(x=0, y=0, z=0)
    array_validation_3Y4EL.antennas[1].set_orientation(
        roll=0,
        elevation=0,
        azimuth=45)
    array_validation_3Y4EL.antennas[1].set_position(x=0, y=1.5, z=0)
    array_validation_3Y4EL.antennas[2].set_orientation(
        roll=0,
        elevation=-45,
        azimuth=-45)
    array_validation_3Y4EL.antennas[2].set_position(x=0, y=-1.5, z=0)
    array_validation_3Y4EL.evaluate()
    
    array_validation_4Y4EL = Array.Array(name='4Y-4EL',
                                          theta=theta,
                                          phi=phi,
                                          antennas=[
                                              hfss_yagi4EL.copy(),
                                              hfss_yagi4EL.copy(),
                                              hfss_yagi4EL.copy(),
                                              hfss_yagi4EL.copy(),
                                              ])
    array_validation_4Y4EL.antennas[0].set_orientation(
        roll=0, elevation=0, azimuth=0)
    array_validation_4Y4EL.antennas[0].set_position(x=0, y=0, z=0)
    array_validation_4Y4EL.antennas[1].set_orientation(
        roll=0, elevation=0, azimuth=45)
    array_validation_4Y4EL.antennas[1].set_position(x=0, y=1.5, z=0)
    array_validation_4Y4EL.antennas[2].set_orientation(
        roll=0, elevation=-45, azimuth=-45)
    array_validation_4Y4EL.antennas[2].set_position(x=0, y=-1.5, z=0)
    array_validation_4Y4EL.antennas[3].set_orientation(
        roll=0, elevation=-45, azimuth=135)
    array_validation_4Y4EL.antennas[3].set_position(
        x=0.34, y=-3.14, z=1.423)
    array_validation_4Y4EL.evaluate()
    
    array_validation_5Y4EL = Array.Array(name='5Y-4EL',
                                          theta=theta,
                                          phi=phi,
                                          antennas=[
                                              hfss_yagi4EL.copy(),
                                              hfss_yagi4EL.copy(),
                                              hfss_yagi4EL.copy(),
                                              hfss_yagi4EL.copy(),
                                              hfss_yagi4EL.copy(),
                                              ])
    array_validation_5Y4EL.antennas[0].set_orientation(
        roll=0, elevation=0, azimuth=0)
    array_validation_5Y4EL.antennas[0].set_position(
        x=0, y=0, z=0)
    array_validation_5Y4EL.antennas[1].set_orientation(
        roll=0, elevation=0, azimuth=45)
    array_validation_5Y4EL.antennas[1].set_position(
        x=0, y=1.5, z=0)
    array_validation_5Y4EL.antennas[2].set_orientation(
        roll=0, elevation=-45, azimuth=-45)
    array_validation_5Y4EL.antennas[2].set_position(
        x=0, y=-1.5, z=0)
    array_validation_5Y4EL.antennas[3].set_orientation(
        roll=0, elevation=-45, azimuth=135)
    array_validation_5Y4EL.antennas[3].set_position(
        x=0.34, y=-3.14, z=1.423)
    array_validation_5Y4EL.antennas[4].set_orientation(
        roll=0, elevation=72, azimuth=14)
    array_validation_5Y4EL.antennas[4].set_position(
        x=0.83, y=1.19, z=-0.72)
    array_validation_5Y4EL.evaluate()
    
    antennas_dict['array_validation_1Y4EL']=array_validation_1Y4EL
    antennas_dict['array_validation_2Y4EL']=array_validation_2Y4EL
    antennas_dict['array_validation_3Y4EL']=array_validation_3Y4EL
    antennas_dict['array_validation_4Y4EL']=array_validation_4Y4EL
    antennas_dict['array_validation_5Y4EL']=array_validation_5Y4EL
    
    return antennas_dict

if __name__=='__main__':
    antennas = run()