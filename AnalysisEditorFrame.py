# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 00:29:03 2023

@author: 160047412
"""

import tkinter as tk
from tkinter import ttk

class AnalysisEditorFrame(tk.Frame):
    def __init__(self,analysis,on_done=None,on_cancel=None,master=None,**kw):
        tk.Frame.__init__(self,master=master,width=300,height=200,**kw)
        self.analysis=analysis
        self.on_done=on_done
        self.on_cancel=on_cancel
        
        self.init_variables()
        self.init_layout()
    
    def init_variables(self):
        self.name = tk.StringVar(value=self.analysis.name)
        self.expression = tk.StringVar(value=self.analysis.expression)
        self.color_expression = tk.StringVar(value=self.analysis.color_expression)
        self.cross_polarization_X_variable = tk.DoubleVar(value=self.analysis.cross_polarization_X)
        self.cross_polarization_Y_variable = tk.DoubleVar(value=self.analysis.cross_polarization_Y)
        self.cross_polarization_Z_variable = tk.DoubleVar(value=self.analysis.cross_polarization_Z)
    
    def init_layout(self):
        fr = ttk.LabelFrame(master=self, text='Analysis name:')
        fr.pack(side='top',fill='both')
        ttk.Entry(master=fr, textvariable=self.name).pack(side='left',fill='both')
        fr = ttk.LabelFrame(master=self, text='Expression:')
        fr.pack(side='top',fill='both')
        ttk.Entry(master=fr, textvariable=self.expression).pack(side='left',fill='both')
        fr = ttk.LabelFrame(master=self, text='Color:')
        fr.pack(side='top',fill='both')
        ttk.Entry(master=fr, textvariable=self.color_expression).pack(side='left',fill='both')
        fr = ttk.LabelFrame(master=self,text='Finish')
        fr.pack(side='top',fill='both')
        
        fr_left_top = ttk.Frame(master=fr)
        fr_left_top.pack(side='top',fill='both')
        
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Cross Polarization Plane')
        fr_left_top_left.pack(side='left',fill='both')
        fr_left_top_left_left = ttk.LabelFrame(master=fr_left_top_left, text='X')
        fr_left_top_left_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left_left,textvariable=self.cross_polarization_X_variable).pack(side='left',fill='both')
        fr_left_top_left_left = ttk.LabelFrame(master=fr_left_top_left, text='Y')
        fr_left_top_left_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left_left,textvariable=self.cross_polarization_Y_variable).pack(side='left',fill='both')
        fr_left_top_left_left = ttk.LabelFrame(master=fr_left_top_left, text='Z')
        fr_left_top_left_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left_left,textvariable=self.cross_polarization_Z_variable).pack(side='left',fill='both')
        
        ttk.Button(master=fr,text='Done',command=self._on_done).pack(side=tk.LEFT,fill=tk.BOTH)
        ttk.Button(master=fr,text='Cancel',command=self.on_cancel).pack(side=tk.LEFT,fill=tk.BOTH)
    
    def _on_done(self):
        self.analysis.config(name=self.name.get(),
                             expression=self.expression.get(),
                             color_expression=self.color_expression.get())
        self.analysis.cross_polarization_X = self.cross_polarization_X_variable.get()
        self.analysis.cross_polarization_Y = self.cross_polarization_Y_variable.get()
        self.analysis.cross_polarization_Z = self.cross_polarization_Z_variable.get()
        
        self.on_done()