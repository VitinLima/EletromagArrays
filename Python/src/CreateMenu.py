# -*- coding: utf-8 -*-
""" tk_ToolTip_class101.py
gives a Tkinter widget a tooltip as the mouse is above the widget
tested with Python27 and Python34  by  vegaseat  09sep2014
www.daniweb.com/programming/software-development/code/
    484591/a-tooltip-class-for-tkinter

Modified to include a delay time by Victor Zaccardo, 25mar16
Modified to include a dynamic tooltip for ttk.combobox by Vítor Lima,
    11dec2022
Modified to create a popup menu by Vítor Lima, 08mar2023
"""

try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk


class CreateMenu(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        # self.widget.bind("<Enter>", self.enter)
        # self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.widget.bind("<Button-3>", self.showtip)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event):
        x = event.x
        y = event.y
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        if self.tw:
            self.tw.destroy()
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        if self.widget.create_drop_menu(self.tw, event) is False:
            self.hidetip()

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
