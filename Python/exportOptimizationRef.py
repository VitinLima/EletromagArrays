#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 21:06:42 2023

@author: vitinho
"""

import sys
import os
import header
export_path = os.path.split(header.src_path)[0]

import Result
import ResultFrame
import App
import Scripts.ExportResults
import Array
import numpy as np
import Scripts.AntennasLoaders.LoadHFSSYagis
import matplotlib.pyplot as plt

plt.close('all')

print("Loading antennas")

antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(
    Ntheta=91, Nphi=91)

print("Loading export results directory")

export_directory = os.path.join(
    export_path,
    'ExportedResults',
    'Optimization',
    'LinearOptimization')
if not os.path.exists(export_directory):
    os.mkdir(export_directory)

print("Creating target distribution")


Ntheta = 91
Nphi = 181

theta = np.linspace(0, 180, Ntheta)
phi = np.linspace(-180, 180, Nphi)

target_antenna = Array.Array(
    name='Target Antenna',
    theta=theta.copy(),
    phi=phi.copy(),
    antennas=[
        antennas['hfss_yagi2EL'].copy(
        ),
        antennas['hfss_yagi2EL'].copy(
        ),
        antennas['hfss_yagi2EL'].copy(
        ),
    ])
target_antenna.antennas[0].set_position(
    x=0, y=0, z=0)
target_antenna.antennas[0].set_orientation(
    elevation=-90, azimuth=55)
target_antenna.antennas[1].set_position(
    x=0, y=0.5, z=0)
target_antenna.antennas[1].set_orientation(
    elevation=-90, azimuth=55)
target_antenna.antennas[2].set_position(
    x=0, y=1, z=0)
target_antenna.antennas[2].set_orientation(
    elevation=-90, azimuth=55)
target_antenna.evaluate()

print("Creating working array")

initial_array = Array.Array(
    name='Initial Array',
    theta=theta.copy(),
    phi=phi.copy(),
    antennas=[
        antennas['hfss_yagi2EL'].copy(
        ),
        antennas['hfss_yagi2EL'].copy(
        ),
        antennas['hfss_yagi2EL'].copy(
        ),
    ])
initial_array.antennas[0].set_position(
    x=0, y=0, z=0)
initial_array.antennas[0].set_orientation(
    elevation=-90, azimuth=60)
initial_array.antennas[1].set_position(
    x=0.0, y=0.5, z=0)
initial_array.antennas[1].set_orientation(
    elevation=-90, azimuth=30)
initial_array.antennas[2].set_position(
    x=0.0, y=1.0, z=0)
initial_array.antennas[2].set_orientation(
    elevation=-90, azimuth=60)
initial_array.evaluate()

print("Exporting initial state")


Scripts.ExportResults.run([
    initial_array,
], export_directory)

print("Optimizing")


def cost_function(target, result):
    total_cost = (np.abs(
        np.abs(target.Fcross)-np.abs(result.Fcross))*target.sin_mesh_theta).sum()
    total_cost += (np.abs(np.abs(target.Fref) -
                         np.abs(result.Fref))*target.sin_mesh_theta).sum()
    return total_cost

import Optimization

working_array = initial_array.copy()
optim = Optimization.Optimization(
    target_antenna=target_antenna,
    working_array=working_array,
    x_map = [
        dict(
            antenna=working_array.antennas[0],
            variables = [
                # 'x',
                # 'y',
                'elevation',
                'azimuth',
                # 'roll',
                ],
            ),
        dict(
            antenna=working_array.antennas[1],
            variables = [
                # 'x',
                # 'y',
                'elevation',
                'azimuth',
                # 'roll',
                ],
            ),
        dict(
            antenna=working_array.antennas[2],
            variables = [
                # 'x',
                # 'y',
                'elevation',
                'azimuth',
                # 'roll',
                ],
            ),
        ],
    cost_function=cost_function,
    # method = 'L-BFGS-B',
    )

result = optim.run()
final_array = optim.working_array

print(result)

final_array.name = 'Result Array'

print("Exporting results")

Scripts.ExportResults.run([
    target_antenna,
    final_array,
], export_directory)

import ExportTable

initial_array.name = 'Arranjo inicial - otimização linear'
target_antenna.name = 'Arranjo alvo de polarização linear ' + \
    '- otimização linear'
final_array.name = 'Arranjo final otimizado - otimização linear'

ExportTable.export_table(
    export_directory,
    arrays=[
        initial_array,
        target_antenna,
        final_array
        ],
    captions = [
        "Arranjo inicial",
        "Arranjo alvo",
        "Resultados da otimização de polarização linear " +
            "com custo final de {:.2f}".format(optim.cost)
        ])

if __name__=='__main__':
    
    print("Starting visualization")
    
    
    app = App.App(antennas=[target_antenna, final_array])
    try:
        Ntheta = 91
        Nphi = 181
        field = 'F'
        plot = '2d Polar Patch'
    
        tab = ResultFrame.ResultFrame(
            master=app.tabs,
            name=field,
            columns=2, rows=1)
        Result.Result(tab=tab,
                      title='Result',
                      name='Result',
                      antenna=final_array,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=1, row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        Result.Result(tab=tab,
                      title='Target',
                      name='Target',
                      antenna=target_antenna,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=2, row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        app.add_tab(tab)
    
        field = 'Fref'
        plot = '2d Polar Patch'
    
        tab = ResultFrame.ResultFrame(
            master=app.tabs, name=field, columns=2, rows=1)
        Result.Result(tab=tab,
                      title='Result',
                      name='Result',
                      antenna=final_array,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=1, row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        Result.Result(tab=tab,
                      title='Target',
                      name='Target',
                      antenna=target_antenna,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=2, row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        app.add_tab(tab)
    
        field = 'Fcross'
        plot = '2d Polar Patch'
    
        tab = ResultFrame.ResultFrame(
            master=app.tabs, name=field, columns=2, rows=1)
        Result.Result(tab=tab,
                      title='Result',
                      name='Result',
                      antenna=final_array,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=1, row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        Result.Result(tab=tab,
                      title='Target',
                      name='Target',
                      antenna=target_antenna,
                      field=field,
                      plot=plot,
                      ticks_flag=False,
                      in_dB=True,
                      column=2, row=1,
                      Ntheta=Ntheta,
                      Nphi=Nphi)
        app.add_tab(tab)
    
        # Main application loop
        app.mainloop()
    except Exception as e:
        # If some error occur, destroy the application to close
        # the window, then show the error
        app.destroy()
        raise e
