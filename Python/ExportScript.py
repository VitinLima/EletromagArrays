# -*- coding: utf-8 -*-
"""
Created on Sat May 13 18:37:32 2023

@author: 160047412
"""

import sys
import os
import header

import matplotlib.pyplot as plt
plt.close('all')

import LoadHFSSYagis
antennas = LoadHFSSYagis.run(
    Ntheta=91, Nphi=91)

import LoadHFSSValidationArrays
antennas.update(LoadHFSSValidationArrays.run(
    Ntheta=91, Nphi=91))

import LoadValidationArrays
antennas.update(LoadValidationArrays.run(
    Ntheta=91, Nphi=91))

import ExportResults
import ExportCompare
import ExportTable

export_directory = os.path.join(header.validation_results_dir,
                                'Fields1Y4EL')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
ExportResults.run([
    antennas['array_validation_1Y4EL'],
    antennas['HFSS_1Y4EL'],
    ], export_directory)
ExportTable.export_table(
    export_directory,
    arrays=[
        antennas['array_validation_1Y4EL']
        ],
    captions = [
        "Arranjo de validação do código com 1 antena"
        ])
export_directory = os.path.join(header.validation_results_dir,
                                'Fields2Y4EL')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
ExportResults.run([
    antennas['array_validation_2Y4EL'],
    antennas['HFSS_2Y4EL'],
    ], export_directory)
ExportTable.export_table(
    export_directory,
    arrays=[
        antennas['array_validation_2Y4EL']
        ],
    captions = [
        "Arranjo de validação do código com 2 antenas"
        ])

export_directory = os.path.join(header.validation_results_dir,
                                'Fields3Y4EL')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
ExportResults.run([
    antennas['array_validation_3Y4EL'],
    antennas['HFSS_3Y4EL'],
    ],export_directory)
ExportTable.export_table(
    export_directory,
    arrays=[
        antennas['array_validation_3Y4EL']
        ],
    captions = [
        "Arranjo de validação do código com 3 antenas"
        ])

export_directory = os.path.join(header.validation_results_dir,
                                'Fields4Y4EL')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
ExportResults.run([
    antennas['array_validation_4Y4EL'],
    antennas['HFSS_4Y4EL'],
    ], export_directory)
ExportTable.export_table(
    export_directory,
    arrays=[
        antennas['array_validation_4Y4EL']
        ],
    captions = [
        "Arranjo de validação do código com 4 antenas"
        ])

export_directory = os.path.join(header.validation_results_dir,
                                'Fields5Y4EL')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
ExportResults.run(
    [
    antennas['array_validation_5Y4EL'],
    antennas['HFSS_5Y4EL']
    ], export_directory)
ExportTable.export_table(
    export_directory,
    arrays=[
        antennas['array_validation_5Y4EL']
        ],
    captions = [
        "Arranjo de validação do código com 5 antenas"
        ])

export_directory = os.path.join(header.results_dir,
                                'Comparisons')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
ExportCompare.run([
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

export_directory = os.path.join(header.results_dir,
                                'ReferenceSystemComparison')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)
ExportResults.run(
    [
        antennas['array_validation_3Y4EL'],
        antennas['HFSS_3Y4EL'],
    ],
    export_directory,
    fields=['Fphi','Ftheta','Fref','Fcross', 'F', 'Fref-Fcross'],
    title='ReferenceSystemComparison')