# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 01:30:47 2023

@author: Vítor Lima Aguirra
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
# import os
# import re
# import sys
# import subprocess
import numpy as np

import ProjectTreeview
# import scope_fields

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('EletromagArrays')
        self.name = 'New project'
        
        self.init_variables()
        self.init_layout()
        
        self.constants = dict()
        self.evaluate_constants()
        
        self.antennas = []
        self.analyses = []
        self.optims = []
        self.result_tabs = []
        
        color = '#303030'
        self.configure(background=color)
        style = ttk.Style(self)
        # set ttk theme to "clam" which support the fieldbackground option
        style.theme_use("clam")
        style.configure("Treeview", background=color, 
                        fieldbackground=color, foreground="white")
    
    def init_variables(self):
        self.frequency = tk.DoubleVar(value=433e6)
    
    def evaluate_constants(self):
        self.constants['c'] = 299792458 # m/s
        self.constants['f'] = self.frequency.get() # Hz
        self.constants['eta'] = 120*np.pi
        self.constants['lam'] = self.constants['c']/self.constants['f'] # m
        self.constants['w'] = 2*np.pi*self.constants['f'] # rad/s
        self.constants['k'] = 2*np.pi/self.constants['lam'] # rad/m
    
    def mark_update(self, event):
        for l in self.constants_listeners:
            l.notify(self)
    
    def init_layout(self):
        # self.menu_bar = tk.Menu(master=self)
        # self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        # self.file_menu.add_command(label='New', command=self.new_file)
        # self.file_menu.add_command(label="Open", command=self.open_file)
        # self.file_menu.add_command(label="Save", command=self.save_file)
        # self.file_menu.add_command(label="Save as...", command=self.save_file_as)
        # self.file_menu.add_command(label="Close", command=self.close_file)
        
        # self.file_menu.add_separator()
        
        # self.file_menu.add_command(label="Constants", command=self.edit_constants)
        
        # self.file_menu.add_separator()
        
        # self.file_menu.add_command(label="Exit", command=self.destroy)
        # self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        # self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        # self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        # self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)
        # self.menu_bar.add_cascade(label='Help', menu=self.help_menu)
        # self.config(menu=self.menu_bar)
        
        self.treeview = ProjectTreeview.ProjectTreeview(self, master=self)
        self.treeview.pack(side='left', fill='both')
        
        self.tabs = ttk.Notebook(master=self)
        self.tabs.pack(side='top', fill='both')
    
    def add_antenna(self, antenna):
        self.antennas.append(antenna)
        self.treeview.add_antenna(antenna)
    
    def add_analysis(self, analysis):
        self.analyses.append(analysis)
        self.treeview.add_analysis(analysis)
    
    def add_optim(self, optim):
        self.optims.append(optim)
        self.treeview.add_optim(optim)
    
    def add_tab(self, tab):
        self.result_tabs.append(tab)
        self.treeview.add_tab(tab)
        self.tabs.add(tab,text=tab.name)
        for result in tab.results:
            self.add_result(tab, result)
    
    def add_result(self, tab, result):
        self.treeview.add_result(tab, result)
    
    def remove_antenna(self, antenna):
        self.antennas.remove(antenna)
        self.treeview.remove_antenna(antenna)
    
    def remove_analysis(self, analysis):
        self.analyses.remove(analysis)
        self.treeview.remove_analysis(analysis)
    
    def remove_optim(self, optim):
        self.optims.remove(optim)
        self.treeview.remove_optim(optim)
    
    def remove_tab(self, tab):
        self.tabs.remove(tab)
        self.treeview.remove_tab(tab)
    
    def remove_result(self, tab, result):
        tab.results.remove(result)
        self.treeview.remove_result(tab, result)
    
    def new_file(self):
        print("new file")
    
    def open_file(self):
        print("open file")
    
    def save_file(self):
        print("save file")
    
    def save_file_as(self):
        print("save file as")
    
    def close_file(self):
        print("close file")
    
    def edit_constants(self):
        root = tk.Toplevel()
        fr = ttk.LabelFrame(master=root,text='Speed of light')
        fr.pack(side='top',fill='both')
        tk.Label(master=fr,text='299792458m/s').pack(side='top')
        fr = ttk.LabelFrame(master=root,text='Frequency')
        fr.pack(side='top',fill='both')
        ttk.Entry(master=fr,textvariable=self.frequency).pack(side='top')
        fr = ttk.LabelFrame(master=root,text='Eta')
        fr.pack(side='top',fill='both')
        tk.Label(master=fr,text='%.2f' % self.constants['eta']).pack(side='top')
        fr = ttk.LabelFrame(master=root,text='Lambda')
        fr.pack(side='top',fill='both')
        tk.Label(master=fr,text='%.2f' % self.constants['lam']).pack(side='top')
        fr = ttk.LabelFrame(master=root,text='w')
        fr.pack(side='top',fill='both')
        tk.Label(master=fr,text='%.2f' % self.constants['w']).pack(side='top')
        fr = ttk.LabelFrame(master=root,text='k')
        fr.pack(side='top',fill='both')
        tk.Label(master=fr,text='%.2f' % self.constants['k']).pack(side='top')
        fr = tk.Frame(master=root)
        fr.pack(side='top',fill='both')
        ttk.Button(master=fr,text='Close',command=root.destroy).pack(side='top')
        root.mainloop()
        self.evaluate_constants()
        self.mark_update('constants update')
    
    def mainloop(self):
        self.after(100,self.updater_thread)
        tk.Tk.mainloop(self)
    
    def updater_thread(self):
        for antenna in [antenna for antenna in self.antennas if str(type(antenna))=="<class: 'Antenna.Antenna'>"]:
            if not antenna.ok:
                antenna.evaluate()
        
        for array in [antenna for antenna in self.antennas if str(type(antenna))=="<class: 'Array.Array'>"]:
            if not array.ok:
                array.evaluate()
        
        for tab in self.result_tabs:
            if not tab.ok:
                tab.update()
        
        self.after(2000,self.updater_thread)

