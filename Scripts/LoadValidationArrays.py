# -*- coding: utf-8 -*-
"""
Created on Sat May 13 20:04:57 2023

@author: 160047412
"""

import numpy as np

def run(app=None, Ntheta=91, Nphi=91):
    import os
    import Antenna
    antenna_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
    
    theta=np.linspace(0, 180, Ntheta)
    phi=np.linspace(-180, 180, Nphi)
    
    antenna_path = os.path.join(antenna_dir, '1Y-4EL.csv')
    HFSS_1Y_4EL = Antenna.Antenna(name='HFSS 1Y-4EL',
                        theta=theta,
                        phi=phi)
    HFSS_1Y_4EL.set_evaluation_method('load file')
    HFSS_1Y_4EL.evaluation_arguments['file path'] = antenna_path
    HFSS_1Y_4EL.evaluation_arguments['load mesh from file'] = False
    HFSS_1Y_4EL.set_orientation(elevation=0, azimuth=0, roll=0)
    HFSS_1Y_4EL.evaluate()
    
    antenna_path = os.path.join(antenna_dir, '2Y-4EL.csv')
    HFSS_2Y_4EL = Antenna.Antenna(name='HFSS 2Y-4EL',
                        theta=theta,
                        phi=phi)
    HFSS_2Y_4EL.set_evaluation_method('load file')
    HFSS_2Y_4EL.evaluation_arguments['file path'] = antenna_path
    HFSS_2Y_4EL.evaluation_arguments['load mesh from file'] = False
    HFSS_2Y_4EL.set_orientation(elevation=0, azimuth=0, roll=0)
    HFSS_2Y_4EL.evaluate()
    
    antenna_path = os.path.join(antenna_dir, '3Y-4EL.csv')
    HFSS_3Y_4EL = Antenna.Antenna(name='HFSS 3Y-4EL',
                        theta=theta,
                        phi=phi)
    HFSS_3Y_4EL.set_evaluation_method('load file')
    HFSS_3Y_4EL.evaluation_arguments['file path'] = antenna_path
    HFSS_3Y_4EL.evaluation_arguments['load mesh from file'] = False
    HFSS_3Y_4EL.set_orientation(elevation=0, azimuth=0, roll=0)
    HFSS_3Y_4EL.evaluate()
    
    antenna_path = os.path.join(antenna_dir, '4Y-4EL.csv')
    HFSS_4Y_4EL = Antenna.Antenna(name='HFSS 4Y-4EL',
                        theta=theta,
                        phi=phi)
    HFSS_4Y_4EL.set_evaluation_method('load file')
    HFSS_4Y_4EL.evaluation_arguments['file path'] = antenna_path
    HFSS_4Y_4EL.evaluation_arguments['load mesh from file'] = False
    HFSS_4Y_4EL.set_orientation(elevation=0, azimuth=0, roll=0)
    HFSS_4Y_4EL.evaluate()
    
    antenna_path = os.path.join(antenna_dir, '5Y-4EL.csv')
    HFSS_5Y_4EL = Antenna.Antenna(name='HFSS 5Y-4EL',
                        theta=theta,
                        phi=phi)
    HFSS_5Y_4EL.set_evaluation_method('load file')
    HFSS_5Y_4EL.evaluation_arguments['file path'] = antenna_path
    HFSS_5Y_4EL.evaluation_arguments['load mesh from file'] = False
    HFSS_5Y_4EL.set_orientation(elevation=0, azimuth=0, roll=0)
    HFSS_5Y_4EL.evaluate()
    
    antennas = dict(HFSS_1Y_4EL=HFSS_1Y_4EL,
                    HFSS_2Y_4EL=HFSS_2Y_4EL,
                    HFSS_3Y_4EL=HFSS_3Y_4EL,
                    HFSS_4Y_4EL=HFSS_4Y_4EL,
                    HFSS_5Y_4EL=HFSS_5Y_4EL,)
    
    if app is not None:
        for antenna in antennas.values():
            app.add_antenna(antenna)
    
    return antennas