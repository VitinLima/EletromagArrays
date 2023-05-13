# -*- coding: utf-8 -*-
"""
Created on Sat May 13 13:46:32 2023

@author: 160047412
"""

import tkinter as tk
from tkinter import ttk

# from AxesEditorFrame import AxesEditorFrame

class FieldResultEditorFrame(ttk.Frame):
    def __init__(self,app,result,on_finish=True,on_done=None,on_cancel=None,master=None,**kw):
        ttk.Frame.__init__(self,master=master,width=300,height=200,**kw)
        self.app = app
        self.result = result
        self.on_finish=on_finish
        self.on_done=on_done
        self.on_cancel=on_cancel
        
        self.current_plot_frame = None
        
        self.init_variables()
        self.init_layout()
        
        self._on_plot_change()
        # self._on_builtin_field_change()
        
        # self.select_axes_lstbx.bind('<<ListboxSelect>>',self.on_axes_selection)
    
    def init_variables(self):
        self.name = tk.StringVar(value=self.result.name)
        self.projection_variable = tk.StringVar(value=self.result.projection)
        self.plot_variable = tk.StringVar(value=self.result.plot)
        self.field_variable = tk.StringVar(value=self.result.field)
        self.color_variable = tk.StringVar(value=self.result.color)
        self.color_textvariable = tk.StringVar(value=self.result.color)
        
        self.reference_plane_X_variable = tk.DoubleVar(value=self.result.reference_plane_X)
        self.reference_plane_Y_variable = tk.DoubleVar(value=self.result.reference_plane_Y)
        self.reference_plane_Z_variable = tk.DoubleVar(value=self.result.reference_plane_Z)
        
        self.in_dB_variable = tk.IntVar(value=self.result.in_dB)
        self.dynamic_scaling_dB_variable = tk.DoubleVar(value=self.result.dynamic_scaling_dB)
        self.hide_axis_variable = tk.IntVar(value=self.result.hide_axis)
        
        # self.edit_axes_frame_label = tk.StringVar()
    
    def init_layout(self):
        fr_left = ttk.Frame(master=self)
        fr_left.pack(side='left',fill='both',padx=7,pady=7)
        
        fr_left_top = ttk.Frame(master=fr_left)
        fr_left_top.pack(side='top',fill='both',padx=3,pady=3)
        
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Tab name:')
        fr_left_top_left.pack(side='left',fill='both',padx=3,pady=3)
        
        ttk.Entry(master=fr_left_top_left,textvariable=self.name).pack(side='left',fill='both')
        
        ttk.Button(master=fr_left_top,text='update',command=self._on_update).pack(side='left',fill='both')
        
        fr_left_top = ttk.Frame(master=fr_left)
        fr_left_top.pack(side='top',fill='both',padx=3,pady=3)
        
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Antennas')
        fr_left_top_left.pack(side='left',fill='both',padx=3,pady=3)
        
        self.antenna_cbbx = ttk.Combobox(master=fr_left_top_left,state='readonly',values=[antenna.name for antenna in self.app.antennas])
        self.antenna_cbbx.pack(side='left',fill='both')
        if len(self.app.antennas)>0:
            if self.result.antenna is not None:
                self.antenna_cbbx.current(self.app.antennas.index(self.result.antenna))
            else:
                self.antenna_cbbx.current(0)
        
        fr_left_top = ttk.Frame(master=fr_left)
        fr_left_top.pack(side='top',fill='both',padx=3,pady=3)
        
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Plot')
        fr_left_top_left.pack(side='left',fill='both',padx=3,pady=3)
        
        cbbx = ttk.Combobox(master=fr_left_top_left,state='readonly',values=self.result.available_plots,textvariable=self.plot_variable,validate='all',validatecommand=self._on_plot_change)
        cbbx.pack(side='left',fill='both')
        cbbx.bind('<<ComboboxSelected>>',self._on_plot_change) 
        
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Field')
        fr_left_top_left.pack(side='left', fill='both',padx=3,pady=3)
        
        field_cbbx = ttk.Combobox(master=fr_left_top_left, state='readonly', textvariable=self.field_variable, values=self.result.available_fields)
        field_cbbx.pack(side='left',fill='both')
        
        fr_left_top = ttk.LabelFrame(master=fr_left, text='Options')
        fr_left_top.pack(side='top',fill='both')
        
        fr_left_top_left = ttk.Frame(master=fr_left_top)
        fr_left_top_left.pack(side='top',fill='both',padx=3,pady=3)
        
        ttk.Checkbutton(master=fr_left_top_left,text='in dB',variable=self.in_dB_variable).pack(side='left',fill='both')
        ttk.Checkbutton(master=fr_left_top_left,text='hide axis',variable=self.hide_axis_variable).pack(side='left',fill='both')
        ttk.Checkbutton(master=fr_left_top_left, textvariable=self.color_textvariable, variable=self.color_variable, command=self._on_color_cbt_change, onvalue='Color by magnitude', offvalue='Color by phase').pack(side='left', fill='both')
        
        fr_left_top_left = ttk.Frame(master=fr_left_top)
        fr_left_top_left.pack(side='top',fill='both',padx=3,pady=3)
        
        fr_left_top_left_left = ttk.LabelFrame(master=fr_left_top_left, text='Dynamic Scaling (dB)')
        fr_left_top_left_left.pack(side='left', fill='both',padx=3,pady=3)
        
        ttk.Entry(master=fr_left_top_left_left, textvariable=self.dynamic_scaling_dB_variable).pack(side='left', fill='both')
        
        # fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Analysis')
        # self.analysis_cbbx = ttk.Combobox(master=fr_left_top_left,state='readonly',values=[analysis.name for analysis in self.app.analyses])
        # self.analysis_cbbx.pack(side='left',fill='both')
        # if len(self.app.analyses)>0:
        #     if self.result.analysis is not None:
        #         self.analysis_cbbx.current(self.app.analyses.index(self.result.analysis))
        #     else:
        #         self.analysis_cbbx.current(0)
        
        # fr_left_top = ttk.Frame(master=fr_left)
        # fr_left_top.pack(side='top',fill='both')
        
        # fr_top_left = ttk.LabelFrame(master=fr_top, text='Projection')
        # fr_top_left.pack(side='left',fill='both')
        # ttk.Combobox(master=fr_top_left,state='readonly',values=['3d','2d'],textvariable=self.projection_variable).pack(side='left',fill='both')
        
        self.plot_frame = ttk.LabelFrame(master=self, text='Plot options')
        
        self.plot_2d_frame = ttk.LabelFrame(master=self.plot_frame, text='2d plot')
        self.plot_3d_frame = ttk.LabelFrame(master=self.plot_frame, text='3d plot')
        
        fr_left_top_left = ttk.LabelFrame(master=self.plot_2d_frame, text='Plot Plane')
        fr_left_top_left.pack(side='left',fill='both')
        fr_left_top_left_left = ttk.LabelFrame(master=fr_left_top_left, text='X')
        fr_left_top_left_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left_left,textvariable=self.reference_plane_X_variable).pack(side='left',fill='both')
        fr_left_top_left_left = ttk.LabelFrame(master=fr_left_top_left, text='Y')
        fr_left_top_left_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left_left,textvariable=self.reference_plane_Y_variable).pack(side='left',fill='both')
        fr_left_top_left_left = ttk.LabelFrame(master=fr_left_top_left, text='Z')
        fr_left_top_left_left.pack(side='left',fill='both')
        ttk.Entry(master=fr_left_top_left_left,textvariable=self.reference_plane_Z_variable).pack(side='left',fill='both')
        
        # fr_left = ttk.LabelFrame(master=self, text='Axes')
        # fr_left.pack(side='left',fill='both')
        # tk.Button(master=fr_left,text='add',command=self.on_add_axes).pack(side='top',fill='both')
        # tk.Button(master=fr_left,text='remove',command=self.on_remove_axes).pack(side='top',fill='both')
        # self.select_axes_lstbx = tk.Listbox(master=fr_left)
        # self.select_axes_lstbx.pack(side='top',fill='both')
        # for axes in self.result.axes:
        #     self.select_axes_lstbx.insert(tk.END, axes.name)
        
        # fr_left_top = ttk.Frame(master=fr_left)
        # fr_left_top.pack(side='top',fill='both')
        
        # self.edit_axes_frame = tk.Frame(master=self)
        
        if self.on_finish:
            fr_left_top = ttk.LabelFrame(master=fr_left,text='Finish')
            fr_left_top.pack(side='top',fill='both')
            ttk.Button(master=fr_left_top,text='Done',command=self._on_done).pack(side=tk.LEFT,fill=tk.BOTH)
            ttk.Button(master=fr_left_top,text='Cancel',command=self.on_cancel).pack(side=tk.LEFT,fill=tk.BOTH)
    
    def _on_update(self):
        self.result.name = self.name.get()
        self.result.set_antenna(self.app.antennas[self.antenna_cbbx.current()])
        # self.result.set_analysis(self.app.analyses[self.analysis_cbbx.current()])
        self.result.set_field(self.field_variable.get())
        self.result.set_plot(self.plot_variable.get())
        self.result.set_color(self.color_textvariable.get())
        
        self.result.reference_plane_X = self.reference_plane_X_variable.get()
        self.result.reference_plane_Y = self.reference_plane_Y_variable.get()
        self.result.reference_plane_Z = self.reference_plane_Z_variable.get()
        
        self.result.in_dB = self.in_dB_variable.get()==True
        self.result.dynamic_scaling_dB = self.dynamic_scaling_dB_variable.get()
        self.result.hide_axis = self.hide_axis_variable.get()==True
        
        self.result.ok = False
        self.result.update()
    
    def _on_done(self):
        self._on_update()
        self.on_done()
    
    def _on_color_cbt_change(self):
        self.color_textvariable.set(self.color_variable.get())
    
    def _on_plot_change(self, event=None):
        if self.current_plot_frame is not None:
            self.current_plot_frame.pack_forget()
        
        if self.plot_variable.get() in ['2d Graph','2d Contour','2d Polar Graph', '2d Polar Contour', '2d Polar Patch']:
            self.current_plot_frame = self.plot_2d_frame
            self.plot_2d_frame.pack(side='top',fill='both')
        elif self.plot_variable.get()==['3d Surface', '3d Polar Surface','3d Polar']:
            self.current_plot_frame = self.plot_3d_frame
            self.plot_3d_frame.pack(side='top',fill='both')
        
        self.plot_frame.pack(side='top',fill='both')
    
    # def _on_builtin_field_change(self, event=None):
    #     if self.current_field_frame is not None:
    #         self.current_field_frame.pack_forget()
        
    #     if self.custom_field_select_variable.get() == True:
    #         self.current_field_frame = self.custom_field_frame
    #     else:
    #         self.current_field_frame = self.builtin_field_fram
        
    #     self.current_field_frame.pack(side='top',fill='both')
    
    # def define_reference_plane(self):
    #     root = 
    
    # def on_axes_selection(self, event=None):
    #     selection = self.select_axes_lstbx.curselection()
    #     if len(selection)==0:
    #         return
    #     if self.current_editing_frame is not None:
    #         self.current_editing_frame._on_done()
    #         self.current_editing_frame.destroy()
    #         self.array.evaluate()
    #     self.edit_axes_frame.pack_forget()
    #     self.current_editing_axes = ([axes for axes in self.result.axes])[selection[0]]
    #     # self.current_editing_frame = AxesEditorFrame(axes=self.current_editing_axes,on_finish=False,master=self.edit_axes_frame)
    #     # self.current_editing_frame.pack(side='left',fill='both')
    #     self.edit_axes_frame.pack(side='left',fill='both')
    
    # def on_add_axes(self):
    #     root = tk.Toplevel()
    #     lbfr = ttk.LabelFrame(master=root,text='Projection')
    #     lbfr.pack(side='top',fill='both')
    #     values=['2d', '2d Polar', '3d','3d Polar']
    #     axes_cbbx = ttk.Combobox(master=lbfr,values=values,state='readonly')
    #     axes_cbbx.pack(side='top',fill='both')
    #     axes_cbbx.current(0)
    #     def on_done():
    #         self.result.add_axes(projection=values[axes_cbbx.current()])
    #         self.select_axes_lstbx.insert(tk.END, self.result.current_axes.name)
    #         root.destroy()
    #     def on_cancel():
    #         root.destroy()
    #     tk.Button(master=root,text='done',command=on_done).pack(side='top',fill='both')
    #     tk.Button(master=root,text='cancel',command=on_cancel).pack(side='top',fill='both')
    #     root.mainloop()
    
    # def on_remove_axes(self):
    #     selection = self.select_axes_lstbx.curselection()
    #     if len(selection)==0:
    #         return
    #     if self.current_editing_frame is not None:
    #         self.current_editing_frame._on_done()
    #         self.current_editing_frame.destroy()
    #     axes = ([axes for axes in self.result.axes])[selection[0]]
    #     self.result.axes.remove(axes)
    #     self.select_axes_lstbx.delete(0,tk.END)
    #     self.result.axes = [axes for axes in self.result.axes]
    #     for axes in self.result.axes:
    #         self.select_axes_lstbx.insert(tk.END, axes.name)