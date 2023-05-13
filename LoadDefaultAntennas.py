# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 21:19:07 2023

@author: 160047412
"""

import os
import numpy as np

import Antenna
import Array

def load_default_antennas(elevation=0, azimuth=0, roll=0, Ntheta=31, Nphi=31):
    theta=np.linspace(0, 180, Ntheta)
    phi=np.linspace(-180, 180, Nphi)
    antennas_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
    
    ideal_dipole = Antenna.Antenna(name='Ideal Dipole',
                        theta=theta.copy(),
                        phi=phi.copy(),
                        evaluate_as='ideal dipole')
    ideal_dipole.evaluate()
    
    ideal_loop_dipole = Antenna.Antenna(name='Ideal Loop Dipole',
                        theta=theta.copy(),
                        phi=phi.copy(),
                        evaluate_as='ideal loop dipole')
    ideal_loop_dipole.evaluate()
    
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
    
    theta=np.linspace(0, 90, Ntheta)
    phi=np.linspace(-180, 180, Nphi)
    
    array_H = Array.Array(name='H',
                          theta=theta,
                          phi=phi,
                          antennas=[antenna_3_H.copy() for i in range(4)])
    array_H.antennas[0].set_current(current_mag=-1)
    array_H.antennas[0].set_orientation(azimuth=180)
    array_H.antennas[1].set_current(current_mag=-1)
    array_H.antennas[1].set_orientation(azimuth=180)
    array_H.evaluate()
    
    array_V = Array.Array(name='V',
                          theta=theta,
                          phi=phi,
                          antennas=[antenna_3_V.copy() for i in range(4)])
    array_V.antennas[0].set_current(current_mag=-1)
    array_V.antennas[0].set_orientation(azimuth=180)
    array_V.antennas[1].set_current(current_mag=-1)
    array_V.antennas[1].set_orientation(azimuth=180)
    array_V.evaluate()
    
    array_RHCP = Array.Array(name='RHCP',
                          theta=theta,
                          phi=phi,
                          antennas=[antenna_3_V.copy(),
                                    antenna_3_H.copy(),
                                    antenna_3_V.copy(),
                                    antenna_3_H.copy(),])
    array_RHCP.antennas[0].set_current(current_mag=-1)
    array_RHCP.antennas[0].set_orientation(azimuth=180)
    array_RHCP.antennas[1].set_current(current_mag=-1)
    array_RHCP.antennas[1].set_orientation(azimuth=180)
    array_RHCP.evaluate()
    
    array_validation_1Y_4El = Array.Array(name='1Y-4El',
                                          theta=theta,
                                          phi=phi,
                                          antennas=[antenna_4_H.copy(),])
    array_validation_1Y_4El.antennas[0].set_orientation(roll=0, elevation=0, azimuth=0)
    array_validation_1Y_4El.antennas[0].set_position(x=0, y=0, z=0)
    array_validation_1Y_4El.evaluate()
    
    array_validation_2Y_4El = Array.Array(name='2Y-4El',
                                                      theta=theta,
                                                      phi=phi,
                                                      antennas=[antenna_4_H.copy(),
                                                                antenna_4_H.copy(),])
    array_validation_2Y_4El.antennas[0].set_orientation(roll=0, elevation=0, azimuth=0)
    array_validation_2Y_4El.antennas[0].set_position(x=0, y=0, z=0)
    array_validation_2Y_4El.antennas[1].set_orientation(roll=0, elevation=0, azimuth=45)
    array_validation_2Y_4El.antennas[1].set_position(x=0, y=1.5, z=0)
    array_validation_2Y_4El.evaluate()
    
    array_validation_3Y_4El = Array.Array(name='3Y-4El',
                                                      theta=theta,
                                                      phi=phi,
                                                      antennas=[antenna_4_H.copy(),
                                                                antenna_4_H.copy(),
                                                                antenna_4_H.copy(),])
    array_validation_3Y_4El.antennas[0].set_orientation(roll=0, elevation=0, azimuth=0)
    array_validation_3Y_4El.antennas[0].set_position(x=0, y=0, z=0)
    array_validation_3Y_4El.antennas[1].set_orientation(roll=0, elevation=0, azimuth=45)
    array_validation_3Y_4El.antennas[1].set_position(x=0, y=1.5, z=0)
    array_validation_3Y_4El.antennas[2].set_orientation(roll=0, elevation=-45, azimuth=-45)
    array_validation_3Y_4El.antennas[2].set_position(x=0, y=-1.5, z=0)
    array_validation_3Y_4El.evaluate()
    
    array_validation_4Y_4El = Array.Array(name='4Y-4El',
                                                      theta=theta,
                                                      phi=phi,
                                                      antennas=[antenna_4_H.copy(),
                                                                antenna_4_H.copy(),
                                                                antenna_4_H.copy(),
                                                                antenna_4_H.copy(),])
    array_validation_4Y_4El.antennas[0].set_orientation(roll=0, elevation=0, azimuth=0)
    array_validation_4Y_4El.antennas[0].set_position(x=0, y=0, z=0)
    array_validation_4Y_4El.antennas[1].set_orientation(roll=0, elevation=0, azimuth=45)
    array_validation_4Y_4El.antennas[1].set_position(x=0, y=1.5, z=0)
    array_validation_4Y_4El.antennas[2].set_orientation(roll=0, elevation=-45, azimuth=-45)
    array_validation_4Y_4El.antennas[2].set_position(x=0, y=-1.5, z=0)
    array_validation_4Y_4El.antennas[3].set_orientation(roll=0, elevation=-45, azimuth=135)
    array_validation_4Y_4El.antennas[3].set_position(x=0.34, y=-3.14, z=1.423)
    array_validation_4Y_4El.evaluate()
    
    array_validation_5Y_4El = Array.Array(name='5Y-4El',
                                                      theta=theta,
                                                      phi=phi,
                                                      antennas=[antenna_4_H.copy(),
                                                                antenna_4_H.copy(),
                                                                antenna_4_H.copy(),
                                                                antenna_4_H.copy(),
                                                                antenna_4_H.copy(),])
    array_validation_5Y_4El.antennas[0].set_orientation(roll=0, elevation=0, azimuth=0)
    array_validation_5Y_4El.antennas[0].set_position(x=0, y=0, z=0)
    array_validation_5Y_4El.antennas[1].set_orientation(roll=0, elevation=0, azimuth=45)
    array_validation_5Y_4El.antennas[1].set_position(x=0, y=1.5, z=0)
    array_validation_5Y_4El.antennas[2].set_orientation(roll=0, elevation=-45, azimuth=-45)
    array_validation_5Y_4El.antennas[2].set_position(x=0, y=-1.5, z=0)
    array_validation_5Y_4El.antennas[3].set_orientation(roll=0, elevation=-45, azimuth=135)
    array_validation_5Y_4El.antennas[3].set_position(x=0.34, y=-3.14, z=1.423)
    array_validation_5Y_4El.antennas[4].set_orientation(roll=36, elevation=72, azimuth=14)
    array_validation_5Y_4El.antennas[4].set_position(x=0.83, y=1.19, z=-0.72)
    array_validation_5Y_4El.evaluate()
    
    return dict(ideal_dipole=ideal_dipole,
                ideal_loop_dipole=ideal_loop_dipole,
                antenna_1_H=antenna_1_H,
                antenna_2_H=antenna_2_H,
                antenna_3_H=antenna_3_H,
                antenna_4_H=antenna_4_H,
                antenna_1_V=antenna_1_V,
                antenna_2_V=antenna_2_V,
                antenna_3_V=antenna_3_V,
                antenna_4_V=antenna_4_V,
                array_H=array_H,
                array_V=array_V,
                array_RHCP=array_RHCP,
                array_validation_1Y_4El=array_validation_1Y_4El,
                array_validation_2Y_4El=array_validation_2Y_4El,
                array_validation_3Y_4El=array_validation_3Y_4El,
                array_validation_4Y_4El=array_validation_4Y_4El,
                array_validation_5Y_4El=array_validation_5Y_4El,)