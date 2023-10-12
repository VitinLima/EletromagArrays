# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:34:00 2023

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
import numpy as np

import matplotlib.pyplot as plt

import ResultFigure
import Result

def run(antennas, export_directory):
    fields = [
        'F',
        # 'Fref',
        # 'Fcross',
        # 'Ftheta',
        # 'Fphi'
        ]
    
    if not os.path.exists(export_directory):
        os.mkdir(export_directory)
    for antenna_pair in antennas:
        for field in fields:
            figure = ResultFigure.ResultFigure()
            plot = '2d Polar Patch'
            result = Result.Result(tab=figure,
                                   title='',
                                   field=field,
                                   plot='custom',
                                   ticks_flag=False,
                                   in_dB=False)
            
            def draw_comparison(result, tab):
                result.axes = tab.request_axes(
                    requester=result,
                    projection='polar',
                    position=result.position)
                
                interp_theta_deg = np.linspace(0,90,81)
                interp_phi_deg = np.linspace(-180,180,91)
                
                interp_mesh_phi_deg,interp_mesh_theta_deg = \
                    np.meshgrid(interp_phi_deg,interp_theta_deg)
                
                field_0,color_0 = result.get_field(antenna_pair[0])
                field_1,color_1 = result.get_field(antenna_pair[1])
                
                color_0 = antenna_pair[0].interpolate_at(
                    interp_mesh_theta_deg,
                    interp_mesh_phi_deg, color_0)
                color_1 = antenna_pair[1].interpolate_at(
                    interp_mesh_theta_deg,
                    interp_mesh_phi_deg, color_1)
                
                color = 20*np.log10(np.abs(color_0) - np.abs(color_1))
                
                color[color<result.dynamic_scaling_dB] = \
                    result.dynamic_scaling_dB
                color[np.isnan(color)] = result.dynamic_scaling_dB
                
                
                if result.color=='Color by magnitude':
                    cmap = 'jet'
                elif result.color=='Color by phase':
                    cmap = 'twilight'
                
                color_max = color.max()
                color_min = color.min()
                if color_max!=color_min:
                    C = (color-color_min)/(color_max-color_min)
                    rgb = plt.colormaps[cmap](C)
                else:
                    rgb = list(color.shape)
                    rgb.append(4)
                    rgb = np.zeros(tuple(rgb))
                    rgb[:,:,3] = 1
                    rgb[:,:,2] = 1
                
                result.graphical_objects = result.axes.pcolormesh(
                    np.radians(interp_mesh_phi_deg),
                    np.sin(np.radians(interp_mesh_theta_deg)),
                    color,
                    shading='gouraud',
                    cmap=cmap)
                plt.colorbar(result.graphical_objects,ax=result.axes)
                result.axes.set_title(result.title)
                result.axes.xaxis.set_ticklabels([])
                result.axes.yaxis.set_ticklabels([])
                # result.axes.set_xticks(
                #     [0,
                #      np.pi/4,
                #      np.pi/2,
                #      3*np.pi/4,
                #      np.pi,
                #      -3*np.pi/4,
                #      -np.pi/2,
                #      -np.pi/4])
            
            result.custom_draw = draw_comparison
            figure.draw()
            fname = os.path.join(
                export_directory,
                antenna_pair[0].name +
                    ' and ' + \
                    antenna_pair[1].name +
                    ' ' + field +
                    ' ' + plot +
                    ' compare.png')
            figure.figure.savefig(fname)
            plt.close('all')

if __name__=='__main__':
    import Scripts.AntennasLoaders.LoadHFSSYagis
    antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(
        Ntheta=91, Nphi=91)

    import Scripts.AntennasLoaders.LoadHFSSValidationArrays
    antennas.update(Scripts.AntennasLoaders.LoadHFSSValidationArrays.run(
        Ntheta=91, Nphi=91))

    import Scripts.AntennasLoaders.LoadValidationArrays
    antennas.update(Scripts.AntennasLoaders.LoadValidationArrays.run(
        Ntheta=91, Nphi=91))
    
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