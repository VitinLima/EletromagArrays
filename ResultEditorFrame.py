# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 17:34:44 2023

@author: 160047412
"""

import tkinter as tk
from tkinter import ttk

# from AxesEditorFrame import AxesEditorFrame

class ResultEditorFrame(ttk.Frame):
    def __init__(self,app,result,on_finish=True,on_done=None,on_cancel=None,master=None,**kw):
        ttk.Frame.__init__(self,master=master,width=300,height=200,**kw)
        self.app = app
        self.result = result
        self.on_finish=on_finish
        self.on_done=on_done
        self.on_cancel=on_cancel
        
        self.init_variables()
        self.init_layout()
        
        # self.select_axes_lstbx.bind('<<ListboxSelect>>',self.on_axes_selection)
    
    def init_variables(self):
        self.name = tk.StringVar(value=self.result.name)
        self.projection_variable = tk.StringVar(value=self.result.projection)
        self.plot_variable = tk.StringVar(value=self.result.plot)
        
        # self.edit_axes_frame_label = tk.StringVar()
    
    def init_layout(self):
        fr_left = ttk.Frame(master=self)
        fr_left.pack(side='left',fill='both')
        
        fr_left_top = ttk.LabelFrame(master=fr_left, text='Tab name:')
        fr_left_top.pack(side='top',fill='both')
        ttk.Entry(master=fr_left_top,textvariable=self.name).pack(side='left',fill='both')
        
        ttk.Button(master=fr_left_top,text='update',command=self._on_update).pack(side='left',fill='both')
        
        fr_left_top = ttk.Frame(master=fr_left)
        fr_left_top.pack(side='top',fill='both')
        
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Antennas')
        fr_left_top_left.pack(side='left',fill='both')
        self.antenna_cbbx = ttk.Combobox(master=fr_left_top_left,state='readonly',values=[antenna.name for antenna in self.app.antennas])
        self.antenna_cbbx.pack(side='left',fill='both')
        if len(self.app.antennas)>0:
            if self.result.antenna is not None:
                self.antenna_cbbx.current(self.app.antennas.index(self.result.antenna))
            else:
                self.antenna_cbbx.current(0)
        
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Analysis')
        fr_left_top_left.pack(side='left',fill='both')
        self.analysis_cbbx = ttk.Combobox(master=fr_left_top_left,state='readonly',values=[analysis.name for analysis in self.app.analyses])
        self.analysis_cbbx.pack(side='left',fill='both')
        if len(self.app.analyses)>0:
            if self.result.analysis is not None:
                self.analysis_cbbx.current(self.app.analyses.index(self.result.analysis))
            else:
                self.analysis_cbbx.current(0)
        
        fr_left_top = ttk.Frame(master=fr_left)
        fr_left_top.pack(side='top',fill='both')
        
        # fr_top_left = ttk.LabelFrame(master=fr_top, text='Projection')
        # fr_top_left.pack(side='left',fill='both')
        # ttk.Combobox(master=fr_top_left,state='readonly',values=['3d','2d'],textvariable=self.projection_variable).pack(side='left',fill='both')
        
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Plot')
        fr_left_top_left.pack(side='left',fill='both')
        ttk.Combobox(master=fr_left_top_left,state='readonly',values=self.result.available_plots,textvariable=self.plot_variable).pack(side='left',fill='both')
        # ttk.Button(master=fr_left_top_left,text='Cross polarization',command=self.on_define_cross_polarization).pack(side='left',fill='both')
        
        if self.on_finish:
            fr_left_top = ttk.LabelFrame(master=fr_left,text='Finish')
            fr_left_top.pack(side='top',fill='both')
            ttk.Button(master=fr_left_top,text='Done',command=self._on_done).pack(side=tk.LEFT,fill=tk.BOTH)
            ttk.Button(master=fr_left_top,text='Cancel',command=self.on_cancel).pack(side=tk.LEFT,fill=tk.BOTH)
        
        # fr_left = ttk.LabelFrame(master=self, text='Axes')
        # fr_left.pack(side='left',fill='both')
        # tk.Button(master=fr_left,text='add',command=self.on_add_axes).pack(side='top',fill='both')
        # tk.Button(master=fr_left,text='remove',command=self.on_remove_axes).pack(side='top',fill='both')
        # self.select_axes_lstbx = tk.Listbox(master=fr_left)
        # self.select_axes_lstbx.pack(side='top',fill='both')
        # for axes in self.result.axes:
        #     self.select_axes_lstbx.insert(tk.END, axes.name)
        
        # self.edit_axes_frame = tk.Frame(master=self)
    
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
    
    # def define_cross_polarization(self):
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