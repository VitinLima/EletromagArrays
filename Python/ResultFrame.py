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
    def __init__(self,master=None,name='New tab',iy=1,**kw):
        tk.Frame.__init__(self, master, width=300, height=200, **kw)
        self.name=name
        self.iy=iy
        
        self.ix = 1
        self.subplot_spaces = [None]
        
        self.listeners = []
        self.ok = True
        
        bg_color = 'white'
        # bg_color = '#505050'
        self.figure = plt.Figure(figsize=(5, 4), dpi=100, facecolor=bg_color)
        self.axes_dict = dict()
        self.results = []
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)  # A tk.DrawingArea.
        self.canvas.draw()
        
        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        
        self.canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        self.canvas.mpl_connect("key_press_event", key_press_handler)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def notify(self, caller, event):
        self.ok = False
        self.mark_update('"' + str(caller) +'" called notify with event "' + event + '"')
    
    def mark_update(self, event):
        for l in self.listeners:
            print(str(self) + ' notifying ' + str(l) + ' for ' + event)
            l.notify(self)
    
    def determine_subplots_layout(self):
        # integer divided by 2 terminates either in 0 or 0.5, so round works fine here
        max_position = max([result.preferred_position[-1] if str(type(result.preferred_position))=="<class 'tuple'>" else result.preferred_position for result in self.results if result.preferred_position is not None] + [len(self.results)])
        ix = max_position/self.iy
        if ix - int(ix) > 0:
            self.ix = int(self.ix) + 1
        else:
            self.ix = int(ix)
        self.subplot_spaces = [None for i in range(self.ix*self.iy)]
    
    def add_result(self, result):
        self.results.append(result)
        result.listeners.append(self)
        self.ok = False
        if len(self.results)>len(self.subplot_spaces):
            self.determine_subplots_layout()
    
    def remove_result(self, result):
        self.results.remove(result)
        result.listeners.remove(self)
        self.ok = False
    
    def request_axes(self, requester, projection, preferred_position=None, **kw):
        # if requester in self.axes_dict.keys():
        #     self.axes_dict[requester].remove()
        if preferred_position==None:
            position = [i for i in range(len(self.subplot_spaces)) if self.subplot_spaces[i]==None][0]+1
        elif str(type(preferred_position))=="<class 'tuple'>":
            flag = True
            for i in preferred_position:
                if self.subplot_spaces[i-1] is not None:
                    flag = False
            if flag:
                position = preferred_position
            else:
                position = [i for i in range(len(self.subplot_spaces)) if self.subplot_spaces[i]==None][0]+1
        else:
            if self.subplot_spaces[preferred_position-1]==None:
                position = preferred_position
            else:
                position = [i for i in range(preferred_position-1,len(self.subplot_spaces)) if self.subplot_spaces[i]==None][0]+1
        self.axes_dict[requester] = self.figure.add_subplot(self.ix,self.iy,position,projection=projection,**kw)
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
        
        self.determine_subplots_layout()
        
        self.draw_background()
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