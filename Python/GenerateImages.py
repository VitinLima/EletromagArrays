#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 17:07:12 2023

@author: vitinho
"""

import sys
import os
import header

python_path = header.python_path
results_dir = os.path.join(header.results_dir, 'Validation')
home_dir = header.home_dir
antennas_dir = header.antennas_dir

import matplotlib.pyplot as plt
plt.close('all')

import Scripts.AntennasLoaders.LoadHFSSYagis
antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(Ntheta=91, Nphi=91,)
                                                     # antennas_dir=antennas_dir)

import Scripts.AntennasLoaders.LoadHFSSValidationArrays
antennas.update(Scripts.AntennasLoaders.LoadHFSSValidationArrays.run(
    Ntheta=91, Nphi=91,))# antennas_dir=antennas_dir))

import Scripts.AntennasLoaders.LoadValidationArrays
antennas.update(Scripts.AntennasLoaders.LoadValidationArrays.run(
    Ntheta=91, Nphi=91))

import Scripts.ExportResults
import Scripts.ExportCompare

if not os.path.exists(results_dir):
    os.mkdir(results_dir)
cur_export_dir = os.path.join(results_dir, 'Fields1Y4EL')
if not os.path.exists(cur_export_dir):
    os.mkdir(cur_export_dir)
Scripts.ExportResults.run([
    antennas['array_validation_1Y4EL'],
    antennas['HFSS_1Y4EL'],
    ], cur_export_dir)
cur_export_dir = os.path.join(results_dir, 'Fields2Y4EL')
Scripts.ExportResults.run([
    antennas['array_validation_2Y4EL'],
    antennas['HFSS_2Y4EL'],
    ], cur_export_dir)
cur_export_dir = os.path.join(results_dir, 'Fields3Y4EL')
Scripts.ExportResults.run([
    antennas['array_validation_3Y4EL'],
    antennas['HFSS_3Y4EL'],
    ],cur_export_dir)
cur_export_dir = os.path.join(results_dir, 'Fields4Y4EL')
Scripts.ExportResults.run([
    antennas['array_validation_4Y4EL'],
    antennas['HFSS_4Y4EL'],
    ], cur_export_dir)
cur_export_dir = os.path.join(results_dir, 'Fields5Y4EL')
Scripts.ExportResults.run(
    [
    antennas['array_validation_5Y4EL'],
    antennas['HFSS_5Y4EL']
    ], cur_export_dir)

cur_export_dir = os.path.join(results_dir, 'Comparisons')
Scripts.ExportCompare.run([
                            (antennas['array_validation_1Y4EL'],
                            antennas['HFSS_1Y4EL']),
                            (antennas['array_validation_2Y4EL'],
                            antennas['HFSS_2Y4EL']),
                            (antennas['array_validation_3Y4EL'],
                            antennas['HFSS_3Y4EL']),
                            (antennas['array_validation_4Y4EL'],
                            antennas['HFSS_4Y4EL']),
                            (antennas['array_validation_5Y4EL'],
                            antennas['HFSS_5Y4EL'])
                            ], cur_export_dir)

cur_export_dir = os.path.join(results_dir, 'ReferenceSystemComparison')
Scripts.ExportResults.run(
    [
        antennas['array_validation_3Y4EL'],
        antennas['HFSS_3Y4EL'],
    ],
    cur_export_dir,
    fields=['Fphi','Ftheta','Fref','Fcross', 'F', 'Fref-Fcross'],
    title='ReferenceSystemComparison')

import Result
import ResultFigure

figure = ResultFigure.ResultFigure()
antenna = antennas['HFSS_3Y4EL']
field = 'Ftheta-Fphi'
plot = '2d Polar Patch'
Result.Result(tab=figure,
              title='',
              antenna=antenna,
              field=field,
              plot=plot,
              in_dB=True)
figure.draw()
fname = os.path.join(results_dir, antenna.name +
                     ' RefSysCompare-Ftheta-Fphi' + '.png')
figure.figure.savefig(fname)

figure = ResultFigure.ResultFigure()
antenna = antennas['HFSS_3Y4EL']
field = 'Fref-Fcross'
plot = '2d Polar Patch'
Result.Result(tab=figure,
              title='',
              antenna=antenna,
              field=field,
              plot=plot,
              in_dB=True)
figure.draw()
fname = os.path.join(results_dir, antenna.name +
                     ' RefSysCompare-Fref-Fcross' + '.png')
figure.figure.savefig(fname)

plt.close('all')