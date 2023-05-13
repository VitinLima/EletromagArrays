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
        
        ttk.Button(master=fr,text='Done',command=self._on_done).pack(side=tk.LEFT,fill=tk.BOTH)
        ttk.Button(master=fr,text='Cancel',command=self.on_cancel).pack(side=tk.LEFT,fill=tk.BOTH)
    
    def _on_done(self):
        self.analysis.config(name=self.name.get(),
                             expression=self.expression.get(),
                             color_expression=self.color_expression.get())
        
        self.on_done()