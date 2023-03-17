import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from app.gui.config import Config
from app.backend.paths import MyPaths


class UrlFrame(Config):
    def __init__(self, scr_frame, pd, url_input):
        super().__init__()

        self.url_frame = ttk.Frame(scr_frame, style="inner.TFrame")
        # self.url_frame.pack(side='left', fill='both', expand='true')
        UrlFrame.grid_configure(self.url_frame, "c3w1")
        global ticks_crosses
        ticks_crosses = {}
        self.widget_list = []

        self.style.configure(
            "tick.TLabel",
            foreground="#43eb34",
            background=self.tab_colour,
            font=("Arial", "13", "bold"),
        )
        self.style.configure(
            "cross.TLabel",
            foreground="Red",
            background=self.tab_colour,
            font=("Arial", "13"),
        )

        # url input heading 1
        self.url_heading_label = ttk.Label(
            self.url_frame,
            text="URL Input Method",
            style="sub.TLabel",
            padding=[pd, pd, pd, pd],
        )
        self.url_heading_label.grid(row=0, column=0, columnspan=3, sticky="nw")

        # url file input
        def browse_files():
            filename = filedialog.askopenfilename(
                initialdir=MyPaths.urls_path,
                title="Select a File",
                filetypes=(("Text files", "*.txt*"), ("all files", "*.*")),
            )
            if filename:
                self.url_subheading_label.configure(
                    text="File Opened: " + filename
                )
                url_input.add_url_file(filename=filename)

        def textinp():
            self.clear_widgets()
            url_input.reset_url_input()
            self.url_subheading_label = ttk.Label(
                self.url_frame,
                text="Browse for .txt file",
                style="small.TLabel",
                padding=[pd * 3, pd, pd, pd],
            )
            self.url_subheading_label.grid(
                row=5, column=0, columnspan=3, sticky="w"
            )
            self.widget_list.append(self.url_subheading_label)
            self.url_browse_button = ttk.Button(
                self.url_frame,
                text="Browse",
                command=browse_files,
                style="internal.TButton",
            )
            self.url_browse_button.grid(
                row=6, column=0, columnspan=3, sticky="w", padx=pd * 3
            )
            self.widget_list.append(self.url_browse_button)

        # url artist input
        def send_parent_url(*args, **kwargs):
            try:
                url_input.parent_url = self.url_value.get()
            except:
                pass

        def artinp():
            self.clear_widgets()
            url_input.reset_url_input()
            url_input.artist = True
            self.url_subheading_label = ttk.Label(
                self.url_frame,
                text="Enter URL of artist's SoundCloud 'track' page below:",
                style="small.TLabel",
                padding=[pd * 3, pd, pd, pd],
            )
            self.url_subheading_label.grid(
                row=5, column=0, columnspan=3, sticky="w"
            )
            self.widget_list.append(self.url_subheading_label)
            self.url_value = tk.StringVar()
            self.url_entry = ttk.Entry(
                self.url_frame, width=70, textvariable=self.url_value
            )
            self.widget_list.append(self.url_entry)
            self.url_entry.grid(
                row=6, column=0, columnspan=3, sticky="w", padx=pd * 3, pady=pd
            )
            self.url_value.trace_add("write", send_parent_url)
            self.check_entry(mode="artist")

        # url playlist input
        def playinp():
            self.clear_widgets()
            url_input.reset_url_input()
            self.url_subheading_label = ttk.Label(
                self.url_frame,
                text="Enter URL of SoundCloud playlist below:",
                style="small.TLabel",
                padding=[pd * 3, pd, pd, pd],
            )
            self.url_subheading_label.grid(
                row=5, column=0, columnspan=3, sticky="w"
            )
            self.widget_list.append(self.url_subheading_label)
            self.url_value = tk.StringVar()
            self.url_entry = ttk.Entry(
                self.url_frame, width=70, textvariable=self.url_value
            )
            self.url_entry.grid(
                row=6, column=0, columnspan=3, sticky="w", padx=pd * 3, pady=pd
            )
            self.widget_list.append(self.url_entry)
            self.url_value.trace_add("write", send_parent_url)
            self.check_entry(mode="playlist")

        # url manual
        def manualinp():
            # traces all entry widgets and sends text to back end
            def update_urls():
                def add_to_url_list(var, row):  # check these arguments
                    url_input.url_list = [
                        text.get()
                        for row, text in self.url_variables_dict.items()
                        if text.get().strip()
                    ]

                for row, var in self.url_variables_dict.items():
                    var.trace_add(
                        "write",
                        lambda name, index, mode, var=var, row=row: add_to_url_list(
                            var, row
                        ),
                    )

            # creates a new entry widget and moves add button
            def new_url():
                self.url_entry_dict = {}
                r = self.url_add_button.grid_info()["row"]
                self.url_add_button.grid(
                    row=r + 1, column=0, padx=pd * 3, pady=pd, sticky="w"
                )
                self.url_variables_dict[r] = tk.StringVar()
                self.url_entry_dict[r] = ttk.Entry(
                    self.url_frame,
                    width=70,
                    textvariable=self.url_variables_dict[r],
                )
                self.widget_list.append(self.url_entry_dict[r])
                self.url_entry_dict[r].grid(
                    row=r,
                    column=0,
                    columnspan=3,
                    sticky="w",
                    padx=pd * 3,
                    pady=pd,
                )
                self.check_entry(
                    text=self.url_variables_dict[r],
                    row=r,
                    column=3,
                    mode="track",
                )
                update_urls()

            self.clear_widgets()
            url_input.reset_url_input()
            # dict binds tkinter variables to row of entry widget
            self.url_variables_dict = {}
            self.url_subheading_label = ttk.Label(
                self.url_frame,
                text="Enter URLs below:",
                style="small.TLabel",
                padding=[pd * 3, pd, pd, pd],
            )
            self.url_subheading_label.grid(
                row=5, column=0, columnspan=3, sticky="w"
            )
            self.widget_list.append(self.url_subheading_label)
            # initial entry widget and add button
            self.url1_value = tk.StringVar()
            self.url1_entry = ttk.Entry(
                self.url_frame, width=70, textvariable=self.url1_value
            )
            self.widget_list.append(self.url1_entry)
            self.url1_entry.grid(
                row=6, column=0, columnspan=3, sticky="w", padx=pd * 3, pady=pd
            )
            self.style.configure(
                "add.TButton",
                foreground="white",
                background=self.background_colour,
                font=(self.font_bold, "10", "bold"),
            )
            self.url_add_button = ttk.Button(
                self.url_frame,
                text="+",
                style="add.TButton",
                width=2,
                command=new_url,
            )
            self.widget_list.append(self.url_add_button)
            self.url_add_button.grid(
                row=7, column=0, padx=pd * 3, pady=pd, sticky="w"
            )
            self.placeholder = ttk.Label(self.url_frame, style="TLabel")
            self.placeholder.grid(row=6, column=6)
            self.check_entry(text=self.url1_value, mode="track")
            self.url_variables_dict[6] = self.url1_value
            update_urls()

        # url input method radiobuttons
        self.retrieval_type = tk.StringVar()
        self.url_rb1 = ttk.Radiobutton(
            self.url_frame,
            text="Manual",
            padding=[pd * 3, pd, pd, 0],
            value="M",
            variable=self.retrieval_type,
            style="TRadiobutton",
            command=manualinp,
        )
        self.url_rb1.grid(row=1, column=0, columnspan=2, sticky="nw")
        self.url_rb2 = ttk.Radiobutton(
            self.url_frame,
            text="From .txt file",
            padding=[pd * 3, pd, pd, 0],
            value="L",
            variable=self.retrieval_type,
            style="TRadiobutton",
            command=textinp,
        )
        self.url_rb2.grid(row=2, column=0, columnspan=2, sticky="nw")
        self.url_rb3 = ttk.Radiobutton(
            self.url_frame,
            text="From artist 'track' page",
            padding=[pd * 3, pd, pd * 16, 0],
            value="A",
            variable=self.retrieval_type,
            style="TRadiobutton",
            command=artinp,
        )
        self.url_rb3.grid(row=1, column=2, columnspan=3, sticky="nw")
        self.url_rb4 = ttk.Radiobutton(
            self.url_frame,
            text="From playlist",
            padding=[pd * 3, pd, pd, pd],
            value="P",
            variable=self.retrieval_type,
            style="TRadiobutton",
            command=playinp,
        )
        self.url_rb4.grid(row=2, column=2, sticky="nw")

        # url input max urls
        def url_max_trace(*args, **kwargs):
            try:
                url_input.url_max = self.url_max.get()
            except:
                pass

        self.url_max = tk.IntVar(value=10)
        self.url_max_label = ttk.Label(
            self.url_frame,
            text="Enter max urls  =",
            style="small.TLabel",
            padding=[pd * 3, pd, pd, pd],
        )
        self.url_max_label.grid(row=3, column=0)
        self.url_max_entry = ttk.Entry(
            self.url_frame, width=5, textvariable=self.url_max
        )
        self.url_max.trace_add("write", url_max_trace)
        self.url_max_entry.grid(row=3, column=1, sticky="w")

        # subheading 2
        self.url_heading2_label = ttk.Label(
            self.url_frame,
            text="URL Entry",
            style="sub.TLabel",
            padding=[pd, pd * 3, pd, pd],
        )
        self.url_heading2_label.grid(row=4, column=0, columnspan=3, sticky="w")

    def check_entry(self, mode, text=None, row=6, column=3):
        def tick_or_cross(*args):
            global ticks_crosses
            self.style.configure(
                "tick.TLabel",
                foreground="#43eb34",
                background=self.tab_colour,
                font=("Arial", "13", "bold"),
            )
            self.style.configure(
                "cross.TLabel",
                foreground="Red",
                background=self.tab_colour,
                font=("Arial", "13"),
            )
            if mode == "track":
                condition1 = "https://soundcloud.com/"
                condition2 = "https://soundcloud.com/"
            elif mode == "artist":
                condition1 = "https://soundcloud.com/"
                condition2 = "/tracks"
            elif mode == "playlist":
                condition1 = "https://soundcloud.com/"
                condition2 = "/sets"
            else:
                pass
            if row in ticks_crosses:
                ticks_crosses[row].destroy()
                if ticks_crosses[row] in self.widget_list:
                    self.widget_list.remove(ticks_crosses[row])
                del ticks_crosses[row]
            if condition1 and condition2 in text.get():
                ticks_crosses[row] = ttk.Label(
                    self.url_frame, text="✓", style="tick.TLabel", width=2
                )
            elif not text.get():
                pass
            else:
                ticks_crosses[row] = ttk.Label(
                    self.url_frame, text="✖", style="cross.TLabel", width=2
                )
            for row_, widget in ticks_crosses.items():
                widget.grid(row=row_, column=column, sticky="w")
                self.widget_list.append(widget)

        if text is None:
            text = self.url_value
        text.trace_add("write", tick_or_cross)
