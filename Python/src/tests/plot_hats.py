#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 17:56:58 2023

@author: vitinho
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_hats(antenna):
    ax = plt.figure().add_subplot(projection='3d')
    
    idxs_1 = 30
    idxs_2 = 30
    
    u = antenna.local_hat_k[idxs_1,idxs_2,0]
    v = antenna.local_hat_k[idxs_1,idxs_2,1]
    w = antenna.local_hat_k[idxs_1,idxs_2,2]
    
    x = np.zeros_like(u)
    y = np.zeros_like(u)
    z = np.zeros_like(u)
    
    ax.quiver(x,y,z,u,v,w,color='b')
    
    x = u
    y = v
    z = w
    
    u = antenna.local_hat_phi[idxs_1,idxs_2,0]
    v = antenna.local_hat_phi[idxs_1,idxs_2,1]
    w = antenna.local_hat_phi[idxs_1,idxs_2,2]
    
    ax.quiver(x,y,z,u,v,w,color='g')
    
    u = antenna.local_hat_theta[idxs_1,idxs_2,0]
    v = antenna.local_hat_theta[idxs_1,idxs_2,1]
    w = antenna.local_hat_theta[idxs_1,idxs_2,2]
    
    ax.quiver(x,y,z,u,v,w,color='r')
    
    ax.set_xlim([-2,2])
    ax.set_ylim([-2,2])
    ax.set_zlim([-2,2])
    
    plt.show()

if __name__=='__main__':
    import sys
    import os
    import numpy as np

    path = os.path.split(os.path.split(__file__)[0])[0]
    sys.path.insert(0, path)

    import Antenna
    import Array

    theta=np.linspace(0, 180, 91)
    phi=np.linspace(-180, 180, 91)
    # antennas_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
    antennas_dir = '/media/vitinho/DADOS/TCC/Antennas'

    file_name = 'antenna-Yagi-4Elements.csv'
    file_path = os.path.join(antennas_dir, file_name)

    hfss_yagi4EL = Antenna.load_from_file(
        file_path,
        name='Yagi 4EL',
        local_theta_deg=theta,
        local_phi_deg=phi,
        load_mesh_from_file=False)
    hfss_yagi4EL.set_position(x=0.0,y=0.0,z=0)
    hfss_yagi4EL.evaluate()
    plot_hats(hfss_yagi4EL)