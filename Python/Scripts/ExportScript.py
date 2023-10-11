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

import Scripts.AntennasLoaders.LoadHFSSYagis
antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(Ntheta=91, Nphi=91)

import Scripts.AntennasLoaders.LoadHFSSValidationArrays
antennas.update(Scripts.AntennasLoaders.LoadHFSSValidationArrays.run(Ntheta=91, Nphi=91))

import Scripts.AntennasLoaders.LoadValidationArrays
antennas.update(Scripts.AntennasLoaders.LoadValidationArrays.run(Ntheta=91, Nphi=91))

import Scripts.ExportResults
import Scripts.ExportCompare

export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/Fields1Y4EL'
Scripts.ExportResults.run([
    antennas['array_validation_1Y4EL'],
    antennas['HFSS_1Y4EL'],
    ], export_directory)

export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/Fields2Y4EL'
Scripts.ExportResults.run([
    antennas['array_validation_2Y4EL'],
    antennas['HFSS_2Y4EL'],
    ], export_directory)
export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/Fields3Y4EL'
Scripts.ExportResults.run([
    antennas['array_validation_3Y4EL'],
    antennas['HFSS_3Y4EL'],
    ],export_directory)
export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/Fields4Y4EL'
Scripts.ExportResults.run([
    antennas['array_validation_4Y4EL'],
    antennas['HFSS_4Y4EL'],
    ], export_directory)
export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/Fields5Y4EL'
Scripts.ExportResults.run(
    [
    antennas['array_validation_5Y4EL'],
    antennas['HFSS_5Y4EL']
    ], export_directory)

export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/Comparisons'
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

export_directory = '/media/vitinho/DADOS/TCC/Python/ExportedResults/ReferenceSystemComparison'
Scripts.ExportResults.run(
    [
        antennas['array_validation_3Y4EL'],
        antennas['HFSS_3Y4EL'],
    ],
    export_directory,
    fields=['Fphi','Ftheta','Fref','Fcross', 'F', 'Fref-Fcross'],
    title='ReferenceSystemComparison')

# import Result
# import ResultFigure
# results_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Python\\ExportedResults'

# figure = ResultFigure.ResultFigure()
# antenna = antennas['HFSS_2Y4EL']
# field = 'Ftheta-Fphi'
# plot = '2d Polar Patch'
# Result.Result(tab=figure,
#               title='',
#               antenna=antenna,
#               field=field,
#               plot=plot,
#               in_dB=True)
# figure.draw()
# fname = os.path.join(results_dir, antenna.name + ' RefSysCompare-Ftheta-Fphi' + '.png')
# figure.figure.savefig(fname)

# figure = ResultFigure.ResultFigure()
# antenna = antennas['HFSS_2Y4EL']
# field = 'Fref-Fcross'
# plot = '2d Polar Patch'
# Result.Result(tab=figure,
#               title='',
#               antenna=antenna,
#               field=field,
#               plot=plot,
#               in_dB=True)
# figure.draw()
# fname = os.path.join(results_dir, antenna.name + ' RefSysCompare-Fref-Fcross' + '.png')
# figure.figure.savefig(fname)

# plt.close('all')