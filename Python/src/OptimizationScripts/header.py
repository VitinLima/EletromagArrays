#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 15:08:46 2023

@author: vitinho
"""

import sys
import os
src_path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, src_path)
import main_header
home_directory = main_header.home_directory