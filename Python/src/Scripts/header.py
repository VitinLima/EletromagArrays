#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 00:44:10 2023

@author: vitinho
"""

import sys
import os
src_path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, src_path)
import main_header

path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, path)

python_path = os.path.split(path)[0]
results_dir = os.path.join(python_path, 'ExportedResults')
path = os.path.split(python_path)[0]
home_dir = os.path.split(path)[0]
path = os.path.split(home_dir)[0]
antennas_dir = os.path.join(path, 'Antennas')