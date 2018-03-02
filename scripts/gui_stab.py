#!/usr/bin/env python

import tkinter as tk
import json

class ConfigGUI:
    def __init__(self, master):
        self.master = master
        master.title("Configure Study")

        # Create main containers
        self.genframe = tk.LabelFrame(master,text='General Info',width=450, height=50, pady=3)
        self.funcframe = tk.LabelFrame(master,text='Functional',width=300, height=40, padx=3, pady=3)
        self.anatframe = tk.LabelFrame(master,text='Structural',width=300, height=40, padx=3, pady=3)
        self.dtiframe = tk.LabelFrame(master,text='DTI',width=300, height=40, padx=3, pady=3)
        self.spectframe = tk.LabelFrame(master,text='Spectroscopy',width=150, height=40, padx=3, pady=3)

        # Lay out the containers
        master.grid_rowconfigure(1, weight=10)
        master.grid_columnconfigure(0, weight=1)

        self.genframe.grid(row=0, sticky="ew")
        self.funcframe.grid(row=1, sticky="ew")
        self.anatframe.grid(row=2, sticky="ew")
        self.dtiframe.grid(row=3, sticky="ew")

        # General frame widgets
        self.label_study = tk.Label(self.genframe, text="Study name:")
        self.text_study = tk.Text(self.genframe,height=1,width=20)

        self.label_study.grid(row=0)
        self.text_study.grid(row=0,column=1)

        self.label_subjcode = tk.Label(self.genframe, text="Subject prefix:")
        self.label_subjcode.grid(row=0,column=4)

        self.text_subjcode = tk.Text(self.genframe,height=1,width=20)
        self.text_subjcode.grid(row=0,column=5)

        # Functional frame widgets
        self.func = []
        self.functask()

        # Anatomy frame widgets
        self.anat = []
        self.anatrun()

        # DTI frame widgets
        self.dti = []
        self.dtiseries()

        self.close_button = tk.Button(master, text="Save and Quit", command=self.save_and_quit)
        self.close_button.grid(row=4,sticky='e')

    def save_and_quit(self):

        d = {}
        d['func'] = {}
        d['anat'] = {}
        d['dti'] = {}
        d['spectro'] = {}

        for f in self.func:
            task_name = self.gettextentry(f['text_func'])
            if not task_name:
                continue

            d['func'][task_name] = {}

            num_runs = self.gettextentry(f['text_func_nruns'])

            # this could probably be more elegant
            if f['is_epi'].get():
                acqtype = 'epi'
            elif f['is_spiral'].get():
                acqtype = 'spiral'
            elif f['is_multiband'].get():
                acqtype = 'multiband'

            d['func'][task_name]['num_runs'] = num_runs
            d['func'][task_name]['acq_type'] = acqtype

        for a in self.anat:
            series_type = self.gettextentry(a['text_anat'])

            if not series_type:
                continue

            series_name = self.gettextentry(a['text_anat_name'])

            if series_name:
                series_fullname = series_type + '_' + series_name
            else:
                series_fullname = series_type

            d['anat'][series_fullname] = {}

        print(d)

        # Write the json

        # Quit
        self.master.quit()

    def dtiseries(self):

        d = {}
        num_existing = len(self.dti)
        this_row = num_existing

        tk.Label(self.dtiframe,text="Series name: DTI_").grid(row=this_row)

        text_dti = tk.Text(self.dtiframe,height=1,width=15)
        text_dti.grid(row=this_row,column=1)
        d['text_dti'] = text_dti

        # List select for acq type (TO DO: break out into own function)
        mb_acq=  tk.Menubutton ( self.dtiframe, text="Acquisition Type", relief=tk.RAISED )
        mb_acq.grid(row=this_row,column=2)
        mb_acq.menu =  tk.Menu ( mb_acq, tearoff = 0 )
        mb_acq["menu"] =  mb_acq.menu

        epiVar = tk.IntVar()
        multibandVar = tk.IntVar()
        spiralVar = tk.IntVar()

        mb_acq.menu.add_checkbutton ( label="EPI",variable=epiVar ,command= lambda: self.optText(mb_acq,'EPI'))
        mb_acq.menu.add_checkbutton ( label="Multiband",variable=multibandVar, command= lambda: self.optText(mb_acq,'Multiband'))

        d['mb_acqtype'] = mb_acq


        varFM = tk.IntVar()
        self.dti_cbx_fm = tk.Checkbutton(self.dtiframe, text="Has Fieldmap", variable=varFM).grid(row=this_row,column=3)

        self.dti.append(d)

    def optText(self,wid,str_display):

        # Select box
        wid.configure(text=str_display)

        if str_display.lower() == 'multiband':
            p = wid.winfo_parent()
            pn = wid._nametowidget(p)
            #print(wid.master)

            parent_name = wid.winfo_parent()
            parent = wid._nametowidget(parent_name)


    def functask(self):

        d = {}
        numtasks_existing = len(self.func)
        this_row = numtasks_existing

        label_func = tk.Label(self.funcframe,text="Task name: func_")
        label_func.grid(row=this_row)

        text_func = tk.Text(self.funcframe,height=1,width=15)
        text_func.grid(row=this_row,column=1)
        d['text_func'] = text_func

        label_func_nruns = tk.Label(self.funcframe,text="Number of Runs:")
        label_func_nruns.grid(row=this_row,column=2)

        d['label_func_nruns'] = label_func_nruns

        text_func_nruns = tk.Text(self.funcframe,height=1,width=5)
        text_func_nruns.grid(row=this_row,column=3)
        d['text_func_nruns'] = text_func_nruns

        label_func_type = tk.Label(self.funcframe,text="Acquisition Type:")
        label_func_type.grid(row=this_row,column=4)

        # List select for acq type
        mb_acq=  tk.Menubutton ( self.funcframe, text="Acquisition Type", relief=tk.RAISED )
        mb_acq.grid(row=this_row,column=5)
        mb_acq.menu =  tk.Menu ( mb_acq, tearoff = 0 )
        mb_acq["menu"] =  mb_acq.menu

        epiVar = tk.IntVar()
        multibandVar = tk.IntVar()
        spiralVar = tk.IntVar()

        mb_acq.menu.add_checkbutton ( label="EPI",variable=epiVar ,command= lambda: self.optText(mb_acq,'EPI'))
        mb_acq.menu.add_checkbutton ( label="Multiband",variable=multibandVar, command= lambda: self.optText(mb_acq,'Multiband'))
        mb_acq.menu.add_checkbutton ( label="Spiral",variable=spiralVar, command= lambda: self.optText(mb_acq,'Spiral'))

        d['mb_acqtype'] = mb_acq
        button_addtask = tk.Button(self.funcframe,text="Add another task",command= self.addtask)
        button_addtask.grid(row=this_row,column=9)

        d['is_epi'] = epiVar
        d['is_spiral'] = spiralVar
        d['is_multiband'] = multibandVar

        # TO DO: only make available for EPI (just multiband?)
        varFM = tk.IntVar()
        func_cbx_fm = tk.Checkbutton(self.funcframe, text="Has Fieldmap", variable=varFM).grid(row=this_row,column=8)
        d['has_fm'] = varFM
        self.func.append(d)

    def anatrun(self):
        d = {}
        num_existing = len(self.anat)
        this_row = num_existing

        tk.Label(self.anatframe,text="Series name:").grid(row=this_row)
        tk.Label(self.anatframe,text="TYPE: (e.g. t1overlay, t2flair)").grid(row=this_row,column=1)

        text_anat_type = tk.Text(self.anatframe,height=1,width=15)
        text_anat_type.grid(row=this_row,column=2)
        d['text_anat'] = text_anat_type

        tk.Label(self.anatframe,text="NAME: (e.g. 43sl)").grid(row=this_row,column=3)
        text_anat_name = tk.Text(self.anatframe,height=1,width=15)
        text_anat_name.grid(row=this_row,column=4)
        d['text_anat_name'] = text_anat_name

        button_addanat = tk.Button(self.anatframe,text="Add another series",command= self.addanat)
        button_addanat.grid(row=this_row,column=8)

        self.anat.append(d)

    def gettextentry(self,wid):
        inputval = wid.get("1.0","end-1c")
        return inputval

    def addanat(self):
        self.anatrun()

    def addtask(self):
        self.functask()

    def all_children (self,wid) :
        _list = wid.winfo_children()

        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())

        print(_list)
        return _list



root = tk.Tk()
my_gui = ConfigGUI(root)
root.mainloop()
