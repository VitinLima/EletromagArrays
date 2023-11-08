# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 22:52:46 2023

@author: 160047412
"""

import Antenna
import pickle
# import os

def save(obj):
    return (obj.__class__, obj.__dict__)

def restore(cls, attributes):
    obj = cls.__new__(cls)
    obj.__dict__.update(attributes)
    return obj

antenna = Antenna.Antenna()
# class MyClass:
#     def __init__(self):
#         self.a = 1
#         self.b = 2

# w_class = MyClass()

with open('antenna.txt', 'wb') as f:
    pickle.dump(antenna, f)

with open('antenna.txt', 'rb') as f:
    r_class = pickle.load(f)