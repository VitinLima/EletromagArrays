# -*- coding: utf-8 -*-
"""
Created on Mon May  1 23:06:40 2023

@author: 160047412
"""

import numpy as np

epsilon = 1e-6

def cross_product(V1, V2):
    x = V1.y*V2.z - V1.z*V2.y
    y = V1.z*V2.x - V1.x*V2.z
    z = V1.x*V2.y - V1.y*V2.x
    return Vector(x=x,y=y,z=z)

def dot_product(V1, V2):
    return V1.x*V2.x+V1.y*V2.y+V1.z*V2.z

def norm(V):
    return np.sqrt(V.x*V.x + V.y*V.y + V.z*V.z)

def normalize(V):
    norm_V = norm(V)
    if norm_V > epsilon:
        V.x /= norm_V
        V.y /= norm_V
        V.z /= norm_V

class Geometry:
    pass

class Point(Geometry):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x=x
        self.y=y
        self.z=z
    
    def to_string(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

class Vector(Geometry):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x=x
        self.y=y
        self.z=z
    
    def to_string(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

class Plane(Geometry):
    def __init__(self, x=0.0, y=0.0, z=1.0):
        self.x = x
        self.y = y
        self.z = z

class Axis(Geometry):
    def __init__(self, x=1.0, y=0.0, z=0.0):
        self.x=x
        self.y=y
        self.z=z
    
    def to_string(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

class ReferenceSystem(Geometry):
    def __init__(self,
                 x_axis=Axis(),
                 z_axis=Axis(x=0.0,z=1.0),
                 origin=Point()):
        self.x_axis=x_axis
        self.z_axis=z_axis
        
        normalize(self.x_axis)
        
        y_vector = cross_product(z_axis, x_axis)
        normalize(y_vector)
        self.y_axis = Axis(x=y_vector.x,y=y_vector.y,z=y_vector.z)
        
        z_vector = cross_product(self.x_axis, self.y_axis)
        normalize(z_vector)
        self.z_axis = Axis(x=z_vector.x,y=z_vector.y,z=z_vector.z)
        
        self.R = np.array([[1,0,0],[0,1,0],[0,0,1]])
        self.elevation=0.0
        self.azimuth=0.0
        
        self.calculate_rotation_matrix()
    
    def calculate_rotation_matrix(self):
        xx = self.x_axis.x
        xy = self.x_axis.y
        xz = self.x_axis.z
        zx = self.z_axis.x
        zy = self.z_axis.y
        zz = self.z_axis.z
        
        self.elevation = np.arctan2(np.sqrt(zy*zy+zx*zx), zz)
        self.azimuth = np.arctan2(xy, xx)
        
        ct = np.cos(self.elevation)
        st = np.sin(self.elevation)
        Relevation = np.zeros((3, 3))
        Relevation[0,0] = ct
        Relevation[0,2] = -st
        Relevation[2,0] = st
        Relevation[1,1] = 1
        Relevation[2,2] = ct
        
        cp = np.cos(self.azimuth)
        sp = np.sin(self.azimuth)
        Razimuth = np.zeros((3, 3))
        Razimuth[0,0] = cp
        Razimuth[0,1] = -sp
        Razimuth[1,0] = sp
        Razimuth[1,1] = cp
        Razimuth[2,2] = 1
        
        self.R = Razimuth@Relevation
    
    # def calculate_transform_matrix(self):
    #     s_mesh_theta = np.arctan2(np.sqrt(s_y*s_y+s_x*s_x), s_z)
        
    #     # ids1 = s_mesh_theta>3*np.pi/4
    #     # ids2 = s_mesh_theta<np.pi/4
        
    #     # s_x[ids1] = s_hat_phi[ids1,1]
    #     # s_y[ids1] = -s_hat_phi[ids1,0]
    #     # s_x[ids2] = s_hat_phi[ids2,1]
    #     # s_y[ids2] = s_hat_phi[ids2,0]
    #     s_mesh_phi = np.arctan2(s_y, s_x)

if __name__=='__main__':
    sq2 = np.sqrt(2)/2
    sq3 = np.sqrt(3)/3
    x = Axis(x=sq2*sq2,y=sq2*sq2,z=sq2)
    z = Axis(x=0.0,z=1.0)
    ref = ReferenceSystem(x_axis=x,z_axis=z)
    
    y = cross_product(z, x)
    normalize(y)
    
    z = cross_product(x, y)
    normalize(z)
    
    angles = np.radians(np.linspace(-180,180,181))
    points = np.zeros((181,3))
    for i in range(181):
        points[i,0] = np.cos(angles[i])
        points[i,1] = np.sin(angles[i])
        points[i,:] = ref.R@points[i,:]
    
    print(z.to_string())
    print('')
    print(ref.x_axis.to_string())
    print(ref.y_axis.to_string())
    print(ref.z_axis.to_string())
    print('')
    print(np.degrees(ref.elevation))
    print(np.degrees(ref.azimuth))
    print('')
    print(norm(ref.x_axis))
    print(norm(ref.y_axis))
    print(norm(ref.z_axis))
    print('')
    print(points)
    
    import matplotlib.pyplot as plt
    
    ax = plt.figure().add_subplot(projection='3d')
    
    ax.quiver(0, 0, 0, x.x, x.y, x.z, length=0.1, normalize=True, color='b')
    ax.quiver(0, 0, 0, y.x, y.y, y.z, length=0.1, normalize=True, color='b')
    ax.quiver(0, 0, 0, z.x, z.y, z.z, length=0.1, normalize=True, color='b')
    
    for i in range(181):
        ax.quiver(0,0,0, points[i,0], points[i,1], points[i,2], length=0.1, normalize=True, color='r')
    
    plt.show()