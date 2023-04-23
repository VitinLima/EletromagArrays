# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 19:01:06 2023

@author: 160047412
"""

import tkinter as tk
from tkinter import ttk
import pickle

import CreateMenu
# from ResultEditorFrame import ResultEditorFrame

import Antenna,AntennaEditorFrame
import Array,ArrayEditorFrame
import Analysis,AnalysisEditorFrame
import Optimization,OptimizationEditorFrame
import ResultFrame,ResultTabEditorFrame
# from Result import Result

class ProjectTreeview(ttk.Treeview):
    def __init__(self, app, master=None, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        self.app = app
        
        self.bind('<<TreeviewSelect>>', self.tree_view_select)
        
        self.antennas = dict()
        self.analyses = dict()
        # self.optims = dict()
        self.result_tabs = dict()
        
        self.antennas_iid = self.insert('', tk.END, text='Antennas')
        self.analyses_iid = self.insert('', tk.END, text='Analyses')
        self.optims_iid = self.insert('', tk.END, text='Optimizations')
        self.result_tabs_iid = self.insert('', tk.END, text='Tabs')
        
        self.object_iid_map = dict()
        self.iid_object_map = dict()
        
        self.menu = CreateMenu.CreateMenu(self)
    
    def tree_view_select(self, event):
        pass
        # print(event)
        # print(self.selection())
    
    def create_drop_menu(self, tw, event):
        self.selection = self.identify_row(event.y)
        if self.selection == '':
            return False
        
        self.obj = None
        if self.selection == self.antennas_iid:
            self.antennas_menu(tw)
        elif self.selection == self.analyses_iid:
            self.analyses_menu(tw)
        elif self.selection == self.optims_iid:
            self.optims_menu(tw)
        elif self.selection == self.result_tabs_iid:
            self.result_tabs_menu(tw)
        else:
            self.obj = self.iid_object_map[self.selection]
            obj_type = str(type(self.obj))
            if obj_type=="<class 'Antenna.Antenna'>":
                self.antenna_menu(tw)
            elif obj_type=="<class 'Array.Array'>":
                self.array_menu(tw)
            elif obj_type=="<class 'Analysis.Analysis'>":
                self.analysis_menu(tw)
            elif obj_type=="<class 'Optimization.Optimization'>":
                self.optim_menu(tw)
            elif obj_type=="<class 'ResultFrame.ResultFrame'>":
                self.result_tab_menu(tw)
            elif obj_type=="<class 'Result.Result'>":
                self.result_menu(tw)
            else:
                print(obj_type)
                return False
        return True
    
    def antennas_menu(self, tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Antennas', justify='left',
                 relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='new antenna',command=self.on_antenna_ppp).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='new array',command=self.on_array_ppp).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='load antenna',command=self.on_load_antenna).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='update all',command=self.on_update_all_antennas).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)
    
    def analyses_menu(self, tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Analysis', justify='left',
                  relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='new analysis',command=self.on_analysis_ppp).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)
    
    def optims_menu(self, tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Optimization', justify='left',
                  relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='new optimization',command=self.on_optim_ppp).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)
    
    def result_tabs_menu(self, tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Result tabs', justify='left',
                  relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='new tab',command=self.on_result_tab_ppp).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='update all',command=self.on_update_all_tabs).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)
    
    def antenna_menu(self, tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Antenna', justify='left',
                  relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='edit',command=self.on_antenna_ppp).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='update',command=self.on_update_antenna).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='save',command=self.on_save_antenna).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='delete',command=self.on_delete_obj).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)
    
    def array_menu(self, tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Array', justify='left',
                  relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='edit',command=self.on_array_ppp).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='update',command=self.on_update_antenna).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='delete',command=self.on_delete_obj).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)
    
    def analysis_menu(self, tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Analysis', justify='left',
                  relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='edit',command=self.on_analysis_ppp).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='delete',command=self.on_delete_obj).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)
    
    def optim_menu(self, tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Optimization', justify='left',
                  relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='edit',command=self.on_optim_ppp).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='run',command=self.on_run_optim).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='delete',command=self.on_delete_obj).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)
    
    def result_tab_menu(self,tw):
        new_menu = tk.Frame(master=tw)
        tk.Label(master=new_menu, text='Results', justify='left',
                  relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='edit',command=self.on_result_tab_ppp).pack(ipadx=1,fill=tk.BOTH)
        # tk.Button(master=new_menu,text='new result',command=self.on_result_ppp).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='update',command=self.on_update_all_results).pack(ipadx=1,fill=tk.BOTH)
        tk.Button(master=new_menu,text='delete',command=self.on_delete_obj).pack(ipadx=1,fill=tk.BOTH)
        new_menu.pack(ipadx=1)
    
    # def result_menu(self,tw):
    #     new_menu = tk.Frame(master=tw)
    #     tk.Label(master=new_menu, text='Results', justify='left',
    #               relief='solid', borderwidth=0).pack(ipadx=1,fill=tk.BOTH)
    #     tk.Button(master=new_menu,text='edit',command=self.on_result_ppp).pack(ipadx=1,fill=tk.BOTH)
    #     tk.Button(master=new_menu,text='update',command=self.on_update_result).pack(ipadx=1,fill=tk.BOTH)
    #     tk.Button(master=new_menu,text='delete',command=self.on_delete_obj).pack(ipadx=1,fill=tk.BOTH)
    #     new_menu.pack(ipadx=1)
    
    def on_antenna_ppp(self):
        self.menu.hidetip()
        root=tk.Toplevel()
        if self.obj is None:
            antenna = Antenna.Antenna(constants=self.app.constants)
            editing = False
        else:
            antenna = self.obj
            editing = True
        def on_done():
            if not editing:
                self.app.add_antenna(antenna)
            else:
                self.item(self.selection,text=antenna.name)
            self.item(self.antennas_iid,open=True)
            root.destroy()
        def on_cancel():
            root.destroy()
        AntennaEditorFrame.AntennaEditorFrame(antenna=antenna,master=root,on_done=on_done,on_cancel=on_cancel).pack()
        root.mainloop()
    
    def on_load_antenna(self):
        file_path = tk.filedialog.askopenfilename()
        if file_path == '':
            return
        with open(file_path, mode='rb') as f:
            antenna = pickle.load(f)
            if str(type(antenna)) == "<class 'Antenna.Antenna'>":
                self.app.add_antenna(antenna)
                self.item(self.antennas_iid,open=True)
            elif str(type(antenna)) == "<class 'Array.Array'>":
                self.app.add_antenna(antenna)
                self.item(self.antennas_iid,open=True)
    
    def on_save_antenna(self):
        with tk.filedialog.asksaveasfile(mode='wb') as f:
            antenna = self.obj
            pickle.dump(antenna, f)
    
    def on_array_ppp(self):
        self.menu.hidetip()
        root=tk.Toplevel()
        if self.obj is None:
            array = Array.Array(constants=self.app.constants)
            editing = False
        else:
            array = self.obj
            editing = True
        def on_done():
            if not editing:
                self.app.add_antenna(array)
            else:
                self.item(self.selection,text=array.name)
            self.item(self.antennas_iid,open=True)
            root.destroy()
        def on_cancel():
            root.destroy()
        ArrayEditorFrame.ArrayEditorFrame(array=array,app=self.app,master=root,on_done=on_done,on_cancel=on_cancel).pack()
        root.mainloop()
    
    def on_analysis_ppp(self):
        self.menu.hidetip()
        root=tk.Toplevel()
        if self.obj is None:
            analysis = Analysis.Analysis()
            editing = False
        else:
            analysis = self.obj
            editing = True
        def on_done():
            if not editing:
                self.app.add_analysis(analysis)
            else:
                self.item(self.selection,text=analysis.name)
            self.item(self.analyses_iid,open=True)
            root.destroy()
        def on_cancel():
            root.destroy()
        AnalysisEditorFrame.AnalysisEditorFrame(analysis=analysis,master=root,on_done=on_done,on_cancel=on_cancel).pack()
        root.mainloop()
    
    def on_optim_ppp(self):
        self.menu.hidetip()
        root=tk.Toplevel()
        if self.obj is None:
            optim = Optimization.Optimization()
            editing = False
        else:
            optim = self.obj
            editing = True
        def on_done():
            if not editing:
                self.app.add_optim(optim)
            else:
                self.item(self.selection,text=optim.name)
            self.item(self.optims_iid,open=True)
            root.destroy()
        def on_cancel():
            root.destroy()
        OptimizationEditorFrame.OptimizationEditorFrame(optim=optim,app=self.app,master=root,on_done=on_done,on_cancel=on_cancel).pack()
        root.mainloop()
    
    def on_result_tab_ppp(self):
        self.menu.hidetip()
        root=tk.Toplevel()
        if self.obj is None:
            result_tab = ResultFrame.ResultFrame(master=self.app.tabs)
            editing = False
        else:
            result_tab = self.obj
            editing = True
        def on_done():
            if not editing:
                self.app.add_result_tab(result_tab)
            else:
                self.item(self.selection,text=result_tab.name)
                self.app.tabs.add(result_tab,text=result_tab.name)
            self.item(self.result_tabs_iid,open=True)
            root.destroy()
        def on_cancel():
            if not editing:
                result_tab.destroy()
            root.destroy()
        ResultTabEditorFrame.ResultTabEditorFrame(app=self.app,result_tab=result_tab,master=root,on_done=on_done,on_cancel=on_cancel).pack()
        root.mainloop()
    
    # def on_result_ppp(self):
    #     self.menu.hidetip()
    #     root=tk.Toplevel()
    #     if type(self.obj) is ResultFrame:
    #         result = Result()
    #         editing = False
    #     else:
    #         result = self.obj
    #         editing = True
    #     def on_done():
    #         if not editing:
    #             self.app.add_result(self.obj, result)
    #         self.item(self.result_tabs_iid,open=True)
    #         root.destroy()
    #     def on_cancel():
    #         root.destroy()
    #     ResultEditorFrame(result=result,app=self.app,master=root,on_done=on_done,on_cancel=on_cancel).pack()
    #     root.mainloop()
    
    def on_delete_obj(self):
        self.menu.hidetip()
        obj_type = str(type(self.obj))
        if obj_type=="<class 'Package.Antenna.Antenna.Antenna'>":
            self.app.antennas.remove(self.obj)
            self.delete_antenna(self.obj)
        elif obj_type=="<class 'Package.Array.Array.Array'>":
            self.app.antennas.remove(self.obj)
            self.delete_antenna(self.obj)
        elif obj_type=="<class 'Package.Analysis.Analysis.Analysis'>":
            self.app.analyses.remove(self.obj)
            self.delete_analysis(self.obj)
        elif obj_type=="<class 'Package.Optimization.Optimization.Optimization'>":
            self.app.optims.remove(self.obj)
            self.delete_optim(self.obj)
        elif obj_type=="<class 'Package.Results.ResultFrame.ResultFrame'>":
            self.app.tabs.forget(self.obj)
            self.delete_result_tab(self.obj)
        # elif obj_type=="<class 'Result.Result'>":
        #     result_tab = self.iid_object_map[self.parent(self.selection)]
        #     self.delete_result(result_tab, self.obj)
    
    def add_antenna(self, antenna):
        iid = self.insert(self.antennas_iid, tk.END, text=antenna.name)
        self.iid_object_map[iid] = antenna
        self.object_iid_map[antenna] = iid
    
    def add_analysis(self, analysis):
        iid = self.insert(self.analyses_iid, tk.END, text=analysis.name)
        self.iid_object_map[iid] = analysis
        self.object_iid_map[analysis] = iid
    
    def add_optim(self, optim):
        iid = self.insert(self.optims_iid, tk.END, text=optim.name)
        self.iid_object_map[iid] = optim
        self.object_iid_map[optim] = iid
    
    def add_result_tab(self, result_tab):
        iid = self.insert(self.result_tabs_iid, tk.END, text=result_tab.name)
        self.iid_object_map[iid] = result_tab
        self.object_iid_map[result_tab] = iid
        # for result in result_tab.results:
        #     result_iid = self.insert(iid, tk.END, text=result.name)
        #     self.iid_object_map[result_iid] = result
        #     self.object_iid_map[result] = result_iid
    
    def add_result(self, result_tab, result):
        result_tab.add_result(result)
        result.axes = result_tab.current_axes
        result.update()
        
        result_tab_iid = self.object_iid_map[result_tab]
        result_iid = self.insert(result_tab_iid, tk.END, text=result.name)
        self.iid_object_map[result_iid] = result
        self.object_iid_map[result] = result_iid
    
    def delete_antenna(self, antenna):
        iid = self.object_iid_map[antenna]
        self.object_iid_map.pop(antenna)
        self.iid_object_map.pop(iid)
        self.delete(iid)
    
    def delete_analysis(self, analysis):
        iid = self.object_iid_map[analysis]
        self.object_iid_map.pop(analysis)
        self.iid_object_map.pop(iid)
        self.delete(iid)
    
    def delete_optim(self, optim):
        iid = self.object_iid_map[optim]
        self.object_iid_map.pop(optim)
        self.iid_object_map.pop(iid)
        self.delete(iid)
    
    def delete_result_tab(self, result_tab):
        iid = self.object_iid_map[result_tab]
        # for result in result_tab.results:
        #     self.delete_result(result_tab, result)
        self.object_iid_map.pop(result_tab)
        self.iid_object_map.pop(iid)
        self.delete(iid)
    
    # def delete_result(self, result_tab, result):
    #     self.app.result_tabs.remove(result_tab)
    #     result.undraw()
    #     result_tab.results.remove(result)
        
    #     iid = self.object_iid_map[result]
    #     self.object_iid_map.pop(result)
    #     self.iid_object_map.pop(iid)
    #     self.delete(iid)
    
    def on_update_antenna(self):
        self.menu.hidetip()
        self.obj.evaluate()
    
    def on_update_result(self):
        self.menu.hidetip()
        self.obj.update()
    
    def on_update_all_antennas(self):
        self.menu.hidetip()
        for antenna in self.app.antennas:
            antenna.evaluate()
    
    def on_update_all_tabs(self):
        self.menu.hidetip()
        for tab in self.app.result_tabs:
            # for result in tab.results:
            #     result.update()
            tab.canvas.draw()
    
    def on_update_all_results(self):
        self.menu.hidetip()
        # for result in self.obj.results:
        #     result.update()
    
    def on_run_optim(self):
        self.obj.run()