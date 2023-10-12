# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 18:28:40 2023

@author: 160047412
"""

import numpy as np
import math
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import matplotlib as mpl

from Antenna import Antenna
from Array import Array

constants = dict()
constants['c'] = 299792458 # m/s
constants['f'] = 433e6 # Hz
constants['eta'] = 120*math.pi
constants['lam'] = constants['c']/constants['f'] # m
constants['w'] = 2*math.pi*constants['f'] # rad/s
constants['k'] = 2*math.pi/constants['lam'] # rad/m
# antenna1 = Antenna(constants, phi=np.linspace(-180,180,91), name='Antenna da Fernanda',
#                   theta=np.linspace(0,180,91))

antennas = []
N = 1
for i in range(N):
    antennas.append(Antenna(constants,
                            phi=np.linspace(-180,180,91),
                            theta=np.linspace(0,180,91)))
    antennas[i].position = i*np.array([constants['lam']/2,0,0])
    antennas[i].elevation=45
    antennas[i].evaluate_R()

array = Array(constants, phi=np.linspace(-180, 180, 91), theta=np.linspace(0, 180, 91))
for ant in antennas:
    array.add_antenna(ant)
array.evaluate()

current_antenna = array



# fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

# ls = LightSource(270, 45)
# # To use a custom hillshading mode, override the built-in shading and pass
# # in the rgb colors of the shaded surface calculated from "shade".
# rgb = ls.shade(array.F, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
# surf = ax.plot_surface(array.mesh_phi, array.mesh_theta, array.F, rstride=1, cstride=1, facecolors=rgb,
#                         linewidth=0, antialiased=False, shade=False)

# # surf = ax.plot_surface(antenna.mesh_phi, antenna.mesh_theta, antenna.rE)

# plt.show()



# fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

# ls = LightSource(270, 45)
# # To use a custom hillshading mode, override the built-in shading and pass
# # in the rgb colors of the shaded surface calculated from "shade".

# R = current_antenna.F[:,:,np.newaxis] *current_antenna.hat_k

# rgb = ls.shade(current_antenna.F, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
# surf = ax.plot_surface(R[:,:,0], R[:,:,1], R[:,:,2], rstride=1, cstride=1, facecolors=rgb,
#                         linewidth=0, antialiased=False, shade=False)

# # surf = ax.plot_surface(antenna.mesh_phi, antenna.mesh_theta, antenna.rE)

# plt.show()



fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

R = current_antenna.F[:,:,np.newaxis] *current_antenna.hat_k

jet = mpl.colormaps['jet']
C = (current_antenna.F-current_antenna.F.min())/(current_antenna.F.max()-current_antenna.F.min())
rgb = jet(C)
surf = ax.plot_surface(R[:,:,0], R[:,:,1], R[:,:,2], rstride=1, cstride=1, facecolors=rgb,
                        linewidth=0, antialiased=False)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# surf = ax.plot_surface(antenna.mesh_phi, antenna.mesh_theta, antenna.rE)

plt.show()