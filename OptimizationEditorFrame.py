# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 00:28:57 2023

@author: 160047412
"""

import tkinter as tk
from tkinter import ttk
# import numpy as np

# from Antenna import Antenna
# from Analysis import Analysis
# from Optimization import Optimization
# from Result import Result

class OptimizationEditorFrame(tk.Frame):
    def __init__(self,optim,app,on_done=None,on_cancel=None,master=None,**kw):
        tk.Frame.__init__(self,master=master,width=300,height=200,**kw)
        self.app = app
        self.optim=optim
        self.on_done=on_done
        self.on_cancel=on_cancel
        
        self.available_arrays = [antenna for antenna in self.app.antennas if str(type(antenna))=="<class 'Array.Array'>"]
        self.available_antennas = [antenna for antenna in self.app.antennas]
        if self.optim.working_array is not None:
            self.working_array = self.optim.working_array
        elif len(self.available_arrays) > 0:
            self.working_array = self.available_arrays[0]
        else:
            self.working_array = None
        if self.working_array is not None:
            self.selectable_antennas = [antenna for antenna in self.working_array.antennas]
        else:
            self.selectable_antennas = []
        self.x_map = self.optim.x_map
        self.optim_map = dict()
        self.available_methods=['BFGS','L-BFGS-B','Nelder-Mead',
                                'Powell','CG','Newton-CG',
                                'TNC','COBYLA','SLSQP',
                                'trust-constr','dogleg','trust-ncg',
                                'trust-exact','trust-krylov']
        
        self.init_variables()
        self.init_layout()
        # self.set_variables()
        
        self.methods_cbbx.bind('<<ComboboxSelected>>',self.on_method_selection)
        self.select_antenna_cbbx.bind('<<ComboboxSelected>>',self.on_antenna_selection)
        self.working_array_cbbx.bind('<<ComboboxSelected>>',self.on_working_array_selection)
        self.on_working_array_selection()
    
    def init_variables(self):
        self.name = tk.StringVar(value='New optimization')
        self.select_antenna = tk.StringVar()
        self.selected_antenna_name = tk.StringVar()
        self.method = tk.StringVar(value=self.optim.method)
    
    def init_layout(self):
        fr_left = tk.Frame(master=self)
        fr_left.pack(side='left',fill='both')
        fr_left_top = ttk.LabelFrame(master=fr_left, text='Antenna name:')
        fr_left_top.pack(side='top',fill='both')
        ttk.Entry(master=fr_left_top, textvariable=self.name).pack(side='left',fill='both')
        fr_left_top = tk.Frame(master=fr_left)
        fr_left_top.pack(side='top',fill='both')
        fr_left_top_left = tk.Frame(master=fr_left_top)
        fr_left_top_left.pack(side='left',fill='both')
        fr_left_top_left_top = ttk.LabelFrame(master=fr_left_top_left, text='Methods')
        fr_left_top_left_top.pack(side='top',fill='both')
        self.methods_cbbx = ttk.Combobox(master=fr_left_top_left_top,state='readonly',values=self.available_methods,textvariable=self.method)
        self.methods_cbbx.pack(side='left',fill='both')
        fr_left_top_left_top = ttk.LabelFrame(master=fr_left_top_left, text='Working array')
        fr_left_top_left_top.pack(side='top',fill='both')
        self.working_array_cbbx = ttk.Combobox(master=fr_left_top_left_top,state='readonly',values=[array.name for array in self.available_arrays])
        self.working_array_cbbx.pack(side='left',fill='both')
        if len(self.available_arrays)>0:
            self.working_array_cbbx.current(0)
        fr_left_top_left_top = ttk.LabelFrame(master=fr_left_top_left, text='Target antenna')
        fr_left_top_left_top.pack(side='top',fill='both')
        self.target_antenna_cbbx = ttk.Combobox(master=fr_left_top_left_top,state='readonly',values=[antenna.name for antenna in self.available_antennas])
        self.target_antenna_cbbx.pack(side='left',fill='both')
        if len(self.available_antennas)>0:
            self.target_antenna_cbbx.current(0)
        fr_left_top_left_top = ttk.LabelFrame(master=fr_left_top_left, text='Analysis')
        fr_left_top_left_top.pack(side='top',fill='both')
        self.analyses_cbbx = ttk.Combobox(master=fr_left_top_left_top,state='readonly',values=[analysis.name for analysis in self.app.analyses])
        self.analyses_cbbx.pack(side='left',fill='both')
        if len(self.app.analyses)>0:
            self.analyses_cbbx.current(0)
        fr_left_top_left_top = ttk.LabelFrame(master=fr_left_top_left, text='Antennas')
        fr_left_top_left_top.pack(side='top',fill='both')
        self.select_antenna_cbbx = ttk.Combobox(master=fr_left_top_left_top,state='readonly',values=[antenna.name for antenna in self.selectable_antennas])
        self.select_antenna_cbbx.pack(side='left',fill='both')
        if len(self.selectable_antennas)>0:
            self.select_antenna_cbbx.current(0)
        fr_left_top = ttk.LabelFrame(master=fr_left,text='Finish')
        fr_left_top.pack(side='top',fill='both')
        ttk.Button(master=fr_left_top,text='Done',command=self._on_done).pack(side=tk.LEFT,fill=tk.BOTH)
        ttk.Button(master=fr_left_top,text='Cancel',command=self.on_cancel).pack(side=tk.LEFT,fill=tk.BOTH)
        self.edit_selected_antenna_frame = ttk.Frame(master=self)
        self.edit_selected_antenna_frame.pack(side='left',fill='both')
        self.edit_selected_method_frame = ttk.Frame(master=self)
        self.edit_selected_method_frame.pack(side='left',fill='both')
        # self.optim_map_lbfr = ttk.LabelFrame(master=fr_left, text='Optimization Mapping')
    
    def on_antenna_selection(self, event=None):
        for antenna in self.selectable_antennas:
            self.optim_map[antenna]['frame'].pack_forget()
        selection = self.select_antenna_cbbx.current()
        if selection == -1:
            return
        if self.working_array is None:
            return
        self.current_selected_antenna = ([antenna for antenna in self.selectable_antennas])[selection]
        self.optim_map[self.current_selected_antenna]['frame'].pack(side='left',fill='both')
    
    def on_working_array_selection(self, event=None):
        for c in self.edit_selected_antenna_frame.winfo_children():
            c.destroy()
        self.working_array = self.available_arrays[self.working_array_cbbx.current()]
        self.selectable_antennas = [antenna for antenna in self.working_array.antennas]
        self.select_antenna_cbbx.config(values=[antenna.name for antenna in self.selectable_antennas])
        self.optim_map = dict()
        if len(self.selectable_antennas)>0:
            for antenna in self.selectable_antennas:
                fr = tk.LabelFrame(master=self.edit_selected_antenna_frame,text='Optimize ' + antenna.name)
                self.optim_map[antenna] = dict(frame=fr,
                                               elevation=tk.IntVar(value=1),
                                               azimuth=tk.IntVar(value=1),
                                               x=tk.IntVar(value=0),
                                               y=tk.IntVar(value=0),
                                               z=tk.IntVar(value=0))
                tk.Checkbutton(master=fr,text='elevation',variable=self.optim_map[antenna]['elevation']).pack(side='top',fill='both')
                tk.Checkbutton(master=fr,text='azimuth',variable=self.optim_map[antenna]['azimuth']).pack(side='top',fill='both')
                tk.Checkbutton(master=fr,text='x',variable=self.optim_map[antenna]['x']).pack(side='top',fill='both')
                tk.Checkbutton(master=fr,text='y',variable=self.optim_map[antenna]['y']).pack(side='top',fill='both')
                tk.Checkbutton(master=fr,text='z',variable=self.optim_map[antenna]['z']).pack(side='top',fill='both')
            self.select_antenna_cbbx.current(0)
            self.on_antenna_selection()
    
    def on_method_selection(self, event=None):
        for c in self.edit_selected_method_frame.winfo_children():
            c.destroy()
        self.method_map = dict()
        method = self.method.get()
        if method=='BFGS':
            print('BFGS')
        elif method=='L-BFGS-B':
            print('L-BFGS-B')
    
    def _on_done(self):
        if len(self.available_antennas)>0:
            target_antenna = self.available_antennas[self.target_antenna_cbbx.current()]
        if len(self.app.analyses)>0:
            analyses = [self.app.analyses[self.analyses_cbbx.current()]]
        x_map = []
        for antenna in self.optim_map.keys():
            optim_map = self.optim_map[antenna]
            optim_map.pop('frame')
            x_map.append({
                'obj':antenna,
                'variables':[key for key in optim_map.keys() if optim_map[key].get()]
            })
        self.optim.config(name=self.name.get(),method=self.method.get(),
                          working_array=self.working_array,
                          target_antenna=target_antenna,
                          analyses=analyses,
                          x_map=x_map)
        # print(x_map)
        self.on_done()