# -*- coding: utf-8 -*-
"""
Created on Sat May 13 20:04:57 2023

@author: 160047412
"""

import os
import numpy as np

import Antenna

def run(Ntheta=91, Nphi=91, antennas_dir='/media/vitinho/DADOS/TCC/Antennas'):
    # antennas_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
    
    theta=np.linspace(0, 90, Ntheta)
    phi=np.linspace(-180, 180, Nphi)
    
    antenna_path = os.path.join(antennas_dir, '1Y-4EL.csv')
    HFSS_1Y4EL = Antenna.Antenna(name='HFSS 1Y-4EL',
                                  theta=theta,
                                  phi=phi)
    HFSS_1Y4EL.set_evaluation_method('load file')
    HFSS_1Y4EL.evaluation_arguments['file path'] = antenna_path
    HFSS_1Y4EL.evaluation_arguments['load mesh from file'] = False
    HFSS_1Y4EL.set_orientation(elevation=0, azimuth=0, roll=0)
    HFSS_1Y4EL.evaluate()
    
    antenna_path = os.path.join(antennas_dir, '2Y-4EL.csv')
    HFSS_2Y4EL = Antenna.Antenna(name='HFSS 2Y-4EL',
                                  theta=theta,
                                  phi=phi)
    HFSS_2Y4EL.set_evaluation_method('load file')
    HFSS_2Y4EL.evaluation_arguments['file path'] = antenna_path
    HFSS_2Y4EL.evaluation_arguments['load mesh from file'] = False
    HFSS_2Y4EL.set_orientation(elevation=0, azimuth=0, roll=0)
    HFSS_2Y4EL.evaluate()
    
    antenna_path = os.path.join(antennas_dir, '3Y-4EL.csv')
    HFSS_3Y4EL = Antenna.Antenna(name='HFSS 3Y-4EL',
                                  theta=theta,
                                  phi=phi)
    HFSS_3Y4EL.set_evaluation_method('load file')
    HFSS_3Y4EL.evaluation_arguments['file path'] = antenna_path
    HFSS_3Y4EL.evaluation_arguments['load mesh from file'] = False
    HFSS_3Y4EL.set_orientation(elevation=0, azimuth=0, roll=0)
    HFSS_3Y4EL.evaluate()
    
    antenna_path = os.path.join(antennas_dir, '4Y-4EL.csv')
    HFSS_4Y4EL = Antenna.Antenna(name='HFSS 4Y-4EL',
                                  theta=theta,
                                  phi=phi)
    HFSS_4Y4EL.set_evaluation_method('load file')
    HFSS_4Y4EL.evaluation_arguments['file path'] = antenna_path
    HFSS_4Y4EL.evaluation_arguments['load mesh from file'] = False
    HFSS_4Y4EL.set_orientation(elevation=0, azimuth=0, roll=0)
    HFSS_4Y4EL.evaluate()
    
    antenna_path = os.path.join(antennas_dir, '5Y-4EL.csv')
    HFSS_5Y4EL = Antenna.Antenna(name='HFSS 5Y-4EL',
                                  theta=theta,
                                  phi=phi)
    HFSS_5Y4EL.set_evaluation_method('load file')
    HFSS_5Y4EL.evaluation_arguments['file path'] = antenna_path
    HFSS_5Y4EL.evaluation_arguments['load mesh from file'] = False
    HFSS_5Y4EL.set_orientation(elevation=0, azimuth=0, roll=0)
    HFSS_5Y4EL.evaluate()
    
    antennas = dict(HFSS_1Y4EL=HFSS_1Y4EL,
                    HFSS_2Y4EL=HFSS_2Y4EL,
                    HFSS_3Y4EL=HFSS_3Y4EL,
                    HFSS_4Y4EL=HFSS_4Y4EL,
                    HFSS_5Y4EL=HFSS_5Y4EL,)
    
    return antennas

if __name__=='__main__':
    antennas = run()