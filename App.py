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
    
    # Create the application
    app = App()
    try:
        import LoadDefaultAntennas
        antennas = LoadDefaultAntennas.load_default_antennas(Ntheta=91, Nphi=91)
        for antenna in antennas.values():
            app.add_antenna(antenna)
        # import LoadDefaultAnalyses
        # analyses = LoadDefaultAnalyses.load_default_analyses()
        # for analysis in analyses.values():
        #     app.add_analysis(analysis)
        
        import ResultFrame
        import LoadDefaultGraphs
        import LoadCompareAntennas
        
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='H')
        # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=antennas['array_H'])
        # app.add_tab(tab)
        
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='V')
        # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=antennas['array_V'])
        # app.add_tab(tab)
        
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='RHCP')
        # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=antennas['array_RHCP'])
        # app.add_tab(tab)
        
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='Validation 1Y-4El')
        # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=antennas['array_validation_1Y_4El'])
        # app.add_tab(tab)
        
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='Validation 2Y-4El')
        # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=antennas['array_validation_2Y_4El'])
        # app.add_tab(tab)
        
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='Validation 5Y-4El')
        # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=antennas['array_validation_5Y_4El'])
        # app.add_tab(tab)
        
        import os
        import Antenna
        antenna_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
        
        # antenna_path = os.path.join(antenna_dir, '1Y-4EL.csv')
        # HFSS_1Y_4EL = Antenna.Antenna(name='HFSS 1Y-4EL',
        #                     theta=np.linspace(0, 90, 91),
        #                     phi=np.linspace(-180, 180, 91))
        # HFSS_1Y_4EL.set_evaluation_method('load file')
        # HFSS_1Y_4EL.evaluation_arguments['file path'] = antenna_path
        # HFSS_1Y_4EL.evaluation_arguments['load mesh from file'] = False
        # HFSS_1Y_4EL.set_orientation(elevation=0, azimuth=0, roll=0)
        # HFSS_1Y_4EL.evaluate()
        # app.add_antenna(HFSS_1Y_4EL)
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='1Y-4El',iy=2)
        # # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=HFSS_1Y_4EL)
        # LoadCompareAntennas.load_compare_graphs(tab=tab,
        #                                         antennas=[HFSS_1Y_4EL,antennas['array_validation_1Y_4El']],
        #                                         titles=['HFSS', 'Validation'])
        # app.add_tab(tab)
        
        # antenna_path = os.path.join(antenna_dir, '2Y-4EL.csv')
        # HFSS_2Y_4EL = Antenna.Antenna(name='HFSS 2Y-4EL',
        #                     theta=np.linspace(0, 90, 91),
        #                     phi=np.linspace(-180, 180, 91))
        # HFSS_2Y_4EL.set_evaluation_method('load file')
        # HFSS_2Y_4EL.evaluation_arguments['file path'] = antenna_path
        # HFSS_2Y_4EL.evaluation_arguments['load mesh from file'] = False
        # HFSS_2Y_4EL.set_orientation(elevation=0, azimuth=0, roll=0)
        # HFSS_2Y_4EL.evaluate()
        # app.add_antenna(HFSS_2Y_4EL)
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='2Y-4El',iy=2)
        # # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=HFSS_2Y_4EL)
        # LoadCompareAntennas.load_compare_graphs(tab=tab,
        #                                         antennas=[HFSS_2Y_4EL,antennas['array_validation_2Y_4El']],
        #                                         titles=['HFSS', 'Validation'])
        # app.add_tab(tab)
        
        # antenna_path = os.path.join(antenna_dir, '3Y-4EL.csv')
        # HFSS_3Y_4EL = Antenna.Antenna(name='HFSS 3Y-4EL',
        #                     theta=np.linspace(0, 90, 91),
        #                     phi=np.linspace(-180, 180, 91))
        # HFSS_3Y_4EL.set_evaluation_method('load file')
        # HFSS_3Y_4EL.evaluation_arguments['file path'] = antenna_path
        # HFSS_3Y_4EL.evaluation_arguments['load mesh from file'] = False
        # HFSS_3Y_4EL.set_orientation(elevation=0, azimuth=0, roll=0)
        # HFSS_3Y_4EL.evaluate()
        # app.add_antenna(HFSS_3Y_4EL)
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='3Y-4El',iy=2)
        # # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=HFSS_5Y_4EL)
        # LoadCompareAntennas.load_compare_graphs(tab=tab,
        #                                         antennas=[HFSS_3Y_4EL,antennas['array_validation_3Y_4El']],
        #                                         titles=['HFSS', 'Validation'])
        # app.add_tab(tab)
        
        # antenna_path = os.path.join(antenna_dir, '4Y-4EL.csv')
        # HFSS_4Y_4EL = Antenna.Antenna(name='HFSS 4Y-4EL',
        #                     theta=np.linspace(0, 90, 91),
        #                     phi=np.linspace(-180, 180, 91))
        # HFSS_4Y_4EL.set_evaluation_method('load file')
        # HFSS_4Y_4EL.evaluation_arguments['file path'] = antenna_path
        # HFSS_4Y_4EL.evaluation_arguments['load mesh from file'] = False
        # HFSS_4Y_4EL.set_orientation(elevation=0, azimuth=0, roll=0)
        # HFSS_4Y_4EL.evaluate()
        # app.add_antenna(HFSS_4Y_4EL)
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='4Y-4El',iy=2)
        # # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=HFSS_5Y_4EL)
        # LoadCompareAntennas.load_compare_graphs(tab=tab,
        #                                         antennas=[HFSS_4Y_4EL,antennas['array_validation_4Y_4El']],
        #                                         titles=['HFSS', 'Validation'])
        # app.add_tab(tab)
        
        # antenna_path = os.path.join(antenna_dir, '5Y-4EL.csv')
        # HFSS_5Y_4EL = Antenna.Antenna(name='HFSS 5Y-4EL',
        #                     theta=np.linspace(0, 90, 91),
        #                     phi=np.linspace(-180, 180, 91))
        # HFSS_5Y_4EL.set_evaluation_method('load file')
        # HFSS_5Y_4EL.evaluation_arguments['file path'] = antenna_path
        # HFSS_5Y_4EL.evaluation_arguments['load mesh from file'] = False
        # HFSS_5Y_4EL.set_orientation(elevation=0, azimuth=0, roll=0)
        # HFSS_5Y_4EL.evaluate()
        # app.add_antenna(HFSS_5Y_4EL)
        # tab = ResultFrame.ResultFrame(master=app.tabs,name='5Y-4El',iy=2)
        # # LoadDefaultGraphs.load_default_graphs(tab=tab,antenna=HFSS_5Y_4EL)
        # LoadCompareAntennas.load_compare_graphs(tab=tab,
        #                                         antennas=[HFSS_5Y_4EL,antennas['array_validation_5Y_4El']],
        #                                         titles=['HFSS', 'Validation'])
        # app.add_tab(tab)
        
        # Main application loop
        app.mainloop()
    except Exception as e:
        # If some error occur, destroy the application to close the window,
        # then show the error
        app.destroy()
        raise e