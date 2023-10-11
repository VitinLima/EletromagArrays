# -*- coding: utf-8 -*-
"""
Created on Wed May 24 22:43:33 2023

@author: 160047412
"""

import os
import numpy as np

import Antenna

def run(elevation=0, azimuth=0, roll=0, Ntheta=91, Nphi=91, antennas_dir='/media/vitinho/DADOS/TCC/Antennas'):
    theta=np.linspace(0, 180, Ntheta)
    phi=np.linspace(-180, 180, Nphi)
    
    antennas_dict = dict()
    
    # antennas_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
    
    
    antenna_path = os.path.join(antennas_dir, 'antenna-Dipole.csv')
    hfss_yagi1EL = Antenna.Antenna(name='Dipole antenna',
                        theta=theta.copy(),
                        phi=phi.copy())
    hfss_yagi1EL.set_evaluation_method('load file')
    hfss_yagi1EL.evaluation_arguments['file path'] = antenna_path
    hfss_yagi1EL.evaluation_arguments['load mesh from file'] = False
    hfss_yagi1EL.set_orientation(elevation=elevation, azimuth=azimuth, roll=roll)
    hfss_yagi1EL.evaluate()
    hfss_yagi1EL_V = hfss_yagi1EL.copy()
    hfss_yagi1EL_V.set_orientation(roll=90);
    hfss_yagi1EL_V.set_current(phase=90);
    hfss_yagi1EL_V.name += " V" 
    hfss_yagi1EL_V.evaluate()
    
    antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-2Elements.csv')
    hfss_yagi2EL = Antenna.Antenna(name='Yagi 2 elements',
                        theta=theta.copy(),
                        phi=phi.copy())
    hfss_yagi2EL.set_evaluation_method('load file')
    hfss_yagi2EL.evaluation_arguments['file path'] = antenna_path
    hfss_yagi2EL.evaluation_arguments['load mesh from file'] = False
    hfss_yagi2EL.set_orientation(elevation=elevation, azimuth=azimuth, roll=roll)
    hfss_yagi2EL.evaluate()
    hfss_yagi2EL_V = hfss_yagi2EL.copy()
    hfss_yagi2EL_V.set_orientation(roll=90);
    hfss_yagi2EL_V.set_current(phase=90);
    hfss_yagi2EL_V.name += " V"
    hfss_yagi2EL_V.evaluate()
    
    antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-3Elements.csv')
    hfss_yagi3EL = Antenna.Antenna(name='Yagi 3 elements',
                        theta=theta.copy(),
                        phi=phi.copy())
    hfss_yagi3EL.set_evaluation_method('load file')
    hfss_yagi3EL.evaluation_arguments['file path'] = antenna_path
    hfss_yagi3EL.evaluation_arguments['load mesh from file'] = False
    hfss_yagi3EL.set_orientation(elevation=elevation, azimuth=azimuth, roll=roll)
    hfss_yagi3EL.evaluate()
    hfss_yagi3EL_V = hfss_yagi3EL.copy()
    hfss_yagi3EL_V.set_orientation(roll=90);
    hfss_yagi3EL_V.set_current(phase=90);
    hfss_yagi3EL_V.name += " V"
    hfss_yagi3EL_V.evaluate()
    
    antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-4Elements.csv')
    hfss_yagi4EL = Antenna.Antenna(name='Yagi 4 elements',
                        theta=theta.copy(),
                        phi=phi.copy())
    hfss_yagi4EL.set_evaluation_method('load file')
    hfss_yagi4EL.evaluation_arguments['file path'] = antenna_path
    hfss_yagi4EL.evaluation_arguments['load mesh from file'] = False
    hfss_yagi4EL.set_orientation(elevation=elevation, azimuth=azimuth, roll=roll)
    hfss_yagi4EL.evaluate()
    hfss_yagi4EL_V = hfss_yagi4EL.copy()
    hfss_yagi4EL_V.set_orientation(roll=90);
    hfss_yagi4EL_V.set_current(phase=90);
    hfss_yagi4EL_V.name += " V"
    hfss_yagi4EL_V.evaluate()
    
    antennas_dict['hfss_yagi1EL']=hfss_yagi1EL
    antennas_dict['hfss_yagi2EL']=hfss_yagi2EL
    antennas_dict['hfss_yagi3EL']=hfss_yagi3EL
    antennas_dict['hfss_yagi4EL']=hfss_yagi4EL
    antennas_dict['hfss_yagi1EL_V']=hfss_yagi1EL_V
    antennas_dict['hfss_yagi2EL_V']=hfss_yagi2EL_V
    antennas_dict['hfss_yagi3EL_V']=hfss_yagi3EL_V
    antennas_dict['hfss_yagi4EL_V']=hfss_yagi4EL_V
    
    return antennas_dict

if __name__=='__main__':
    antennas = run()