# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 14:56:38 2023

@author: 160047412
"""

import tkinter as tk
from tkinter import ttk
import numpy as np

from NumpyExpressionParser import NumpyExpressionParser as NEP

class AntennaEditorFrame(tk.Frame):
    def __init__(self,antenna,on_finish=True,on_done=None,on_cancel=None,master=None,**kw):
        tk.Frame.__init__(self,master=master,**kw)
        self.antenna=antenna
        self.on_finish=on_finish
        self.on_done=on_done
        self.on_cancel=on_cancel
        
        self.init_variables()
        self.init_layout()
        self.radiobutton_change()
    
    def init_variables(self,):
        self.name = tk.StringVar(value=self.antenna.name)
        self.current_mag = tk.DoubleVar(value=self.antenna.current_mag)
        self.current_phase = tk.DoubleVar(value=self.antenna.current_phase)
        self.theta_initial = tk.DoubleVar(value=np.min(self.antenna.theta))
        self.theta_final = tk.DoubleVar(value=np.max(self.antenna.theta))
        self.theta_N = tk.IntVar(value=self.antenna.theta.size)
        self.phi_initial = tk.DoubleVar(value=np.min(self.antenna.phi))
        self.phi_final = tk.DoubleVar(value=np.max(self.antenna.phi))
        self.phi_N = tk.IntVar(value=self.antenna.phi.size)
        self.elevation = tk.DoubleVar(value=self.antenna.elevation)
        self.azimuth = tk.DoubleVar(value=self.antenna.azimuth)
        self.roll = tk.DoubleVar(value=self.antenna.roll)
        self.position = tk.StringVar(value=str([self.antenna.x,self.antenna.y,self.antenna.z]))
        
        if self.antenna.evaluate_as=='isotropic':
            self.radiobutton_variable = tk.StringVar(value='Isotropic')
        elif self.antenna.evaluate_as=='ideal dipole':
            self.radiobutton_variable = tk.StringVar(value='Ideal dipole')
        elif self.antenna.evaluate_as=='ideal loop dipole':
            self.radiobutton_variable = tk.StringVar(value='Ideal loop dipole')
        elif self.antenna.evaluate_as=='expressions':
            self.radiobutton_variable = tk.StringVar(value='Expressions')
        elif self.antenna.evaluate_as=='load file':
            self.radiobutton_variable = tk.StringVar(value='Load file')
        
        self.ideal_dipole_length = tk.DoubleVar(value=self.antenna.evaluation_arguments['dipole length'])
        self.ideal_loop_dipole_area = tk.DoubleVar(value=self.antenna.evaluation_arguments['loop dipole area'])
        self.expression_theta = tk.StringVar(value=self.antenna.evaluation_arguments['expression theta'])
        self.expression_phi = tk.StringVar(value=self.antenna.evaluation_arguments['expression phi'])
        self.isotropic_radiobutton_variable = tk.StringVar(value=self.antenna.evaluation_arguments['isotropic on'])
        self.file_path = tk.StringVar(value=self.antenna.evaluation_arguments['file path'])
        self.load_mesh_from_file = tk.IntVar(value=self.antenna.evaluation_arguments['load mesh from file'])
    
    def init_layout(self):
        fr_top = tk.Frame(master=self)
        fr_top.pack(side='top',fill='both')
        fr = ttk.LabelFrame(master=fr_top, text='Antenna name:')
        fr.pack(side='left',fill='both')
        ttk.Entry(master=fr, textvariable=self.name).pack(side='left',fill='both')
        fr = ttk.LabelFrame(master=fr_top, text='Current magnitude:')
        fr.pack(side='left',fill='both')
        ttk.Entry(master=fr, textvariable=self.current_mag).pack(side='left',fill='both')
        fr = ttk.LabelFrame(master=fr_top, text='Current phase:')
        fr.pack(side='left',fill='both')
        ttk.Entry(master=fr, textvariable=self.current_phase).pack(side='left',fill='both')
        tk.Button(master=fr_top,text='update',command=self._on_update).pack(side='left',fill='both')
        
        fr = ttk.LabelFrame(master=self, text='Phi angle samples: linspace(start, stop, num)')
        fr.pack(side='top',fill='both')
        ttk.Label(master=fr, text='Start').grid(row=0,column=0)
        ttk.Label(master=fr, text='Stop').grid(row=0,column=1)
        ttk.Label(master=fr, text='Num').grid(row=0,column=2)
        ttk.Entry(master=fr, textvariable=self.phi_initial).grid(row=1,column=0)
        ttk.Entry(master=fr, textvariable=self.phi_final).grid(row=1,column=1)
        ttk.Entry(master=fr, textvariable=self.phi_N).grid(row=1,column=2)
        fr = ttk.LabelFrame(master=self, text='Theta angle samples: linspace(start, stop, num)')
        fr.pack(side='top',fill='both')
        ttk.Label(master=fr, text='Start').grid(row=0,column=0)
        ttk.Label(master=fr, text='Stop').grid(row=0,column=1)
        ttk.Label(master=fr, text='Num').grid(row=0,column=2)
        ttk.Entry(master=fr, textvariable=self.theta_initial).grid(row=1,column=0)
        ttk.Entry(master=fr, textvariable=self.theta_final).grid(row=1,column=1)
        ttk.Entry(master=fr, textvariable=self.theta_N).grid(row=1,column=2)
        fr = tk.Frame(master=self)
        fr.pack(side='top',fill='both')
        fr2 = ttk.LabelFrame(master=fr, text='Elevation')
        fr2.pack(side='left',fill='both')
        ttk.Entry(master=fr2, textvariable=self.elevation).pack(side='top',fill='both')
        fr2 = ttk.LabelFrame(master=fr, text='Azimuth')
        fr2.pack(side='left',fill='both')
        ttk.Entry(master=fr2, textvariable=self.azimuth).pack(side='top',fill='both')
        fr2 = ttk.LabelFrame(master=fr, text='Roll')
        fr2.pack(side='left',fill='both')
        ttk.Entry(master=fr2, textvariable=self.roll).pack(side='top',fill='both')
        fr2 = ttk.LabelFrame(master=fr, text='Position')
        fr2.pack(side='left',fill='both')
        ttk.Entry(master=fr2, textvariable=self.position).pack(side='top',fill='both')
        fr2 = ttk.LabelFrame(master=fr, text='Radiation pattern (F)')
        fr2.pack(side=tk.TOP,fill=tk.BOTH)
        fr = tk.Frame(master=self)
        fr.pack(side='top',fill='both')
        radiobutton_frame = tk.LabelFrame(master=fr,text='Options')
        radiobutton_frame.pack(side=tk.LEFT,fill=tk.BOTH)
        tk.Radiobutton(master=radiobutton_frame,text='Isotropic',value='Isotropic',variable=self.radiobutton_variable,command=self.radiobutton_change).pack(side=tk.TOP,fill=tk.BOTH)
        tk.Radiobutton(master=radiobutton_frame,text='Ideal dipole',value='Ideal dipole',variable=self.radiobutton_variable,command=self.radiobutton_change).pack(side=tk.TOP,fill=tk.BOTH)
        tk.Radiobutton(master=radiobutton_frame,text='Ideal loop dipole',value='Ideal loop dipole',variable=self.radiobutton_variable,command=self.radiobutton_change).pack(side=tk.TOP,fill=tk.BOTH)
        tk.Radiobutton(master=radiobutton_frame,text='Expressions',value='Expressions',variable=self.radiobutton_variable,command=self.radiobutton_change).pack(side=tk.TOP,fill=tk.BOTH)
        tk.Button(master=radiobutton_frame,text='Load from file...',command=self.load_file).pack(side=tk.TOP,fill=tk.BOTH)
        electric_field_frame = tk.Frame(master=fr)
        electric_field_frame.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        self.isotropic_frame = tk.LabelFrame(master=electric_field_frame,text='Isotropic antenna')
        tk.Radiobutton(master=self.isotropic_frame,text='Isotropic on both',value='both',variable=self.isotropic_radiobutton_variable).pack(side=tk.TOP,fill=tk.BOTH)
        tk.Radiobutton(master=self.isotropic_frame,text='Isotropic on theta',value='theta',variable=self.isotropic_radiobutton_variable).pack(side=tk.TOP,fill=tk.BOTH)
        tk.Radiobutton(master=self.isotropic_frame,text='Isotropic on phi',value='phi',variable=self.isotropic_radiobutton_variable).pack(side=tk.TOP,fill=tk.BOTH)
        self.ideal_dipole_frame = tk.LabelFrame(master=electric_field_frame,text='Ideal dipole length (L)')
        self.ideal_loop_dipole_frame = tk.LabelFrame(master=electric_field_frame,text='Ideal loop dipole area (S)')
        self.expression_frame = tk.LabelFrame(master=electric_field_frame,text='Expressions')
        self.load_file_frame = tk.LabelFrame(master=electric_field_frame,text='Load file')
        ttk.Label(master=self.expression_frame,text='Expression theta').grid(row=0,column=0)
        ttk.Label(master=self.expression_frame,text='Expression phi').grid(row=1,column=0)
        ttk.Entry(master=self.ideal_dipole_frame,textvariable=self.ideal_dipole_length).pack(side='left',fill='x')
        ttk.Entry(master=self.ideal_loop_dipole_frame,textvariable=self.ideal_loop_dipole_area).pack(side='left',fill='x')
        ttk.Entry(master=self.expression_frame,textvariable=self.expression_theta).grid(row=0,column=1)
        ttk.Entry(master=self.expression_frame,textvariable=self.expression_phi).grid(row=1,column=1)
        ttk.Entry(master=self.load_file_frame,textvariable=self.file_path).pack(side='top',expand=True,fill='x')
        tk.Checkbutton(master=self.load_file_frame,text='Load mesh from file',variable=self.load_mesh_from_file).pack(side='bottom',fill='both')
        if self.on_finish:
            fr = ttk.LabelFrame(master=self,text='Finish')
            fr.pack(side='top',fill='both')
            ttk.Button(master=fr,text='Done',command=self._on_done).pack(side=tk.LEFT,fill=tk.BOTH)
            ttk.Button(master=fr,text='Cancel',command=self.on_cancel).pack(side=tk.LEFT,fill=tk.BOTH)
    
    def _on_update(self):
        if self.radiobutton_variable.get()=='Isotropic':
            evaluate_as = 'isotropic'
        elif self.radiobutton_variable.get()=='Ideal dipole':
            evaluate_as = 'ideal dipole'
        elif self.radiobutton_variable.get()=='Ideal loop dipole':
            evaluate_as = 'ideal loop_dipole'
        elif self.radiobutton_variable.get()=='Expressions':
            evaluate_as = 'expressions'
        elif self.radiobutton_variable.get()=='Load file':
            evaluate_as = 'load file'
        self.antenna.set_evaluation_method(evaluate_as)
        self.antenna.evaluation_arguments['dipole length'] = self.ideal_dipole_length.get()
        self.antenna.evaluation_arguments['loop dipole area'] = self.ideal_loop_dipole_area.get()
        self.antenna.evaluation_arguments['expression theta'] = self.expression_theta.get()
        self.antenna.evaluation_arguments['expression phi'] = self.expression_phi.get()
        self.antenna.evaluation_arguments['isotropic on'] = self.isotropic_radiobutton_variable.get()
        self.antenna.evaluation_arguments['file path'] = self.file_path.get()
        self.antenna.evaluation_arguments['force reload'] = True
        self.antenna.evaluation_arguments['load mesh from file'] = self.load_mesh_from_file.get()
        
        self.antenna.set_current(current_mag = self.current_mag.get(),
                                 current_phase = self.current_phase.get())
        
        position = NEP.eval(expression=self.position.get())
        self.antenna.set_position(x=position[0],y=position[1],z=position[2])
        
        self.antenna.set_orientation(elevation=self.elevation.get(),
                                   azimuth=self.azimuth.get(),
                                   roll=self.roll.get())
        
        self.antenna.resample(theta=np.linspace(self.theta_initial.get(),self.theta_final.get(),self.theta_N.get()),
                            phi=np.linspace(self.phi_initial.get(),self.phi_final.get(),self.phi_N.get()))
        
        self.antenna.set_name(name=self.name.get())
        
        self.antenna.evaluate()
    
    def _on_done(self):
        self._on_update()
        if self.on_done is not None:
            self.on_done()
    
    def radiobutton_change(self):
        self.isotropic_frame.pack_forget()
        self.ideal_dipole_frame.pack_forget()
        self.ideal_loop_dipole_frame.pack_forget()
        self.expression_frame.pack_forget()
        self.load_file_frame.pack_forget()
        if self.radiobutton_variable.get()=='Isotropic':
            self.isotropic_frame.pack(side=tk.LEFT,fill=tk.X)
        elif self.radiobutton_variable.get()=='Ideal dipole':
            self.ideal_dipole_frame.pack(side=tk.LEFT,fill=tk.X)
        elif self.radiobutton_variable.get()=='Ideal loop dipole':
            self.ideal_loop_dipole_frame.pack(side=tk.LEFT,fill=tk.X)
        elif self.radiobutton_variable.get()=='Expressions':
            self.expression_frame.pack(side=tk.LEFT,fill=tk.X)
        elif self.radiobutton_variable.get()=='Load file':
            self.load_file_frame.pack(side='left',expand=True,fill='x')
    
    def load_file(self):
        self.ideal_dipole_frame.pack_forget()
        self.ideal_loop_dipole_frame.pack_forget()
        self.expression_frame.pack_forget()
        self.load_file_frame.pack_forget()
        self.radiobutton_variable.set('Load file')
        file_path = tk.filedialog.askopenfilename(initialfile=self.file_path.get())
        if file_path != '':
            self.file_path.set(file_path)
        self.load_file_frame.pack(side='left',expand=True,fill='x')

if __name__=="__main__":
    from Antenna import Antenna
    
    constants = dict()
    constants['c'] = 299792458 # m/s
    constants['f'] = 433e6 # Hz
    constants['eta'] = 120*np.pi
    constants['lam'] = constants['c']/constants['f'] # m
    constants['w'] = 2*np.pi*constants['f'] # rad/s
    constants['k'] = 2*np.pi/constants['lam'] # rad/m
    
    antenna = Antenna(constants=constants)
    
    root = tk.Tk()
    
    def on_done():
        print('done')
        root.destroy()
    
    def on_cancel():
        print('cancel')
        root.destroy()
    
    AntennaEditorFrame(antenna=antenna,on_done=on_done,on_cancel=on_cancel,master=root).pack(side=tk.LEFT,fill=tk.BOTH)
    root.mainloop()