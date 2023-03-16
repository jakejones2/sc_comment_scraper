import tkinter as tk
from tkinter import ttk
from app.gui.config import Config
from app.gui.filter_popup import FilterPopUp


class FilterFrame(Config):
    def __init__(self, set_frame, pd, master, filters):
        super().__init__()

        # binds each filter to an integer key
        self.filt_dict = {}

        # header and frame widgets
        self.filt_frame = ttk.Frame(set_frame, style="inner2.TFrame")
        self.filt_frame.grid(column=0, row=4, columnspan=5, sticky="w", padx=0)
        self.filt_heading_label = ttk.Label(
            self.filt_frame,
            text="Filters",
            style="sub2.TLabel",
            padding=[pd, pd, pd, pd],
        )
        self.filt_heading_label.grid(row=0, column=0, pady=pd, sticky="w")

        #'none' checkbutton
        def n_cbutton():
            if self.filt_n_var.get():
                self.enact_filter("on", "index > 1", "N", filters)
            else:
                self.enact_filter("off", "index > 1", "N", filters)
            if self.filt_n_var.get():
                self.custom_filter_button.config(state="disabled")
            else:
                self.custom_filter_button.config(state="normal")

        self.filt_n_var = tk.IntVar()
        self.filt_n_cbutton = ttk.Checkbutton(
            self.filt_frame,
            text=" None",
            style="filters.TCheckbutton",
            variable=self.filt_n_var,
            command=n_cbutton,
        )
        self.filt_n_cbutton.grid(row=1, column=0, padx=pd * 3, sticky="w")
        self.filt_dict[1] = self.filt_n_cbutton

        #'just emojis' checkbutton
        def je_cbutton():
            if self.filt_je_var.get():
                self.enact_filter("on", "index != 2", "JE", filters)
            else:
                self.enact_filter("off", "index != 2", "JE", filters)

        self.filt_je_var = tk.IntVar()
        self.filt_je_cbutton = ttk.Checkbutton(
            self.filt_frame,
            text=" Just emojis",
            style="filters.TCheckbutton",
            variable=self.filt_je_var,
            command=je_cbutton,
        )
        self.filt_je_cbutton.grid(row=1, column=1, padx=pd * 3, sticky="w")
        self.filt_dict[2] = self.filt_je_cbutton

        #'no emojis' checkbutton
        def ne_cbutton():
            if self.filt_ne_var.get():
                self.enact_filter("on", "index <= 2", "NE", filters)
            else:
                self.enact_filter("off", "index <= 2", "NE", filters)

        self.filt_ne_var = tk.IntVar()
        self.filt_ne_cbutton = ttk.Checkbutton(
            self.filt_frame,
            text=" No emojis",
            style="filters.TCheckbutton",
            variable=self.filt_ne_var,
            command=ne_cbutton,
        )
        self.filt_ne_cbutton.grid(row=1, column=2, padx=pd * 3, sticky="w")
        self.filt_dict[3] = self.filt_ne_cbutton

        #'no user tags' checkbutton
        def nt_cbutton():
            if self.filt_nt_var.get():
                self.enact_filter("on", "index not in (3, 4)", "NT", filters)
            else:
                self.enact_filter("off", "index not in (3, 4)", "NT", filters)

        self.filt_nt_var = tk.IntVar()
        self.filt_nt_cbutton = ttk.Checkbutton(
            self.filt_frame,
            text=" No user tags",
            style="filters.TCheckbutton",
            variable=self.filt_nt_var,
            command=nt_cbutton,
        )
        self.filt_nt_cbutton.grid(
            row=2, column=0, padx=pd * 3, pady=pd, sticky="w"
        )
        self.filt_dict[4] = self.filt_nt_cbutton

        #'no replies' checkbutton
        def nr_cbutton():
            if self.filt_nr_var.get():
                self.enact_filter("on", "index not in (3, 5)", "NR", filters)
            else:
                self.enact_filter("off", "index not in (3, 5)", "NR", filters)

        self.filt_nr_var = tk.IntVar()
        self.filt_nr_cbutton = ttk.Checkbutton(
            self.filt_frame,
            text=" No replies",
            style="filters.TCheckbutton",
            variable=self.filt_nr_var,
            command=nr_cbutton,
        )
        self.filt_nr_cbutton.grid(
            row=2, column=1, padx=pd * 3, pady=pd, sticky="w"
        )
        self.filt_dict[5] = self.filt_nr_cbutton

        #'no social' checkbutton
        def ns_cbutton():
            if self.filt_ns_var.get():
                self.enact_filter("on", "index not in (3, 6)", "NS", filters)
            else:
                self.enact_filter("off", "index not in (3, 6)", "NS", filters)

        self.filt_ns_var = tk.IntVar()
        self.filt_ns_cbutton = ttk.Checkbutton(
            self.filt_frame,
            text=" No social",
            style="filters.TCheckbutton",
            variable=self.filt_ns_var,
            command=ns_cbutton,
        )
        self.filt_ns_cbutton.grid(
            row=2, column=2, padx=pd * 3, pady=pd, sticky="w"
        )
        self.filt_dict[6] = self.filt_ns_cbutton

        # custom filters button
        def custom_filters():
            self.custom_filter_pop = FilterPopUp(
                master=master, pd=pd, filters=filters
            )

        self.custom_filter_button = ttk.Button(
            self.filt_frame,
            text=" Custom filters ",
            command=custom_filters,
            style="internal2.TButton",
        )
        self.custom_filter_button.grid(
            row=3, column=0, sticky="w", padx=pd * 2, pady=pd * 1.5
        )

    def enact_filter(self, action, index_condition, filt, filters):
        # disable checkbuttons of incompatible filters
        for index, cbutton in self.filt_dict.items():
            if not eval(index_condition):
                continue
            elif action == "on":
                cbutton.config(state="disabled")
            elif action == "off":
                if (
                    self.filt_ne_var.get()
                    or self.filt_nt_var.get()
                    or self.filt_ns_var.get()
                    or self.filt_nr_var.get()
                ) and index in (1, 2):
                    continue
                cbutton.config(state="active")
        # apply or remove filter
        if action == "on":
            filters.add_or_remove_filter("add", filt)
        elif action == "off":
            filters.add_or_remove_filter("remove", filt)
