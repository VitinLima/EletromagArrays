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
import Scripts.ExportCompare

Scripts.ExportResults.run([
                            antennas['array_validation_1Y_4El'],
                            antennas['array_validation_2Y_4El'],
                            antennas['array_validation_3Y_4El'],
                            antennas['array_validation_4Y_4El'],
                            antennas['array_validation_5Y_4El'],
                            antennas['HFSS_1Y_4EL'],
                            antennas['HFSS_2Y_4EL'],
                            antennas['HFSS_3Y_4EL'],
                            antennas['HFSS_4Y_4EL'],
                            antennas['HFSS_5Y_4EL']
                            ])

Scripts.ExportCompare.run([
                            (antennas['array_validation_1Y_4El'],
                            antennas['HFSS_1Y_4EL']),
                            (antennas['array_validation_2Y_4El'],
                            antennas['HFSS_2Y_4EL']),
                            (antennas['array_validation_3Y_4El'],
                            antennas['HFSS_3Y_4EL']),
                            (antennas['array_validation_4Y_4El'],
                            antennas['HFSS_4Y_4EL']),
                            (antennas['array_validation_5Y_4El'],
                            antennas['HFSS_5Y_4EL'])
                            ])

import Result
import ResultFigure
results_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Python\\ExportedResults'

figure = ResultFigure.ResultFigure()
antenna = antennas['HFSS_2Y_4EL']
field = 'Ftheta-Fphi'
plot = '2d Polar Patch'
Result.Result(tab=figure,
              title='',
              antenna=antenna,
              field=field,
              plot=plot,
              in_dB=True)
figure.draw()
fname = os.path.join(results_dir, 'RefSysCompare-Ftheta-Fphi' + '.png')
figure.figure.savefig(fname)

figure = ResultFigure.ResultFigure()
antenna = antennas['HFSS_2Y_4EL']
field = 'Fref-Fcross'
plot = '2d Polar Patch'
Result.Result(tab=figure,
              title='',
              antenna=antenna,
              field=field,
              plot=plot,
              in_dB=True)
figure.draw()
fname = os.path.join(results_dir, 'RefSysCompare-Fref-Fcross' + '.png')
figure.figure.savefig(fname)

plt.close('all')