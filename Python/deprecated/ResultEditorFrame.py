# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 00:28:41 2023

@author: 160047412
"""

import tkinter as tk
from tkinter import ttk

class ResultEditorFrame(tk.Frame):
    def __init__(self,result,app,on_finish=True,on_done=None,on_cancel=None,master=None,**kw):
        tk.Frame.__init__(self,master=master,width=300,height=200,**kw)
        self.app = app
        self.result=result
        self.on_finish=on_finish
        self.on_done=on_done
        self.on_cancel=on_cancel
        
        self.init_variables()
        self.init_layout()
    
    def init_variables(self):
        self.name = tk.StringVar(value=self.result.name)
        self.projection_variable = tk.StringVar(value=self.result.projection)
        self.plot_variable = tk.StringVar(value=self.result.plot)
    
    def init_layout(self):
        fr_top = tk.Frame(master=self)
        fr_top.pack(side='top',fill='both')
        
        fr_top_left = ttk.LabelFrame(master=fr_top, text='Result name:')
        fr_top_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_top_left,textvariable=self.name).pack(side='left',fill='both')
        
        tk.Button(master=fr_top,text='update',command=self._on_update).pack(side='left',fill='both')
        
        fr_top = tk.Frame(master=self)
        fr_top.pack(side='top',fill='both')
        
        fr_top_left = ttk.LabelFrame(master=fr_top, text='Antennas')
        fr_top_left.pack(side='left',fill='both')
        self.antenna_cbbx = ttk.Combobox(master=fr_top_left,state='readonly',values=[antenna.name for antenna in self.app.antennas])
        self.antenna_cbbx.pack(side='left',fill='both')
        if len(self.app.antennas)>0:
            if self.result.antenna is not None:
                self.antenna_cbbx.current(self.app.antennas.index(self.result.antenna))
            else:
                self.antenna_cbbx.current(0)
        
        fr_top_left = ttk.LabelFrame(master=fr_top, text='Analysis')
        fr_top_left.pack(side='left',fill='both')
        self.analysis_cbbx = ttk.Combobox(master=fr_top_left,state='readonly',values=[analysis.name for analysis in self.app.analyses])
        self.analysis_cbbx.pack(side='left',fill='both')
        if len(self.app.analyses)>0:
            if self.result.analysis is not None:
                self.analysis_cbbx.current(self.app.analyses.index(self.result.analysis))
            else:
                self.analysis_cbbx.current(0)
        
        fr_top = tk.Frame(master=self)
        fr_top.pack(side='top',fill='both')
        
        # fr_top_left = ttk.LabelFrame(master=fr_top, text='Projection')
        # fr_top_left.pack(side='left',fill='both')
        # ttk.Combobox(master=fr_top_left,state='readonly',values=['3d','2d'],textvariable=self.projection_variable).pack(side='left',fill='both')
        
        fr_top_left = ttk.LabelFrame(master=fr_top, text='Plot')
        fr_top_left.pack(side='left',fill='both')
        ttk.Combobox(master=fr_top_left,state='readonly',values=['Graph','Contour','Surface','Polar Graph', 'Polar Contour','Polar 3D', 'Polar Surface'],textvariable=self.plot_variable).pack(side='left',fill='both')
        
        if self.on_finish:
            fr_top = ttk.LabelFrame(master=self,text='Finish')
            fr_top.pack(side='top',fill='both')
            ttk.Button(master=fr_top,text='Done',command=self._on_done).pack(side=tk.LEFT,fill=tk.BOTH)
            ttk.Button(master=fr_top,text='Cancel',command=self.on_cancel).pack(side=tk.LEFT,fill=tk.BOTH)
    
    def _on_update(self):
        self.result.name = self.name.get()
        self.result.set_antenna(self.app.antennas[self.antenna_cbbx.current()])
        self.result.set_analysis(self.app.analyses[self.analysis_cbbx.current()])
        self.result.set_plot(self.plot_variable.get())
        
        self.result.ok = False
        self.result.update()
    
    def _on_done(self):
        self._on_update()
        self.on_done()