# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 17:34:44 2023

@author: 160047412
"""

import tkinter as tk
from tkinter import ttk

# from AxesEditorFrame import AxesEditorFrame
import Geometry


class ResultEditorFrame(ttk.Frame):
    def __init__(self,
                 app,
                 result,
                 on_finish=True,
                 on_done=None,
                 on_cancel=None,
                 master=None,
                 **kw):
        ttk.Frame.__init__(self, master=master, width=300, height=200, **kw)
        self.app = app
        self.result = result
        self.on_finish = on_finish
        self.on_done = on_done
        self.on_cancel = on_cancel

        self.current_plot_frame = None

        self.init_variables()
        self.init_layout()

        self._on_plot_change()
        # self._on_builtin_field_change()

        # self.select_axes_lstbx.bind('<<ListboxSelect>>',
        #                             self.on_axes_selection)

    def init_variables(self):
        self.name = tk.StringVar(value=self.result.name)
        self.projection_variable = tk.StringVar(value=self.result.projection)
        self.plot_variable = tk.StringVar(value=self.result.plot)
        self.field_variable = tk.StringVar(value=self.result.field)
        self.color_by_variable = tk.StringVar(value=self.result.color_by)
        self.color_by_textvariable = tk.StringVar(value=self.result.color_by)
        self.row_variable = tk.IntVar(value=self.result.row)
        self.column_variable = tk.IntVar(value=self.result.column)

        self.X_X_variable = tk.DoubleVar(
            value=self.result.reference_2d.x_axis.x)
        self.X_Y_variable = tk.DoubleVar(
            value=self.result.reference_2d.x_axis.y)
        self.X_Z_variable = tk.DoubleVar(
            value=self.result.reference_2d.x_axis.z)
        self.Z_X_variable = tk.DoubleVar(
            value=self.result.reference_2d.z_axis.x)
        self.Z_Y_variable = tk.DoubleVar(
            value=self.result.reference_2d.z_axis.y)
        self.Z_Z_variable = tk.DoubleVar(
            value=self.result.reference_2d.z_axis.z)

        self.in_dB_variable = tk.IntVar(value=self.result.in_dB)
        self.colorbar_dB_min_variable = tk.DoubleVar(
            value=self.result.colorbar_dB_min)
        self.visible_flag_variable = tk.IntVar(value=self.result.visible_flag)
        self.axis_flag_variable = tk.IntVar(value=self.result.axis_flag)
        self.grid_flag_variable = tk.IntVar(value=self.result.grid_flag)
        self.antialiased_variable = tk.IntVar(value=self.result.antialiased)
        self.add_colorbar_variable = tk.IntVar(value=self.result.add_colorbar)
        self.colorbar_dB_min_variable = tk.DoubleVar(value=self.result.colorbar_dB_min)
        self.colorbar_dB_max_variable = tk.DoubleVar(value=self.result.colorbar_dB_max)
        self.colorbar_min_variable = tk.DoubleVar(value=self.result.colorbar_min)
        self.colorbar_max_variable = tk.DoubleVar(value=self.result.colorbar_max)

        # self.edit_axes_frame_label = tk.StringVar()

    def init_layout(self):
        fr_left = ttk.Frame(master=self)
        fr_left.pack(side='left', fill='both', padx=7, pady=7)

        fr_left_top = ttk.Frame(master=fr_left)
        fr_left_top.pack(side='top', fill='both', padx=3, pady=3)

        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Tab name:')
        fr_left_top_left.pack(side='left', fill='both', padx=3, pady=3)

        ttk.Entry(master=fr_left_top_left, textvariable=self.name).pack(
            side='left', fill='both')

        ttk.Button(master=fr_left_top, text='update',
                   command=self._on_update).pack(side='left', fill='both')
    
        fr_left_top = ttk.LabelFrame(master=fr_left, text='Axes position:')
        fr_left_top.pack(side='top', fill='both', padx=3, pady=3)
        
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Row:')
        fr_left_top_left.pack(side='left', fill='both', padx=3, pady=3)
        ttk.Entry(master=fr_left_top_left, textvariable=self.row_variable).pack(
            side='left', fill='both')
        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Column:')
        fr_left_top_left.pack(side='left', fill='both', padx=3, pady=3)
        ttk.Entry(master=fr_left_top_left, textvariable=self.column_variable).pack(
            side='left', fill='both')
    
        # ttk.Button(master=fr_left_top, text='update',
        #             command=self._on_update).pack(side='left', fill='both')
        
        # fr_left_top_left_left = ttk.LabelFrame(master=fr_left_top_left, text='Row:')
        # fr_left_top_left.pack(side='left', fill='both', padx=3, pady=3)
        # ttk.Entry(master=fr_left_top_left_left, textvariable=self.row_variable).pack(
        #     side='left', fill='both')
        # fr_left_top_left_left = ttk.LabelFrame(master=fr_left_top_left, text='Column:')
        # fr_left_top_left.pack(side='left', fill='both', padx=3, pady=3)
        # ttk.Entry(master=fr_left_top_left_left, textvariable=self.column_variable).pack(
        #     side='left', fill='both')

        fr_left_top = ttk.Frame(master=fr_left)
        fr_left_top.pack(side='top', fill='both', padx=3, pady=3)

        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Antennas')
        fr_left_top_left.pack(side='left', fill='both', padx=3, pady=3)

        self.antenna_cbbx = ttk.Combobox(
            master=fr_left_top_left,
            state='readonly',
            values=[
                antenna.name
                for antenna
                in self.app.antennas])
        self.antenna_cbbx.pack(side='left', fill='both')
        if len(self.app.antennas) > 0:
            if self.result.antenna is not None:
                self.antenna_cbbx.current(
                    self.app.antennas.index(self.result.antenna))
            else:
                self.antenna_cbbx.current(0)

        fr_left_top = ttk.Frame(master=fr_left)
        fr_left_top.pack(side='top', fill='both', padx=3, pady=3)

        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Plot')
        fr_left_top_left.pack(side='left', fill='both', padx=3, pady=3)

        cbbx = ttk.Combobox(
            master=fr_left_top_left,
            state='readonly',
            values=self.result.available_plots,
            textvariable=self.plot_variable,
            validate='all',
            validatecommand=self._on_plot_change)
        cbbx.pack(side='left', fill='both')
        cbbx.bind('<<ComboboxSelected>>', self._on_plot_change)

        fr_left_top_left = ttk.LabelFrame(master=fr_left_top, text='Field')
        fr_left_top_left.pack(side='left', fill='both', padx=3, pady=3)

        field_cbbx = ttk.Combobox(
            master=fr_left_top_left,
            state='readonly',
            textvariable=self.field_variable,
            values=self.result.available_fields)
        field_cbbx.pack(side='left', fill='both')

        fr_left_top = ttk.LabelFrame(master=fr_left, text='Options')
        fr_left_top.pack(side='top', fill='both')

        fr_left_top_left = ttk.Frame(master=fr_left_top)
        fr_left_top_left.pack(side='left', fill='both', padx=3, pady=3)

        ttk.Checkbutton(
            master=fr_left_top_left, text='visible',
            variable=self.visible_flag_variable).pack(side='top', fill='both')
        ttk.Checkbutton(
            master=fr_left_top_left, text='axis',
            variable=self.axis_flag_variable).pack(side='top', fill='both')
        ttk.Checkbutton(
            master=fr_left_top_left, text='grid',
            variable=self.grid_flag_variable).pack(side='top', fill='both')
        ttk.Checkbutton(
            master=fr_left_top_left, text='in dB',
            variable=self.in_dB_variable).pack(side='top', fill='both')
        ttk.Checkbutton(
            master=fr_left_top_left, text='antialiased',
            variable=self.antialiased_variable).pack(side='top', fill='both')

        fr_left_top_left = ttk.Frame(master=fr_left_top)
        fr_left_top_left.pack(side='left', fill='both', padx=3, pady=3)

        ttk.Checkbutton(
            master=fr_left_top_left, textvariable=self.color_by_textvariable,
            variable=self.color_by_variable,
            command=self._on_color_cbt_change,
            onvalue='Color by magnitude',
            offvalue='Color by phase').pack(side='left', fill='both')

        fr_left_top_left = ttk.Frame(master=fr_left_top)
        fr_left_top_left.pack(side='top', fill='both', padx=3, pady=3)

        fr_left_top_left_left = ttk.LabelFrame(
            master=fr_left_top_left, text='Dynamic Scaling')
        fr_left_top_left_left.pack(side='left')
        
        fr_left_top_left_left_top = ttk.Frame(master=fr_left_top_left_left)
        ttk.Label(master=fr_left_top_left_left_top, text="min dB").pack(side='left')
        ttk.Entry(
            master=fr_left_top_left_left_top,
            textvariable=self.colorbar_dB_min_variable).pack(
            side='left', fill='both')
        fr_left_top_left_left_top.pack(side='top', fill='both', padx=3, pady=3)

        fr_left_top_left_left_top = ttk.Frame(master=fr_left_top_left_left)
        ttk.Label(master=fr_left_top_left_left_top, text="max dB").pack(side='left')
        ttk.Entry(
            master=fr_left_top_left_left_top,
            textvariable=self.colorbar_dB_max_variable).pack(
            side='left', fill='both')
        fr_left_top_left_left_top.pack(side='top', fill='both', padx=3, pady=3)
        
        fr_left_top_left_left_top = ttk.Frame(master=fr_left_top_left_left)
        ttk.Label(master=fr_left_top_left_left_top, text="min").pack(side='left')
        ttk.Entry(
            master=fr_left_top_left_left_top,
            textvariable=self.colorbar_min_variable).pack(
            side='left', fill='both')
        fr_left_top_left_left_top.pack(side='top', fill='both', padx=3, pady=3)

        fr_left_top_left_left_top = ttk.Frame(master=fr_left_top_left_left)
        ttk.Label(master=fr_left_top_left_left_top, text="max").pack(side='left')
        ttk.Entry(
            master=fr_left_top_left_left_top,
            textvariable=self.colorbar_max_variable).pack(
            side='left', fill='both')
        fr_left_top_left_left_top.pack(side='top', fill='both', padx=3, pady=3)

        self.plot_frame = ttk.LabelFrame(master=self, text='Plot options')

        self.plot_2d_frame = ttk.LabelFrame(
            master=self.plot_frame, text='2d plot')
        self.plot_3d_frame = ttk.LabelFrame(
            master=self.plot_frame, text='3d plot')

        fr_left_top_left = ttk.LabelFrame(
            master=self.plot_2d_frame, text='X Axis')
        fr_left_top_left.pack(side='top', fill='both')
        fr_left_top_left_left = ttk.LabelFrame(
            master=fr_left_top_left, text='X')
        fr_left_top_left_left.pack(side='left', fill='both')
        ttk.Entry(master=fr_left_top_left_left,
                  textvariable=self.X_X_variable).pack(
                      side='left', fill='both')
        fr_left_top_left_left = ttk.LabelFrame(
            master=fr_left_top_left, text='Y')
        fr_left_top_left_left.pack(side='left', fill='both')
        ttk.Entry(master=fr_left_top_left_left,
                  textvariable=self.X_Y_variable).pack(
                      side='left', fill='both')
        fr_left_top_left_left = ttk.LabelFrame(
            master=fr_left_top_left, text='Z')
        fr_left_top_left_left.pack(side='left', fill='both')
        ttk.Entry(master=fr_left_top_left_left,
                  textvariable=self.X_Z_variable).pack(
                      side='left', fill='both')

        fr_left_top_left = ttk.LabelFrame(
            master=self.plot_2d_frame, text='Z Plane')
        fr_left_top_left.pack(side='top', fill='both')
        fr_left_top_left_left = ttk.LabelFrame(
            master=fr_left_top_left, text='X')
        fr_left_top_left_left.pack(side='left', fill='both')
        ttk.Entry(master=fr_left_top_left_left,
                  textvariable=self.Z_X_variable).pack(
                      side='left', fill='both')
        fr_left_top_left_left = ttk.LabelFrame(
            master=fr_left_top_left, text='Y')
        fr_left_top_left_left.pack(side='left', fill='both')
        ttk.Entry(master=fr_left_top_left_left,
                  textvariable=self.Z_Y_variable).pack(
                      side='left', fill='both')
        fr_left_top_left_left = ttk.LabelFrame(
            master=fr_left_top_left, text='Z')
        fr_left_top_left_left.pack(side='left', fill='both')
        ttk.Entry(master=fr_left_top_left_left,
                  textvariable=self.Z_Z_variable).pack(
                      side='left', fill='both')

        if self.on_finish:
            fr_left_top = ttk.LabelFrame(master=fr_left, text='Finish')
            fr_left_top.pack(side='top', fill='both')
            ttk.Button(master=fr_left_top, text='Done',
                       command=self._on_done).pack(
                           side=tk.LEFT, fill=tk.BOTH)
            ttk.Button(master=fr_left_top, text='Cancel',
                       command=self.on_cancel).pack(side=tk.LEFT, fill=tk.BOTH)

    def _on_update(self):
        # self.result.ok = False
        # self.result.update()
        # if True:
        #     return
        self.result.name = self.name.get()
        self.result.set_antenna(self.app.antennas[self.antenna_cbbx.current()])
        self.result.set_field(self.field_variable.get())
        self.result.set_plot(self.plot_variable.get())
        self.result.set_color(self.color_by_textvariable.get())
        self.result.set_position(row=self.row_variable.get(), column=self.column_variable.get())

        x_axis = Geometry.Axis()
        z_axis = Geometry.Axis()

        x_axis.x = self.X_X_variable.get()
        x_axis.y = self.X_Y_variable.get()
        x_axis.z = self.X_Z_variable.get()

        z_axis.x = self.Z_X_variable.get()
        z_axis.y = self.Z_Y_variable.get()
        z_axis.z = self.Z_Z_variable.get()

        self.result.reference_2d = Geometry.ReferenceSystem(
            x_axis=x_axis, z_axis=z_axis)

        # print(self.visible_flag_variable.get())
        self.result.in_dB = self.in_dB_variable.get() == 1
        self.result.colorbar_dB_min = self.colorbar_dB_min_variable.get()
        self.result.visible_flag = self.visible_flag_variable.get() == 1
        self.result.axis_flag = self.axis_flag_variable.get() == 1
        self.result.grid_flag = self.grid_flag_variable.get() == 1
        self.result.add_colorbar = self.add_colorbar_variable.get() == 1
        self.result.colorbar_min = self.colorbar_min_variable.get()
        self.result.colorbar_max = self.colorbar_max_variable.get()

        self.result.ok = False
        self.result.update()

    def _on_done(self):
        self._on_update()
        self.on_done()

    def _on_color_cbt_change(self):
        self.color_by_textvariable.set(self.color_by_variable.get())

    def _on_plot_change(self, event=None):
        if self.current_plot_frame is not None:
            self.current_plot_frame.pack_forget()
            self.plot_frame.pack_forget()

        if self.plot_variable.get() in [
                '2d Graph',
                '2d Polar Graph',
                '2d Contour',
                '2d Polar Contour',
                '2d Polar Patch']:
            self.current_plot_frame = self.plot_2d_frame
            self.plot_2d_frame.pack(side='top', fill='both')
            self.plot_frame.pack(side='top', fill='both')
        elif self.plot_variable.get() == [
                '3d Surface',
                '3d Polar Surface',
                '3d Polar']:
            self.current_plot_frame = self.plot_3d_frame
            self.plot_3d_frame.pack(side='top', fill='both')
            self.plot_frame.pack(side='top', fill='both')
