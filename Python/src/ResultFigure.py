# -*- coding: utf-8 -*-
"""
Created on Sat May 13 18:10:10 2023

@author: 160047412
"""

import matplotlib.pyplot as plt

class ResultFigure:
    def __init__(self,columns=1,rows=1):
        self.columns=columns
        self.rows=rows
        
        self.listeners = []
        self.ok = True
        
        bg_color = 'white'
        # bg_color = '#505050'
        self.figure = plt.figure(figsize=(5, 4), dpi=100, facecolor=bg_color)
        self.axes_dict = dict()
        self.results = []
    
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
        # if len(self.results)>len(self.subplot_spaces):
        #     self.determine_subplots_layout()
    
    def remove_result(self, result):
        self.results.remove(result)
        result.listeners.remove(self)
        self.ok = False
    
    def request_axes(self, requester, projection, column=None,row=None, **kw):
        position = (row - 1)*self.columns + column
        self.axes_dict[requester] = self.figure.add_subplot(self.rows,self.columns,position,projection=projection,**kw)
        # if requester in self.axes_dict.keys():
        #     self.axes_dict[requester].remove()
        # if preferred_position==None:
        #     position = [i for i in range(len(self.subplot_spaces)) if self.subplot_spaces[i]==None][0]+1
        # elif str(type(preferred_position))=="<class 'tuple'>":
        #     flag = True
        #     for i in preferred_position:
        #         if self.subplot_spaces[i-1] is not None:
        #             flag = False
        #     if flag:
        #         position = preferred_position
        #     else:
        #         position = [i for i in range(len(self.subplot_spaces)) if self.subplot_spaces[i]==None][0]+1
        # else:
        #     if self.subplot_spaces[preferred_position-1]==None:
        #         position = preferred_position
        #     else:
        #         position = [i for i in range(preferred_position-1,len(self.subplot_spaces)) if self.subplot_spaces[i]==None][0]+1
        # self.axes_dict[requester] = self.figure.add_subplot(self.ix,self.iy,position,projection=projection,**kw)
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
        
        # self.figure.show()
        # self.canvas.draw()
        # self.configure(width=300*self.iy, height=200*self.ix)
    
    def undraw(self):
        self.figure.clear()
    
    def draw_background(self):
        pass
        # self.background_axes = self.figure.axes(rect=(0,0,1,1))
        # self.background_axes.set_facecolor('#505050')