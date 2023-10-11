# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 20:18:17 2023

@author: 160047412
"""

import tkinter as tk
from tkinter import ttk

class AxesEditorFrame(tk.Frame):
    def __init__(self,axes,app,on_finish=True,on_done=None,on_cancel=None,master=None,**kw):
        tk.Frame.__init__(self,master=master,width=300,height=200,**kw)
        self.app = app
        self.axes=axes
        self.on_finish=on_finish
        self.on_done=on_done
        self.on_cancel=on_cancel
        
        self.init_variables()
        self.init_layout()
    
    def init_variables(self):
        self.name = tk.StringVar()
    
    def init_layout(self):
        fr_left = tk.Frame(master=self)
        fr_left.pack(side='left',fill='both')
        fr_left_top = tk.Frame(master=fr_left)
        fr_left_top.pack(side='top',fill='both')
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Axes name:')
        fr_left_top_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left, textvariable=self.name).pack(side='left',fill='both')