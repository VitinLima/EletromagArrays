# -*- coding: utf-8 -*-
"""
Created on Sat May 13 18:37:32 2023

@author: 160047412
"""

import sys
import os
path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, path)

import matplotlib.pyplot as plt
plt.close('all')

import Scripts.LoadDefaultAntennas
antennas = Scripts.LoadDefaultAntennas.run(Ntheta=91, Nphi=91)

import Scripts.LoadValidationArrays
antennas.update(Scripts.LoadValidationArrays.run(Ntheta=91, Nphi=91))

import Scripts.ExportResults

# Scripts.ExportResults.run([antennas['array_validation_1Y_4El'],
#                             antennas['array_validation_2Y_4El'],
#                             antennas['array_validation_3Y_4El'],
#                             antennas['array_validation_4Y_4El'],
#                             antennas['array_validation_5Y_4El'],
#                             antennas['HFSS_1Y_4EL'],
#                             antennas['HFSS_2Y_4EL'],
#                             antennas['HFSS_3Y_4EL'],
#                             antennas['HFSS_4Y_4EL'],
#                             antennas['HFSS_5Y_4EL']])

Scripts.ExportResults.run([antennas['antenna_1_H'],])

plt.close('all')