if __name__=="__main__":
    import os
    import pickle
    
    import Antenna
    import Array
    import Analysis
    # import Optimization
    import ResultFrame
    import Result
    import LoadDefaultAntennas
    
    theta=np.linspace(0, 90, 31)
    phi=np.linspace(-180, 180, 91)
    antenna_1_H,antenna_2_H,antenna_3_H,antenna_4_H,antenna_1_V,antenna_2_V,antenna_3_V,antenna_4_V = LoadDefaultAntennas.load_default_antennas(elevation=-45)

    # Create the application
    app = App()
    try:
        antennas_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
        app.add_antenna(antenna_1_H)
        app.add_antenna(antenna_1_V)
        app.add_antenna(antenna_2_H)
        app.add_antenna(antenna_2_V)
        app.add_antenna(antenna_3_H)
        app.add_antenna(antenna_3_V)
        app.add_antenna(antenna_4_H)
        app.add_antenna(antenna_4_V)
        
        F = Analysis.Analysis(name='F',expression='F')
        Ftheta = Analysis.Analysis(name='Ftheta',expression='Ftheta',color_expression='')
        Fphi = Analysis.Analysis(name='Fphi',expression='Fphi',color_expression='')
        Frhcp = Analysis.Analysis(name='Frhcp',expression='Frhcp',color_expression='')
        Flhcp = Analysis.Analysis(name='Flhcp',expression='Flhcp',color_expression='')
        
        app.add_analysis(F)
        app.add_analysis(Ftheta)
        app.add_analysis(Fphi)
        app.add_analysis(Frhcp)
        app.add_analysis(Flhcp)
        
        array_H = Array.Array(name='H',
                              theta=theta,
                              phi=phi,
                              antennas=[antenna_3_H.copy() for i in range(4)])
        array_H.antennas[0].set_current(current_mag=-1)
        array_H.antennas[0].set_orientation(azimuth=180)
        array_H.antennas[1].set_current(current_mag=-1)
        array_H.antennas[1].set_orientation(azimuth=180)
        array_H.evaluate()
        
        tab = ResultFrame.ResultFrame(master=app.tabs,name='H')
        result = Result.Result(tab=tab,
                               name='F',
                               antenna=array_H,analysis=F,
                               plot='3d Polar Surface')
        result = Result.Result(tab=tab,
                               name='Ftheta',
                               antenna=array_H,analysis=Ftheta,
                               plot='2d Polar Patch')
        result = Result.Result(tab=tab,
                               name='Fphi',
                               antenna=array_H,analysis=Fphi,
                               plot='2d Polar Patch')
        
        app.add_antenna(array_H)
        app.add_tab(tab)
        
        # array_V = Array.Array(name='V',
        #                       theta=theta,
        #                       phi=phi,
        #                       antennas=[antenna_3_V.copy() for i in range(4)])
        # array_V.antennas[0].set_current(current_mag=-1)
        # array_V.antennas[0].set_orientation(azimuth=180)
        # array_V.antennas[1].set_current(current_mag=-1)
        # array_V.antennas[1].set_orientation(azimuth=180)
        # array_V.evaluate()
        
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='V')
        # result = Result.Result(tab=tab,
        #                        name='F',
        #                        antenna=array_V,analysis=F,
        #                        plot='3d Polar Surface')
        # result = Result.Result(tab=tab,
        #                        name='Ftheta',
        #                        antenna=array_V,analysis=Ftheta,
        #                        plot='2d Polar Patch')
        # result = Result.Result(tab=tab,
        #                        name='Fphi',
        #                        antenna=array_V,analysis=Fphi,
        #                        plot='2d Polar Patch')
        
        # app.add_antenna(array_V)
        # app.add_tab(tab)
        
        # array_RHCP = Array.Array(name='RHCP',
        #                       theta=theta,
        #                       phi=phi,
        #                       antennas=[antenna_3_V.copy(),
        #                                 antenna_3_H.copy(),
        #                                 antenna_3_V.copy(),
        #                                 antenna_3_H.copy(),])
        # array_RHCP.antennas[0].set_current(current_mag=-1)
        # array_RHCP.antennas[0].set_orientation(azimuth=180)
        # array_RHCP.antennas[1].set_current(current_mag=-1)
        # array_RHCP.antennas[1].set_orientation(azimuth=180)
        # array_RHCP.evaluate()
        
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='RHCP')
        # result = Result.Result(tab=tab,
        #                        name='F',
        #                        antenna=array_RHCP,analysis=F,
        #                        plot='3d Polar Surface')
        # result = Result.Result(tab=tab,
        #                        name='Ftheta',
        #                        antenna=array_RHCP,analysis=Ftheta,
        #                        plot='2d Polar Patch')
        # result = Result.Result(tab=tab,
        #                        name='Fphi',
        #                        antenna=array_RHCP,analysis=Fphi,
        #                        plot='2d Polar Patch')
        
        # app.add_antenna(array_RHCP)
        # app.add_tab(tab)
        
        # Main application loop
        app.mainloop()
    except Exception as e:
        # If some error occur, destroy the application to close the window,
        # then show the error
        app.destroy()
        raise e