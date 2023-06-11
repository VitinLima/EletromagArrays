# -*- coding: utf-8 -*-
"""
Created on Sat May 13 16:32:59 2023

@author: 160047412
"""

import matplotlib.pyplot as plt

import ResultFigure
import Result

import os
# import shutil

def run(antennas,
        export_directory,
        fields = [
            'F',
            'Fref',
            'Fcross',
            'Ftheta',
            'Fphi'
            ],
        title=''):
    
    if not os.path.exists(export_directory):
        os.mkdir(export_directory)
    # results_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Python\\ExportedResults'
    # results_dir = '/media/vitinho/DADOS/TCC/Python/ExportedResults'
    for antenna in antennas:
        for field in fields:
            figure = ResultFigure.ResultFigure()
            plot = '2d Polar Patch'
            Result.Result(tab=figure,
                          title='',
                          antenna=antenna,
                          field=field,
                          plot=plot,
                          ticks_flag=False,
                          in_dB=True)
            figure.draw()
            fname = os.path.join(export_directory, ' '.join([s for s in [antenna.name,field,plot,title] if s != '']) + '.png')
            figure.figure.savefig(fname)
            plt.close('all')