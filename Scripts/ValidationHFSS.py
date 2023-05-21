# -*- coding: utf-8 -*-
"""
Created on Sat May 13 14:49:56 2023

@author: 160047412
"""

import Scripts.LoadDefaultGraphs
import Scripts.LoadCompareAntennas

def run(app, antennas):
    # Scripts.LoadDefaultGraphs.load_default_graphs(app=app,name='H',antenna=antennas['array_H'])
    # Scripts.LoadDefaultGraphs.load_default_graphs(app=app,name='V',antenna=antennas['array_V'])
    # Scripts.LoadDefaultGraphs.load_default_graphs(app=app,name='RHCP',antenna=antennas['array_RHCP'])
    # Scripts.LoadDefaultGraphs.load_default_graphs(app=app,name='Validation 1Y-4El',antenna=antennas['array_validation_1Y_4El'])
    Scripts.LoadDefaultGraphs.load_default_graphs(app=app,name='Validation 2Y-4El',antenna=antennas['array_validation_2Y_4El'],fields=['Fref', 'Fcross'])
    Scripts.LoadDefaultGraphs.load_default_graphs(app=app,name='Validation 3Y-4El',antenna=antennas['array_validation_3Y_4El'],fields=['Fref', 'Fcross'])
    # Scripts.LoadDefaultGraphs.load_default_graphs(app=app,name='Validation 4Y-4El',antenna=antennas['array_validation_4Y_4El'])
    # Scripts.LoadDefaultGraphs.load_default_graphs(app=app,name='Validation 5Y-4El',antenna=antennas['array_validation_5Y_4El'])
    
    # Scripts.LoadDefaultGraphs.load_default_graphs(app=app,
    #                                               name='HFSS 1Y-4El',
    #                                               antenna=antennas['HFSS_1Y_4EL'])
    Scripts.LoadDefaultGraphs.load_default_graphs(app=app,
                                                  name='HFSS 2Y-4El',
                                                  antenna=antennas['HFSS_2Y_4EL'],
                                                  fields=['Fref', 'Fcross'])
    Scripts.LoadDefaultGraphs.load_default_graphs(app=app,
                                                  name='HFSS 3Y-4El',
                                                  antenna=antennas['HFSS_3Y_4EL'],
                                                  fields=['Fref', 'Fcross'])
    # Scripts.LoadDefaultGraphs.load_default_graphs(app=app,
    #                                               name='HFSS 4Y-4El',
    #                                               antenna=antennas['HFSS_4Y_4EL'])
    # Scripts.LoadDefaultGraphs.load_default_graphs(app=app,
    #                                               name='HFSS 5Y-4El',
    #                                               antenna=antennas['HFSS_5Y_4EL'])
    
    # Scripts.LoadCompareAntennas.load_compare_graphs(app=app,
    #                                                 name='1Y-4El',
    #                                                 antennas=[antennas['HFSS_1Y_4EL'],antennas['array_validation_1Y_4El']],
    #                                                 titles=['HFSS', 'Validation'])
    Scripts.LoadCompareAntennas.load_compare_graphs(app=app,
                                                    name='2Y-4El',
                                                    antennas=[antennas['HFSS_2Y_4EL'],antennas['array_validation_2Y_4El']],
                                                    titles=['HFSS', 'Validation'])
    Scripts.LoadCompareAntennas.load_compare_graphs(app=app,
                                                    name='3Y-4El',
                                                    antennas=[antennas['HFSS_3Y_4EL'],antennas['array_validation_3Y_4El']],
                                                    titles=['HFSS', 'Validation'])
    Scripts.LoadCompareAntennas.load_compare_graphs(app=app,
                                                    name='4Y-4El',
                                                    antennas=[antennas['HFSS_4Y_4EL'],antennas['array_validation_4Y_4El']],
                                                    titles=['HFSS', 'Validation'])
    Scripts.LoadCompareAntennas.load_compare_graphs(app=app,
                                                    name='5Y-4El',
                                                    antennas=[antennas['HFSS_5Y_4EL'],antennas['array_validation_5Y_4El']],
                                                    titles=['HFSS', 'Validation'])