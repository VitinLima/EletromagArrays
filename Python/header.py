#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 00:44:10 2023

@author: vitinho
"""

import sys
import os
src_dir = os.path.split(__file__)[0]
results_dir = os.path.join(src_dir, 'Images')
sys.path.insert(0, src_dir)

path = os.path.split(src_dir)[0]
path = os.path.split(path)[0]
antennas_dir = os.path.join(path, 'Antennas')