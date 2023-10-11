# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 23:18:10 2023

@author: 160047412
"""

import tkinter as tk
from tkinter import ttk
import numpy as np

import Antenna,AntennaEditorFrame
from NumpyExpressionParser import NumpyExpressionParser as NEP

class ArrayEditorFrame(tk.Frame):
    def __init__(self,array,app,on_finish=True,on_done=None,on_cancel=None,master=None,**kw):
        tk.Frame.__init__(self,master=master,width=300,height=200,**kw)
        self.app = app
        self.array=array
        self.on_finish=on_finish
        self.on_done=on_done
        self.on_cancel=on_cancel
        
        self.antennas = [antenna for antenna in self.array.antennas]
        self.current_editing_antenna = None
        self.current_editing_frame = None
        
        self.init_variables()
        self.init_layout()
        
        self.select_antenna_lstbx.bind('<<ListboxSelect>>',self.on_antenna_selection)
    
    def init_variables(self):
        self.name = tk.StringVar(value=self.array.name)
        self.current_magnitude = tk.DoubleVar(value=self.array.current_magnitude)
        self.current_phase = tk.DoubleVar(value=self.array.current_phase)
        self.phi_initial = tk.DoubleVar(value=np.min(self.array.phi))
        self.phi_final = tk.DoubleVar(value=np.max(self.array.phi))
        self.phi_N = tk.IntVar(value=self.array.phi.size)
        self.theta_initial = tk.DoubleVar(value=np.min(self.array.theta))
        self.theta_final = tk.DoubleVar(value=np.max(self.array.theta))
        self.theta_N = tk.IntVar(value=self.array.theta.size)
        self.azimuth = tk.DoubleVar(value=self.array.azimuth)
        self.elevation = tk.DoubleVar(value=self.array.elevation)
        self.position = tk.StringVar(value=str([self.array.x,self.array.y,self.array.z]))
        self.x_mirror_variable = tk.IntVar(value=self.array.x_mirror)
        self.y_mirror_variable = tk.IntVar(value=self.array.y_mirror)
        self.z_mirror_variable = tk.IntVar(value=self.array.z_mirror)
        self.current_mirror_variable = tk.IntVar(value=self.array.current_mirror)
        self.azimuth_symmetry_variable = tk.IntVar(value=self.array.azimuth_symmetry)
        
        self.edit_antenna_frame_label = tk.StringVar()
    
    def init_layout(self):
        fr_left = tk.Frame(master=self)
        fr_left.pack(side='left',fill='both')
        fr_left_top = tk.Frame(master=fr_left)
        fr_left_top.pack(side='top',fill='both')
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Array name:')
        fr_left_top_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left, textvariable=self.name).pack(side='left',fill='both')
        
        fr = ttk.LabelFrame(master=fr_left_top_left, text='Current magnitude:')
        fr.pack(side='left',fill='both')
        ttk.Entry(master=fr, textvariable=self.current_magnitude).pack(side='left',fill='both')
        
        fr = ttk.LabelFrame(master=fr_left_top_left, text='Current phase:')
        fr.pack(side='left',fill='both')
        ttk.Entry(master=fr, textvariable=self.current_phase).pack(side='left',fill='both')
        
        tk.Button(master=fr_left_top_left,text='update',command=self._on_update).pack(side='left',fill='both')
        
        fr_left_top = ttk.LabelFrame(master=fr_left, text='Phi angle samples: linspace(start, stop, num)')
        fr_left_top.pack(side='top',fill='both')
        ttk.Label(master=fr_left_top, text='Start').grid(row=0,column=0)
        ttk.Label(master=fr_left_top, text='Stop').grid(row=0,column=1)
        ttk.Label(master=fr_left_top, text='Num').grid(row=0,column=2)
        ttk.Entry(master=fr_left_top, textvariable=self.phi_initial).grid(row=1,column=0)
        ttk.Entry(master=fr_left_top, textvariable=self.phi_final).grid(row=1,column=1)
        ttk.Entry(master=fr_left_top, textvariable=self.phi_N).grid(row=1,column=2)
        fr_left_top = ttk.LabelFrame(master=fr_left, text='Theta angle samples: linspace(start, stop, num)')
        fr_left_top.pack(side='top',fill='both')
        ttk.Label(master=fr_left_top, text='Start').grid(row=0,column=0)
        ttk.Label(master=fr_left_top, text='Stop').grid(row=0,column=1)
        ttk.Label(master=fr_left_top, text='Num').grid(row=0,column=2)
        ttk.Entry(master=fr_left_top, textvariable=self.theta_initial).grid(row=1,column=0)
        ttk.Entry(master=fr_left_top, textvariable=self.theta_final).grid(row=1,column=1)
        ttk.Entry(master=fr_left_top, textvariable=self.theta_N).grid(row=1,column=2)
        
        fr_left_top = tk.Frame(master=fr_left)
        fr_left_top.pack(side='top',fill='both')
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Elevation')
        fr_left_top_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left, textvariable=self.elevation).pack(side='top',fill='both')
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Azimuth')
        fr_left_top_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left, textvariable=self.azimuth).pack(side='top',fill='both')
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Position')
        fr_left_top_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left, textvariable=self.position).pack(side='top',fill='both')
        
        fr_left_top = tk.Frame(master=fr_left)
        fr_left_top.pack(side='top',fill='both')
        mirror_frame = ttk.LabelFrame(master=fr_left_top, text='Mirror:')
        mirror_frame.pack(side='left',fill='both')
        tk.Checkbutton(master=mirror_frame, text='YZ plane',variable=self.x_mirror_variable).grid(row=0,column=0)
        tk.Checkbutton(master=mirror_frame, text='ZX plane',variable=self.y_mirror_variable).grid(row=1,column=0)
        tk.Checkbutton(master=mirror_frame, text='XY plane',variable=self.z_mirror_variable).grid(row=2,column=0)
        tk.Checkbutton(master=mirror_frame, text='Current',variable=self.current_mirror_variable).grid(row=3,column=0)
        symmetry_frame = ttk.LabelFrame(master=fr_left_top, text='Symmetry:')
        symmetry_frame.pack(side='left',fill='both')
        tk.Checkbutton(master=symmetry_frame, text='Azimuth',variable=self.azimuth_symmetry_variable).grid(row=0,column=1)
        
        if self.on_finish:
            fr_left_top = ttk.LabelFrame(master=fr_left,text='Finish')
            fr_left_top.pack(side='top',fill='both')
            ttk.Button(master=fr_left_top,text='Done',command=self._on_done).pack(side=tk.LEFT,fill=tk.BOTH)
            ttk.Button(master=fr_left_top,text='Cancel',command=self.on_cancel).pack(side=tk.LEFT,fill=tk.BOTH)
        
        fr_left = ttk.LabelFrame(master=self, text='Antennas')
        fr_left.pack(side='left',fill='both')
        tk.Button(master=fr_left,text='add',command=self.on_add_antenna).pack(side='top',fill='both')
        tk.Button(master=fr_left,text='remove',command=self.on_remove_antenna).pack(side='top',fill='both')
        self.select_antenna_lstbx = tk.Listbox(master=fr_left)
        self.select_antenna_lstbx.pack(side='top',fill='both')
        for antenna in self.antennas:
            self.select_antenna_lstbx.insert(tk.END, antenna.name)
        
        self.edit_antenna_frame = tk.Frame(master=self)
    
    def on_antenna_selection(self, event=None):
        selection = self.select_antenna_lstbx.curselection()
        if len(selection)==0:
            return
        if self.current_editing_frame is not None:
            self.current_editing_frame._on_done()
            self.current_editing_frame.destroy()
            self.array.evaluate()
        self.edit_antenna_frame.pack_forget()
        self.current_editing_antenna = ([antenna for antenna in self.antennas])[selection[0]]
        if str(self.current_editing_antenna.EditorFrame) == "<class 'AntennaEditorFrame.AntennaEditorFrame'>":
            self.current_editing_frame = AntennaEditorFrame.AntennaEditorFrame(antenna=self.current_editing_antenna,on_finish=False,master=self.edit_antenna_frame)
        elif str(self.current_editing_antenna.EditorFrame) == "<class 'ArrayEditorFrame.ArrayEditorFrame'>":
            self.current_editing_frame = ArrayEditorFrame(array=self.current_editing_antenna,app=self.app,on_finish=False,master=self.edit_antenna_frame)
        self.current_editing_frame.pack(side='left',fill='both')
        self.edit_antenna_frame.pack(side='left',fill='both')
    
    def on_add_antenna(self):
        root = tk.Toplevel()
        N_antennas = tk.IntVar(value=1)
        def on_new():
            for i in range(N_antennas.get()):
                antenna = Antenna()
                self.array.antennas.append(antenna)
                self.antennas.append(antenna)
                self.select_antenna_lstbx.insert(tk.END,antenna.name)
            root.destroy()
        def on_copy_from():
            def on_done():
                sel = lstbx.curselection()
                if len(sel)>0:
                    selected_antenna = self.app.antennas[sel[0]]
                    for i in range(N_antennas.get()):
                        antenna = selected_antenna.copy()
                        self.array.antennas.append(antenna)
                        self.antennas.append(antenna)
                        self.select_antenna_lstbx.insert(tk.END,antenna.name)
                root.destroy()
            for c in root.winfo_children():
                c.destroy()
            tk.Entry(master=root,textvariable=N_antennas).pack(side='top',fill='both')
            lstbx = tk.Listbox(master=root)
            lstbx.pack(side='left',fill='both')
            tk.Button(master=root,text='done',command=on_done).pack(side='left',fill='both')
            for antenna in self.app.antennas:
                lstbx.insert(tk.END, antenna.name)
        def on_cancel():
            root.destroy()
        tk.Entry(master=root,textvariable=N_antennas).pack(side='top',fill='both')
        tk.Button(master=root,text='New',command=on_new).pack(side='top',fill='both')
        tk.Button(master=root,text='Copy from',command=on_copy_from).pack(side='top',fill='both')
        tk.Button(master=root,text='Cancel',command=on_cancel).pack(side='top',fill='both')
        root.mainloop()
    
    def on_remove_antenna(self):
        selection = self.select_antenna_lstbx.curselection()
        if len(selection)==0:
            return
        if self.current_editing_frame is not None:
            self.current_editing_frame._on_done()
            self.current_editing_frame.destroy()
        antenna = ([antenna for antenna in self.antennas])[selection[0]]
        self.array.antennas.remove(antenna)
        self.select_antenna_lstbx.delete(0,tk.END)
        self.antennas = [antenna for antenna in self.array.antennas]
        for antenna in self.antennas:
            self.select_antenna_lstbx.insert(tk.END, antenna.name)
    
    def _on_done(self):
        self._on_update()
        if self.on_done is not None:
            self.on_done()

    def _on_update(self):
        if self.current_editing_frame is not None:
            self.current_editing_frame._on_update()
        
        self.array.set_current(magnitude = self.current_magnitude.get(),
                               phase = self.current_phase.get())
        
        # self.array.set_symmetry(x_mirror = self.x_mirror_variable.get()==1,
        #                         y_mirror = self.y_mirror_variable.get()==1,
        #                         z_mirror = self.z_mirror_variable.get()==1,
        #                         current_mirror = self.current_mirror_variable.get()==1,
        #                         azimuth_symmetry = self.azimuth_symmetry_variable.get()==1)
        
        position = NEP.eval(expression=self.position.get())
        self.array.set_position(x=position[0],y=position[1],z=position[2])
        
        self.array.set_orientation(elevation=self.elevation.get(),
                                   azimuth=self.azimuth.get())
        
        self.array.resample(theta=np.linspace(self.theta_initial.get(),self.theta_final.get(),self.theta_N.get()),
                            phi=np.linspace(self.phi_initial.get(),self.phi_final.get(),self.phi_N.get()))
        
        self.array.set_name(name=self.name.get())
        
        self.array.evaluate()