# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 21:19:07 2023

@author: 160047412
"""

import os
import numpy as np

import Antenna

def load_default_antennas(elevation=-90, azimuth=0, roll=0):
    theta=np.linspace(0, 180, 91)
    phi=np.linspace(-180, 180, 91)
    antennas_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
    
    antenna_path = os.path.join(antennas_dir, 'antenna-Dipole.csv')
    antenna_1_H = Antenna.Antenna(name='Dipole antenna',
                        theta=theta.copy(),
                        phi=phi.copy())
    antenna_1_H.set_evaluation_method('load file')
    antenna_1_H.evaluation_arguments['file path'] = antenna_path
    antenna_1_H.evaluation_arguments['load mesh from file'] = False
    antenna_1_H.set_orientation(elevation=elevation, azimuth=azimuth, roll=roll)
    antenna_1_H.evaluate()
    antenna_1_V = antenna_1_H.copy()
    antenna_1_V.set_orientation(roll=90);
    antenna_1_V.set_current(current_phase=90);
    antenna_1_V.name += " V" 
    antenna_1_V.evaluate()
    
    antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-2Elements.csv')
    antenna_2_H = Antenna.Antenna(name='Yagi 2 elements',
                        theta=theta.copy(),
                        phi=phi.copy())
    antenna_2_H.set_evaluation_method('load file')
    antenna_2_H.evaluation_arguments['file path'] = antenna_path
    antenna_2_H.evaluation_arguments['load mesh from file'] = False
    antenna_2_H.set_orientation(elevation=elevation, azimuth=azimuth, roll=roll)
    antenna_2_H.evaluate()
    antenna_2_V = antenna_2_H.copy()
    antenna_2_V.set_orientation(roll=90);
    antenna_2_V.set_current(current_phase=90);
    antenna_2_V.name += " V"
    antenna_2_V.evaluate()
    
    antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-3Elements.csv')
    antenna_3_H = Antenna.Antenna(name='Yagi 3 elements',
                        theta=theta.copy(),
                        phi=phi.copy())
    antenna_3_H.set_evaluation_method('load file')
    antenna_3_H.evaluation_arguments['file path'] = antenna_path
    antenna_3_H.evaluation_arguments['load mesh from file'] = False
    antenna_3_H.set_orientation(elevation=elevation, azimuth=azimuth, roll=roll)
    antenna_3_H.evaluate()
    antenna_3_V = antenna_3_H.copy()
    antenna_3_V.set_orientation(roll=90);
    antenna_3_V.set_current(current_phase=90);
    antenna_3_V.name += " V"
    antenna_3_V.evaluate()
    
    antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-4Elements.csv')
    antenna_4_H = Antenna.Antenna(name='Yagi 4 elements',
                        theta=theta.copy(),
                        phi=phi.copy())
    antenna_4_H.set_evaluation_method('load file')
    antenna_4_H.evaluation_arguments['file path'] = antenna_path
    antenna_4_H.evaluation_arguments['load mesh from file'] = False
    antenna_4_H.set_orientation(elevation=elevation, azimuth=azimuth, roll=roll)
    antenna_4_H.evaluate()
    antenna_4_V = antenna_4_H.copy()
    antenna_4_V.set_orientation(roll=90);
    antenna_4_V.set_current(current_phase=90);
    antenna_4_V.name += " V"
    antenna_4_V.evaluate()
    
    return antenna_1_H,antenna_2_H,antenna_3_H,antenna_4_H,antenna_1_V,antenna_2_V,antenna_3_V,antenna_4_V