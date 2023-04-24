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
    
    def add_result_tab(self, result_tab):
        self.result_tabs.append(result_tab)
        self.treeview.add_result_tab(result_tab)
        self.tabs.add(result_tab,text=result_tab.name)
    
    def add_result(self, result_tab, result):
        self.treeview.add_result(result_tab, result)
    
    def remove_antenna(self, antenna):
        self.antennas.remove(antenna)
        self.treeview.remove_antenna(antenna)
    
    def remove_analysis(self, analysis):
        self.analyses.remove(analysis)
        self.treeview.remove_analysis(analysis)
    
    def remove_optim(self, optim):
        self.optims.remove(optim)
        self.treeview.remove_optim(optim)
    
    def remove_result_tab(self, result_tab):
        self.result_tabs.remove(result_tab)
        self.treeview.remove_result_tab(result_tab)
    
    def remove_result(self, result_tab, result):
        result_tab.results.remove(result)
        self.treeview.remove_result(result_tab, result)
    
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
        
        for result_tab in self.result_tabs:
            if not result_tab.ok:
                result_tab.update()
        
        self.after(2000,self.updater_thread)

if __name__=="__main__":
    import os
    import pickle
    
    import Antenna
    import Array
    import Analysis
    # import Optimization
    import ResultFrame

    # Create the application
    app = App()
    try:
        antennas_dir = 'C:\\Users\\160047412\\OneDrive - unb.br\\LoraAEB\\Antennas'
        
        # isotropic = Antenna(app.constants,name='Ideal isotropic antenna')
        # isotropic.set_evaluation_method('isotropic')
        # isotropic.evaluation_arguments['isotropic on'] = 'theta'
        # isotropic.evaluate()
        
        # dipole = Antenna(app.constants,name='Ideal dipole')
        # dipole.evaluate()
        
        antenna_path = os.path.join(antennas_dir, 'antenna-Dipole.csv')
        antenna_1 = Antenna.Antenna(app.constants,name='Dipole antenna')
        antenna_1.set_evaluation_method('load file')
        antenna_1.evaluation_arguments['file path'] = antenna_path
        antenna_1.evaluation_arguments['load mesh from file'] = False
        antenna_1.set_orientation(elevation=0,azimuth=0)
        antenna_1.evaluate()
        
        antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-2Elements.csv')
        antenna_2 = Antenna.Antenna(app.constants,name='Yagi 2 elements')
        antenna_2.set_evaluation_method('load file')
        antenna_2.evaluation_arguments['file path'] = antenna_path
        antenna_2.evaluation_arguments['load mesh from file'] = False
        antenna_2.set_orientation(elevation=-90)
        antenna_2.evaluate()
        
        antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-3Elements.csv')
        antenna_3 = Antenna.Antenna(app.constants,name='Yagi 3 elements')
        antenna_3.set_evaluation_method('load file')
        antenna_3.evaluation_arguments['file path'] = antenna_path
        antenna_3.evaluation_arguments['load mesh from file'] = False
        antenna_3.set_orientation(elevation=-90)
        antenna_3.evaluate()
        
        antenna_path = os.path.join(antennas_dir, 'antenna-Yagi-4Elements.csv')
        antenna_4 = Antenna.Antenna(app.constants,name='Yagi 4 elements')
        antenna_4.set_evaluation_method('load file')
        antenna_4.evaluation_arguments['file path'] = antenna_path
        antenna_4.evaluation_arguments['load mesh from file'] = False
        antenna_4.set_orientation(elevation=0)
        antenna_4.evaluate()
        
        # app.add_antenna(isotropic)
        # app.add_antenna(dipole)
        app.add_antenna(antenna_1)
        app.add_antenna(antenna_2)
        app.add_antenna(antenna_3)
        app.add_antenna(antenna_4)
        
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
        
        theta=np.linspace(0,180,91)
        phi=np.linspace(-180,180,91)
        
        # filedir = 'Optimization Results Theta'
        # filename = os.path.join(filedir,'best array with 1 antenna and cost 355.4455867999418.dat')
        # # filename = os.path.join(filedir,'best array with 2 antenna and cost 167.3758780615933.dat')
        # # filename = os.path.join(filedir,'best array with 3 antenna and cost 167.3758780615933.dat')
        # with open(filename, 'rb') as f:
        #     array_theta = pickle.load(f)
        # app.add_antenna(array_theta)
        # array_theta.name = "Array theta"

        # filedir = 'Optimization Results Phi'
        # filename = os.path.join(filedir,'best array with 1 antenna and cost 1134.8675783045935.dat')
        # # filename = os.path.join(filedir,'best array with 2 antenna and cost 206.2206481490366.dat')
        # # filename = os.path.join(filedir,'best array with 3 antenna and cost 167.3758780615933.dat')
        # with open(filename, 'rb') as f:
        #     array_phi = pickle.load(f)
        #     array_phi.name = "Array phi"
        # app.add_antenna(array_phi)
        
        # array_rhcp = Array(app.constants,name='Array rhcp',
        #               theta=theta.copy(),phi=phi.copy(),
        #               current_mirror=True,
        #               y_symmetry=True,
        #               y_mirror=True,
        #               x_mirror=True)
        # array_rhcp.add_antenna(array_theta)
        # array_rhcp.add_antenna(array_phi)
        # array_rhcp.antennas[1].set_position(y=1.5)
        # array_rhcp.antennas[1].set_current(current_phase=90)
        # array_rhcp.evaluate()
        # app.add_antenna(array_rhcp)
        
        # result_tab = ResultFrame(master=app.tabs,name='Array theta',
        #                           antenna=array_theta,analysis=F,
        #                           plot='2d Polar Patch')
        # app.add_result_tab(result_tab)
        
        # result_tab = ResultFrame(master=app.tabs,name='Array phi',
        #                           antenna=array_phi,analysis=F,
        #                           plot='2d Polar Patch')
        # app.add_result_tab(result_tab)
        
        # result_tab = ResultFrame(master=app.tabs,name='Array rhcp',
        #                           antenna=array_rhcp,analysis=Frhcp,
        #                           plot='2d Polar Patch')
        # app.add_result_tab(result_tab)
        
        # Main application loop
        app.mainloop()
    except Exception as e:
        # If some error occur, destroy the application to close the window,
        # then show the error
        app.destroy()
        raise e