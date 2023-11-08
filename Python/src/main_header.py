#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 15:07:12 2023

@author: vitinho
"""

import sys
import os
home_directory = os.path.split(__file__)[0]
path = os.path.join(home_directory, "OptimizationScripts")
sys.path.insert(0,path)
path = os.path.join(home_directory, "Scripts")
sys.path.insert(0,path)
path = os.path.join(path, "AntennasLoaders")
sys.path.insert(0,path)