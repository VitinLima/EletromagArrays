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
antennas_dir = os.path.join(path, 'Antennas')

if not os.path.exists(results_dir):
    os.mkdir(results_dir)

validation_results_dir = os.path.join(results_dir, "Validation")
if not os.path.exists(validation_results_dir):
    os.mkdir(validation_results_dir)

optimization_results_dir = os.path.join(results_dir, "Optimization")
if not os.path.exists(optimization_results_dir):
    os.mkdir(optimization_results_dir)

# comparisons_results_dir = os.path.join(results_dir, "Comparisons")
# if not os.path.exists(comparisons_results_dir):
#     os.mkdir(comparisons_results_dir)

# reference_system_comparison_results_dir = os.path.join(results_dir, "ReferenceSystemComparison")
# if not os.path.exists(comparisons_results_dir):
#     os.mkdir(reference_system_comparison_results_dir)