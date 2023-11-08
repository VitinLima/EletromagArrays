#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 14:27:57 2023

@author: vitinho
"""

import os

def export_table(export_directory, arrays, captions):
    with open(os.path.join(export_directory, "table.tex"), 'w') as f:
        print('Exporting tables in ' + f.name)
        for array, caption in zip(arrays, captions):
            f.write("\\begin{table}[H]\n")
            f.write("    \\centering\n")
            f.write("    \\tiny\n")
            f.write("    \\begin{tabular}{c|c|c|c|c|c|c|c|c}\n")
            f.write("         & \\multicolumn{3}{|c|}{Posição} & " +
                    "\\multicolumn{3}{|c|}{Orientação} & " +
                    "\\multicolumn{2}{|c}{Alimentação} \\\\\n")
            f.write("         \\hline\n")
            f.write("        Antenna & X & Y & Z & Elevation " +
                    "[$\circ$] & Azimuth [$\circ$] & Roll " +
                    "[$\circ$] & Magnitude & Phase [$\circ$] \\\\\n")
            f.write("        \\hline\n")
            for i in range(len(array.antennas)):
                x = array.antennas[i].x
                y = array.antennas[i].y
                z = array.antennas[i].z
                e = array.antennas[i].elevation
                a = array.antennas[i].azimuth
                r = array.antennas[i].roll
                m = array.antennas[i].current_magnitude
                p = array.antennas[i].current_phase
                f.write("        " + array.antennas[i].name +
                        " & {x:.2f}".format(x=x) +
                        " & {y:.2f}".format(y=y) +
                        " & {z:.2f}".format(z=z) +
                        " & {e:.2f}".format(e=e) +
                        " & {a:.2f}".format(a=a) +
                        " & {r:.2f}".format(r=r) +
                        " & {m:.2f}".format(m=m) +
                        " & {p:.2f}".format(p=p) +
                        " \\\\\n")
            f.write("    \\end{tabular}\n")
            f.write("    \\caption{{{caption}}}\n".format(
                caption=caption))
            f.write("    \\label{tab:Arranjo " + array.name + "}\n")
            f.write("\\end{table}\n")

if __name__=="__main__":
    import sys
    path = os.path.split(os.path.split(__file__)[0])[0]
    sys.path.insert(0, path)
    path = os.path.split(path)[0]
    export_directory = os.path.join(
        path, 
        'ExportedResults')
    
    import Array
    import numpy as np
    import Scripts.AntennasLoaders.LoadHFSSYagis

    print("Loading antennas")

    antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(
        Ntheta=91, Nphi=91)
    
    Ntheta = 91
    Nphi = 181

    theta = np.linspace(0, 180, Ntheta)
    phi = np.linspace(-180, 180, Nphi)

    ant = Array.Array(
        name='Target',
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
    ant.antennas[0].set_position(x=0, y=0, z=0)
    ant.antennas[0].set_orientation(
        elevation=-90, azimuth=90)
    ant.antennas[1].set_position(
        x=0, y=0.5, z=0)
    ant.antennas[1].set_orientation(
        elevation=-90, azimuth=0)
    ant.antennas[2].set_position(x=0, y=1, z=0)
    ant.antennas[2].set_orientation(
        elevation=-90, azimuth=120)
    ant.evaluate()
    
    export_table(export_directory=export_directory,
                 arrays=[ant],
                 captions=["Testing"])
    
    import exportOptimizationRef
    import exportOptimizationRefNonConverged
    import exportOptimizationCircular
    import CustomOptimization