# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 21:19:07 2023

@author: 160047412
"""

import numpy as np

import Antenna

def run(elevation=0, azimuth=0, roll=0, Ntheta=91, Nphi=91):
    theta=np.linspace(0, 180, Ntheta)
    phi=np.linspace(-180, 180, Nphi)
    
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
    
    antennas =  dict(ideal_dipole=ideal_dipole,
                     ideal_loop_dipole=ideal_loop_dipole,)
    
    # if app is not None:
    #     for antenna in antennas.values():
    #         app.add_antenna(antenna)
    
    return antennas

if __name__=='__main__':
    antennas = run()