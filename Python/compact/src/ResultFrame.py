# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:19:19 2023

@author: 160047412
"""

import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler


class ResultFrame(tk.Frame):
    def __init__(self, master=None, name='New tab',
                 columns=1, rows=1, **kw):
        tk.Frame.__init__(self,
                          master,
                          width=300, height=200,
                          **kw)
        self.name = name
        self.columns = columns
        self.rows = rows
        self.subplot_spaces = [None]

        self.listeners = []
        self.ok = True

        bg_color = 'white'
        # bg_color = '#505050'
        self.figure = plt.Figure(figsize=(5, 4),
                                 dpi=100,
                                 facecolor=bg_color)
        self.axes_dict = dict()
        self.results = []

        # A tk.DrawingArea.
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()

        # pack_toolbar=False will make it easier to use a
        # layout manager later on.
        self.toolbar = NavigationToolbar2Tk(self.canvas,
                                            self,
                                            pack_toolbar=False)
        self.toolbar.update()

        self.canvas.mpl_connect(
            "key_press_event",
            lambda event: print(f"you pressed {event.key}"))
        self.canvas.mpl_connect("key_press_event",
                                key_press_handler)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP,
                                         fill=tk.BOTH,
                                         expand=True)

    def notify(self, caller, event):
        self.ok = False
        self.mark_update('"' + str(caller) +
                         '" called notify with event "' +
                         event + '"')

    def mark_update(self, event):
        for l in self.listeners:
            print(str(self) + ' notifying ' + str(l) + ' for ' +
                  event)
            l.notify(self)

    def add_result(self, result):
        self.results.append(result)
        # result.listeners.append(self)
        self.ok = False
        # if len(self.results)>len(self.subplot_spaces):
        #     self.determine_subplots_layout()

    # def remove_result(self, result):
    #     self.results.remove(result)
    #     result.listeners.remove(self)
    #     self.ok = False

    def request_axes(self, requester, projection,
                     position=None, column=None, row=None, **kw):
        if position is None:
            position = (row - 1)*self.columns + column
        self.axes_dict[requester] = \
            self.figure.add_subplot(
                self.rows, self.columns,
                position, projection=projection, **kw)
        return self.axes_dict[requester]

    def request_axes_delete(self, requester):
        if requester in self.axes_dict.get_keys():
            self.axes_dict[requester].remove()
            self.axes_dict.pop(requester)

    def request_repaint(self):
        self.canvas_flag = True

    def update(self):
        if self.ok:
            return

        self.draw()

        self.ok = True
        self.mark_update('Draw')

    def draw(self):
        self.undraw()

        # self.draw_background()
        for result in self.results:
            result.draw()

        self.canvas.draw()
        # self.configure(width=300*self.iy, height=200*self.ix)

    def undraw(self):
        self.figure.clear()

    def draw_background(self):
        pass
        # self.background_axes = self.figure.axes(rect=(0,0,1,1))
        # self.background_axes.set_facecolor('#505050')
