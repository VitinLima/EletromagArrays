# -*- coding: utf-8 -*-
"""
Created on Sat May 13 14:49:56 2023

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

import Scripts.LoadDefaultGraphs
import Scripts.LoadCompareAntennas

def run(app, antennas):
    
    # Scripts.LoadDefaultGraphs.load_default_graphs(
    #     app=app,
    #     name='H',
    #     antenna=antennas['array_H'])
    # Scripts.LoadDefaultGraphs.load_default_graphs(
    #     app=app,
    #     name='V',
    #     antenna=antennas['array_V'])
    # Scripts.LoadDefaultGraphs.load_default_graphs(
    #     app=app,
    #     name='RHCP',
    #     antenna=antennas['array_RHCP'])
    
    Scripts.LoadDefaultGraphs.load_default_graphs(
        app=app,
        name='Validation 1Y-4EL',
        antenna=antennas['array_validation_1Y4EL'])
    Scripts.LoadDefaultGraphs.load_default_graphs(
        app=app,
        name='Validation 2Y-4EL',
        antenna=antennas['array_validation_2Y4EL'],
        fields=['F', 'Fref', 'Fcross'])
    Scripts.LoadDefaultGraphs.load_default_graphs(
        app=app,
        name='Validation 3Y-4EL',
        antenna=antennas['array_validation_3Y4EL'],
        fields=['F', 'Fref', 'Fcross'])
    Scripts.LoadDefaultGraphs.load_default_graphs(
        app=app,
        name='Validation 4Y-4EL',
        antenna=antennas['array_validation_4Y4EL'])
    Scripts.LoadDefaultGraphs.load_default_graphs(
        app=app,
        name='Validation 5Y-4EL',
        antenna=antennas['array_validation_5Y4EL'])
    
    Scripts.LoadDefaultGraphs.load_default_graphs(
        app=app,
        name='HFSS 1Y-4EL',
        antenna=antennas['HFSS_1Y4EL'])
    Scripts.LoadDefaultGraphs.load_default_graphs(
        app=app,
        name='HFSS 2Y-4EL',
        antenna=antennas['HFSS_2Y4EL'],
        fields=['F', 'Fref', 'Fcross'])
    Scripts.LoadDefaultGraphs.load_default_graphs(
        app=app,
        name='HFSS 3Y-4EL',
        antenna=antennas['HFSS_3Y4EL'],
        fields=['F', 'Fref', 'Fcross'])
    Scripts.LoadDefaultGraphs.load_default_graphs(
        app=app,
        name='HFSS 4Y-4EL',
        antenna=antennas['HFSS_4Y4EL'])
    Scripts.LoadDefaultGraphs.load_default_graphs(
        app=app,
        name='HFSS 5Y-4EL',
        antenna=antennas['HFSS_5Y4EL'])
    
    Scripts.LoadCompareAntennas.load_compare_graphs(
        app=app,
        name='1Y-4EL',
        antennas=[antennas['HFSS_1Y4EL'],
                  antennas['array_validation_1Y4EL']],
        titles=['HFSS', 'Validation'])
    Scripts.LoadCompareAntennas.load_compare_graphs(
        app=app,
        name='2Y-4EL',
        antennas=[antennas['HFSS_2Y4EL'],
                  antennas['array_validation_2Y4EL']],
        titles=['HFSS', 'Validation'])
    Scripts.LoadCompareAntennas.load_compare_graphs(
        app=app,
        name='3Y-4EL',
        antennas=[antennas['HFSS_3Y4EL'],
                  antennas['array_validation_3Y4EL']],
        titles=['HFSS', 'Validation'])
    Scripts.LoadCompareAntennas.load_compare_graphs(
        app=app,
        name='4Y-4EL',
        antennas=[antennas['HFSS_4Y4EL'],
                  antennas['array_validation_4Y4EL']],
        titles=['HFSS', 'Validation'])
    Scripts.LoadCompareAntennas.load_compare_graphs(
        app=app,
        name='5Y-4EL',
        antennas=[antennas['HFSS_5Y4EL'],
                  antennas['array_validation_5Y4EL']],
        titles=['HFSS', 'Validation'])