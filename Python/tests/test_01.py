#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 16:45:31 2023

@author: vitinho
"""

import sys
import os
path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, path)

import Scripts.AntennasLoaders.LoadHFSSYagis

antennas = Scripts.AntennasLoaders.LoadHFSSYagis.run(Ntheta=91, Nphi=91, elevation=-90)
new_antenna = antennas['hfss_yagi3EL'].copy()
new_antenna.name = 'copied antenna'

import App

app = App.App()
try:
    app.add_antenna(antennas['hfss_yagi3EL'])
    app.add_antenna(new_antenna)
    
    # Main application loop
    app.mainloop()
except Exception as e:
    # If some error occur, destroy the application to close the window,
    # then show the error
    app.destroy()
    raise e