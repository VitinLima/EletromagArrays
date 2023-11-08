# -*- coding: utf-8 -*-
"""
Created on Sat May 13 18:37:32 2023

@author: 160047412
"""

import sys
import os
path = os.path.split(__file__)[0]
path = os.path.split(path)[0]
sys.path.insert(0, path)
path = os.path.split(path)[0]
home_directory = os.path.split(path)[0]
antennas_dir=os.path.join(home_directory, 'Antennas')

import matplotlib.pyplot as plt
plt.close('all')

import Scripts.AntennasLoaders.LoadHFSSYagis
antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(
    Ntheta=91, Nphi=91)

import Scripts.AntennasLoaders.LoadHFSSValidationArrays
antennas.update(Scripts.AntennasLoaders.LoadHFSSValidationArrays.run(
    Ntheta=91, Nphi=91))

import Scripts.AntennasLoaders.LoadValidationArrays
antennas.update(Scripts.AntennasLoaders.LoadValidationArrays.run(
    Ntheta=91, Nphi=91))

import Scripts.ExportResults
import Scripts.ExportCompare
import OptimizationScripts.ExportTable

export_directory = os.path.join(home_directory,
                                'Python',
                                'ExportedResults',
                                'Validation',
                                'Fields1Y4EL')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
Scripts.ExportResults.run([
    antennas['array_validation_1Y4EL'],
    antennas['HFSS_1Y4EL'],
    ], export_directory)
OptimizationScripts.ExportTable.export_table(
    export_directory,
    arrays=[
        antennas['array_validation_1Y4EL']
        ],
    captions = [
        "Arranjo de validação do código com 1 antena"
        ])
export_directory = os.path.join(home_directory,
                                'Python',
                                'ExportedResults',
                                'Validation',
                                'Fields2Y4EL')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
Scripts.ExportResults.run([
    antennas['array_validation_2Y4EL'],
    antennas['HFSS_2Y4EL'],
    ], export_directory)
OptimizationScripts.ExportTable.export_table(
    export_directory,
    arrays=[
        antennas['array_validation_2Y4EL']
        ],
    captions = [
        "Arranjo de validação do código com 2 antenas"
        ])

export_directory = os.path.join(home_directory,
                                'Python',
                                'ExportedResults',
                                'Validation',
                                'Fields3Y4EL')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
Scripts.ExportResults.run([
    antennas['array_validation_3Y4EL'],
    antennas['HFSS_3Y4EL'],
    ],export_directory)
OptimizationScripts.ExportTable.export_table(
    export_directory,
    arrays=[
        antennas['array_validation_3Y4EL']
        ],
    captions = [
        "Arranjo de validação do código com 3 antenas"
        ])

export_directory = os.path.join(home_directory,
                                'Python',
                                'ExportedResults',
                                'Validation',
                                'Fields4Y4EL')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
Scripts.ExportResults.run([
    antennas['array_validation_4Y4EL'],
    antennas['HFSS_4Y4EL'],
    ], export_directory)
OptimizationScripts.ExportTable.export_table(
    export_directory,
    arrays=[
        antennas['array_validation_4Y4EL']
        ],
    captions = [
        "Arranjo de validação do código com 4 antenas"
        ])

export_directory = os.path.join(home_directory,
                                'Python',
                                'ExportedResults',
                                'Validation',
                                'Fields5Y4EL')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
Scripts.ExportResults.run(
    [
    antennas['array_validation_5Y4EL'],
    antennas['HFSS_5Y4EL']
    ], export_directory)
OptimizationScripts.ExportTable.export_table(
    export_directory,
    arrays=[
        antennas['array_validation_5Y4EL']
        ],
    captions = [
        "Arranjo de validação do código com 5 antenas"
        ])

export_directory = os.path.join(home_directory,
                                'Python',
                                'ExportedResults',
                                'Comparisons')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
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
                            ], export_directory)

export_directory = os.path.join(home_directory,
                                'Python',
                                'ExportedResults',
                                'ReferenceSystemComparison')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
Scripts.ExportResults.run(
    [
        antennas['array_validation_3Y4EL'],
        antennas['HFSS_3Y4EL'],
    ],
    export_directory,
    fields=['Fphi','Ftheta','Fref','Fcross', 'F', 'Fref-Fcross'],
    title='ReferenceSystemComparison')