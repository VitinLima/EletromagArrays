# -*- coding: utf-8 -*-
"""
Created on Sat May 13 16:32:59 2023

@author: 160047412
"""

import matplotlib.pyplot as plt

import ResultFigure
import Result

import os

def run(antennas):
    fields = [
        'F',
        'Fref',
        'Fcross',
        # 'Ftheta',
        # 'Fphi'
        ]
    results_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Python\\ExportedResults'
    for antenna in antennas:
        for field in fields:
            figure = ResultFigure.ResultFigure()
            plot = '2d Polar Patch'
            Result.Result(tab=figure,
                          title='',
                          antenna=antenna,
                          field=field,
                          plot=plot,
                          in_dB=False)
            figure.draw()
            fname = os.path.join(results_dir, antenna.name + ' ' + field + ' ' + plot + '.png')
            figure.figure.savefig(fname)
            plt.close('all')