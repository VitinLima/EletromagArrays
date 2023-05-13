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
    z = V1.x*V2.y - V1.y*V1.x
    return Vector(x=x,y=y,z=z)

def dot_product(V1, V2):
    return V1.x*V2.x+V1.y*V2.y+V1.z*V2.z

def norm(V):
    return np.sqrt(V.x*V.x + V.y*V.y + V.z*V.z)

def normalize(V):
    norm_V = norm(V)
    if norm_V > epsilon:
        V.x /= epsilon
        V.y /= epsilon
        V.z /= epsilon

class Geometry:
    pass

class Point(Geometry):
    def __init__(self, x=0, y=0, z=0):
        self.x=x
        self.y=y
        self.z=z

class Vector(Geometry):
    def __init__(self, x=0, y=0, z=0):
        self.x=x
        self.y=y
        self.z=z

class Plane(Geometry):
    def __init__(self, x=0, y=0, z=1):
        self.x = x
        self.y = y
        self.z = z

class Axis(Geometry):
    def __init__(self, x=1, y=0, z=0):
        self.x=x
        self.y=y
        self.z=z

class ReferenceSystem(Geometry):
    def __init__(self,
                 principal_plane=Plane(),
                 x_axis=Axis(),
                 origin=Point()):
        self.principal_plane=principal_plane
        self.x_axis=x_axis
        y_vector = cross_product(principal_plane, x_axis)
        normalize(y_vector)
        self.y_axis = Axis(x=y_vector.x,y=y_vector.y,z=y_vector.z)
        self.R = np.array([[1,0,0],[0,1,0],[0,0,1]])