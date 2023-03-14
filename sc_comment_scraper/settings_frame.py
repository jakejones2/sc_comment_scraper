import tkinter as tk
from tkinter import ttk
from config import Config
from settings_popup import SettingsPopUp
from filter_frame import FilterFrame

class SettingsFrame(Config):
    
    def __init__(self, scr_frame, pd, master, settings, filters):
        super().__init__()

        self.style.configure('inner2.TFrame', background=self.tab_colour2)
        self.set_frame = ttk.Frame(scr_frame, style='inner2.TFrame')
        #self.set_frame.pack(side='right', fill='both', expand='true')
        SettingsFrame.grid_configure(self.set_frame, 'c4w1')

        self.set_heading_label = ttk.Label(self.set_frame,
                                           text='Scraping Settings',
                                           style='sub2.TLabel',
                                           padding=[pd, pd, pd, pd])
        self.set_heading_label.grid(row=0,
                                    column=0,
                                    columnspan=5,
                                    sticky='nw')
        self.widget_list = []

        #merge or individual csv files
        def csv_ind():
            self.set_fn_entry.config(state='disabled')
            settings.csv_merge = False
        
        def csv_merge():

            def send_filename(*args, **kwargs):
                try:
                    settings.csvfilename = self.set_fn_var.get()
                    settings.check_csvfilename()
                except: pass

            self.set_fn_entry.config(state='active')
            settings.csv_merge = True
            self.set_fn_var.trace_add('write', send_filename)

        self.csv_merge = tk.StringVar()
        self.set_rb1 = ttk.Radiobutton(self.set_frame, 
                                       text='Indiviual csv files', 
                                       padding=[pd*3, pd, pd*4, pd], 
                                       value='I', 
                                       variable=self.csv_merge, 
                                       style='tab2.TRadiobutton', 
                                       command=csv_ind)
        self.set_rb1.grid(row=1, column=0, columnspan=3, sticky='w')
        self.set_rb2 = ttk.Radiobutton(self.set_frame, 
                                       text='Merge csv files as  =', 
                                       padding=[pd*2, pd, 0, pd], 
                                       value='M', 
                                       variable=self.csv_merge, 
                                       style='tab2.TRadiobutton', 
                                       command=csv_merge)
        self.set_rb2.grid(row=1, column=2, sticky='w')
        self.set_fn_var = tk.StringVar()
        self.set_fn_entry = ttk.Entry(self.set_frame, 
                                      width=pd, 
                                      state='disabled', 
                                      textvariable=self.set_fn_var)
        self.set_fn_entry.grid(row=1, column=4, padx=pd, sticky='w')

        #max number of comments per url

        self.set_maxnum_label = ttk.Label(
            self.set_frame,
            text='Enter max comments per url  =',
            padding=[pd*3, pd, pd, pd],
            style='tab2.small.TLabel')
        self.set_maxnum_label.grid(row=2, column=0, columnspan=2, sticky='w')
        self.set_maxnum_var = tk.IntVar(value=100)
        self.set_maxnum_entry = ttk.Entry(self.set_frame, 
                                          width=7,
                                          textvariable=self.set_maxnum_var)
        self.set_maxnum_entry.grid(row=2, 
                                   column=2, 
                                   columnspan=3, 
                                   sticky='w')
        def max_num_trace(*args, **kwargs):
            try:
                settings.max_num = self.set_maxnum_var.get()
                settings.estimate_scroll()
            except: pass
        self.set_maxnum_var.trace_add('write', max_num_trace)

        #advanced settings
        def adv_settings():
            self.set_adv_pop = SettingsPopUp(master=master, pd=pd, settings=settings)
            
        self.set_adv_button = ttk.Button(self.set_frame, 
                                         text=" Advanced Settings ", 
                                         command=adv_settings, 
                                         style='internal2.TButton')
        self.set_adv_button.grid(row=3, 
                                 column=0, 
                                 sticky='w', 
                                 padx=pd*2, 
                                 pady=pd*1.5)

        self.filters = FilterFrame(self.set_frame, pd, master, filters=filters)