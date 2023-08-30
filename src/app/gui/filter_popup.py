import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import Toplevel
from app.gui.config import Config
from app.backend.paths import MyPaths


class FilterPopUp(Config):
    def __init__(self, master, pd, filters):
        super().__init__()

        self.master = master
        self.icon = ImageTk.PhotoImage(Image.open(MyPaths.icon_path))
        self.filt_popup = Toplevel(self.master)
        self.filt_popup.configure(background=self.background_colour)
        self.filt_popup.title(" Custom filters (comma-delimited list)")
        self.filt_popup.iconphoto(False, self.icon)

        #'no comments containing' checkbutton
        self.filt_no_cbutton_var = tk.IntVar()
        self.filt_no_cbutton = ttk.Checkbutton(
            self.filt_popup,
            text=" No comments containing the following strings: ",
            style="popup.TCheckbutton",
            padding=[0, pd, 0, 0],
            variable=self.filt_no_cbutton_var,
        )
        if filters.current_no_cbutton:
            self.filt_no_cbutton.state(["selected"])
        self.filt_no_cbutton.grid(row=3, column=0, columnspan=3, padx=pd, sticky="w")

        self.filt_no_entry_var = tk.StringVar()
        self.filt_no_entry = ttk.Entry(
            self.filt_popup, width=pd * 8, textvariable=self.filt_no_entry_var
        )
        self.filt_no_entry.insert(0, filters.current_no_cfilter)
        self.filt_no_entry.grid(
            row=4, column=0, columnspan=3, padx=pd, pady=pd, sticky="w"
        )
        if filters.current_no_cbutton:
            self.filt_no_entry.config(state="active")
        else:
            self.filt_no_entry.config(state="disabled")

        #'only comments containing' checkbutton
        self.filt_only_cbutton_var = tk.IntVar()
        self.filt_only_cbutton = ttk.Checkbutton(
            self.filt_popup,
            text=" Only comments containing the following strings: ",
            style="popup.TCheckbutton",
            padding=[0, pd, 0, 0],
            variable=self.filt_only_cbutton_var,
        )
        if filters.current_only_cbutton:
            self.filt_only_cbutton.state(["selected"])
        self.filt_only_cbutton.grid(row=5, column=0, columnspan=3, padx=pd, sticky="w")

        self.filt_only_entry_var = tk.StringVar()
        self.filt_only_entry = ttk.Entry(
            self.filt_popup,
            width=pd * 8,
            textvariable=self.filt_only_entry_var,
        )
        self.filt_only_entry.insert(0, filters.current_only_cfilter)
        self.filt_only_entry.grid(
            row=6, column=0, columnspan=3, padx=pd, pady=pd, sticky="w"
        )
        if filters.current_only_cbutton:
            self.filt_only_entry.config(state="active")
        else:
            self.filt_only_entry.config(state="disabled")

        #'remove all instances' checkbutton
        self.filt_omit_cbutton_var = tk.IntVar()
        self.filt_omit_cbutton = ttk.Checkbutton(
            self.filt_popup,
            text=" Remove all instances of the following strings: ",
            style="popup.TCheckbutton",
            padding=[0, pd, 0, 0],
            variable=self.filt_omit_cbutton_var,
        )
        if filters.current_omit_cbutton:
            self.filt_omit_cbutton.state(["selected"])
        self.filt_omit_cbutton.grid(row=7, column=0, columnspan=3, padx=pd, sticky="w")

        self.filt_omit_entry_var = tk.StringVar()
        self.filt_omit_entry = ttk.Entry(
            self.filt_popup,
            width=pd * 8,
            textvariable=self.filt_omit_entry_var,
        )
        self.filt_omit_entry.insert(0, filters.current_omit_cfilter)
        self.filt_omit_entry.grid(
            row=8, column=0, columnspan=3, padx=pd, pady=pd, sticky="w"
        )
        if filters.current_omit_cbutton:
            self.filt_omit_entry.config(state="active")
        else:
            self.filt_omit_entry.config(state="disabled")

        # tracing 'no' custom filter
        def no_cbutton(*args, **kwargs):
            if self.filt_no_cbutton_var.get():
                filters.current_no_cbutton = True
                self.filt_no_entry.config(state="active")
            else:
                filters.current_no_cbutton = False
                self.filt_no_entry.config(state="disabled")

        self.filt_no_cbutton_var.trace_add("write", no_cbutton)

        def no_entry(*args, **kwargs):
            filters.current_no_cfilter = self.filt_no_entry_var.get()

        self.filt_no_entry_var.trace_add("write", no_entry)

        # tracing 'only' custom filter
        def only_cbutton(*args, **kwargs):
            if self.filt_only_cbutton_var.get():
                filters.current_only_cbutton = True
                self.filt_only_entry.config(state="active")
            else:
                filters.current_only_cbutton = False
                self.filt_only_entry.config(state="disabled")

        self.filt_only_cbutton_var.trace_add("write", only_cbutton)

        def only_entry(*args, **kwargs):
            filters.current_only_cfilter = self.filt_only_entry_var.get()

        self.filt_only_entry_var.trace_add("write", only_entry)

        # tracing 'omit' custom filter
        def omit_cbutton(*args, **kwargs):
            if self.filt_omit_cbutton_var.get():
                filters.current_omit_cbutton = True
                self.filt_omit_entry.config(state="active")
            else:
                filters.current_omit_cbutton = False
                self.filt_omit_entry.config(state="disabled")

        self.filt_omit_cbutton_var.trace_add("write", omit_cbutton)

        def omit_entry(*args, **kwargs):
            filters.current_omit_cfilter = self.filt_omit_entry_var.get()

        self.filt_omit_entry_var.trace_add("write", omit_entry)
