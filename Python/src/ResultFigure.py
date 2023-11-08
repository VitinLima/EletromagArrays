# -*- coding: utf-8 -*-
"""
Created on Sat May 13 18:10:10 2023

@author: 160047412
"""

import matplotlib.pyplot as plt


class ResultFigure:
    def __init__(self, columns=1, rows=1):
        self.columns = columns
        self.rows = rows

        self.listeners = []
        self.ok = True

        bg_color = 'white'
        # bg_color = '#505050'
        self.figure = plt.figure(figsize=(5, 4), dpi=100,
                                 facecolor=bg_color)
        self.axes_dict = dict()
        self.results = []

    def notify(self, caller, event):
        self.ok = False
        self.mark_update('"' + str(caller) +
                         '" called notify with event "' + event + '"')

    def mark_update(self, event):
        for l in self.listeners:
            print(str(self) + 
                  ' notifying ' + str(l) + ' for ' + event)
            l.notify(self)

    def add_result(self, result):
        self.results.append(result)
        result.listeners.append(self)
        self.ok = False

    def remove_result(self, result):
        self.results.remove(result)
        result.listeners.remove(self)
        self.ok = False

    def request_axes(self, requester, projection,
                     position=None, column=None, row=None, **kw):
        if position is None:
            position = (row - 1)*self.columns + column
        self.axes_dict[requester] = self.figure.add_subplot(
            self.rows, self.columns, position, projection=projection)
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

        self.draw_background()
        for result in self.results:
            result.draw()

    def undraw(self):
        self.figure.clear()

    def draw_background(self):
        pass
        # self.background_axes = self.figure.axes(rect=(0,0,1,1))
        # self.background_axes.set_facecolor('#505050')
