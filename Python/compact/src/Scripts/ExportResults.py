# -*- coding: utf-8 -*-
"""
Created on Sat May 13 16:32:59 2023

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

import ResultFigure
import Result

def run(antennas,
        export_directory,
        fields = [
            'F',
            'Fref',
            'Fcross',
            'Ftheta',
            'Fphi'
            ],
        colors = [
            'Color by magnitude',
            'Color by phase'
            ],
        title='',
        Ntheta=91,
        Nphi=181,):
    
    if not os.path.exists(export_directory):
        os.mkdir(export_directory)
    
    for antenna in antennas:
        for field in fields:
            for color in colors:
                figure = ResultFigure.ResultFigure()
                plot = '2d Polar Patch'
                Result.Result(tab=figure,
                              title='',
                              antenna=antenna,
                              field=field,
                              color=color,
                              plot=plot,
                              ticks_flag=False,
                              in_dB=True,
                              Ntheta=Ntheta,
                              Nphi=Nphi,)
                figure.draw()
                fname = os.path.join(
                    export_directory, ' '.join(
                        [s for s \
                         in [antenna.name,field,color,plot,title] \
                             if s != '']) + '.png')
                figure.figure.savefig(fname)
                plt.close('all')