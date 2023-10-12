# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:36:17 2023

@author: 160047412
"""

import os
import pickle
import numpy as np

from Antenna import Antenna
from Array import Array
from Analysis import Analysis

def copy_antenna(antenna):
    new_antenna = Antenna(name=antenna.name,
                          phi=antenna.phi,
                          theta=antenna.theta,
                          current_mag=antenna.current_mag,
                          current_phase=antenna.current_phase,
                          roll=antenna.roll,
                          elevation=antenna.elevation,
                          azimuth=antenna.azimuth,
                          x=antenna.x, y=antenna.y, z=antenna.z,
                          evaluate_as=antenna.evaluate_as)
    new_antenna.evaluation_arguments = antenna.evaluation_arguments.copy()
    new_antenna.evaluate()
    return new_antenna

def copy_array(array):
    new_array = Array(name=array.name,
                      phi=array.phi,
                      theta=array.theta,
                      current_mag=array.current_mag,
                      current_phase=array.current_phase,
                      roll=array.roll,
                      elevation=array.elevation,
                      azimuth=array.azimuth,
                      x=array.x, y=array.y, z=array.z,
                      x_mirror=array.x_mirror,
                      y_mirror=array.y_mirror,
                      z_mirror=array.z_mirror,
                      current_mirror=array.current_mirror,
                      x_symmetry=array.x_symmetry,
                      y_symmetry=array.y_symmetry,
                      z_symmetry=array.z_symmetry)
    for antenna in array.antennas:
        if str(type(antenna))=="<class 'Antenna.Antenna'>":
            new_array.add_antenna(copy_antenna(antenna))
        elif str(type(antenna))=="<class 'Array.Array'>":
            new_array.add_antenna(copy_array(antenna))
    new_array.evaluate()
    return new_array

filedir = 'Optimization Results Theta'
filename = os.path.join(filedir,'best array with 3 antenna and cost 139.7724336651349.dat')
with open(filename, 'rb') as f:
    antenna = pickle.load(f)

if str(type(antenna))=="<class 'Antenna.Antenna'>":
    new_antenna = copy_antenna(antenna)
elif str(type(antenna))=="<class 'Array.Array'>":
    new_antenna = copy_array(antenna)