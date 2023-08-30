import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import Toplevel
from app.gui.config import Config
from app.backend.paths import MyPaths


class SettingsPopUp(Config):
    def __init__(self, master, pd, settings):
        super().__init__()

        self.master = master
        self.icon = ImageTk.PhotoImage(Image.open(MyPaths.icon_path))
        self.set_popup = Toplevel(self.master)

        ws = master.winfo_screenwidth()  # width of the screen
        hs = master.winfo_screenheight()  # height of the screen
        w = pd * 25
        h = pd * 12
        x = int((ws / 2) - (w / 2))
        y = int((hs / 2) - (h / 2))

        # self.set_popup.geometry(f'{pd*25}x{pd*12}')
        self.set_popup.geometry(f"{w}x{h}+{x}+{y}")
        self.set_popup.configure(background=self.background_colour)
        self.set_popup.title(" Advanced Settings")
        self.set_popup.iconphoto(False, self.icon)

        # wait time
        self.set_wt_label = ttk.Label(
            self.set_popup,
            text="Wait time (s)  = ",
            padding=[pd * 3, pd, 0, pd],
            style="popup.small.TLabel",
        )
        self.set_wt_label.grid(row=0, column=0)
        self.set_wt = tk.StringVar(value=1.0)
        self.set_wt_entry = ttk.Entry(self.set_popup, width=5, textvariable=self.set_wt)
        self.set_wt_entry.grid(row=0, column=1)

        def trace_wait_time(*args, **kwargs):
            settings.wait = float(self.set_wt.get())

        self.set_wt.trace_add("write", trace_wait_time)

        # override scroll parameter
        self.set_ovr_label = ttk.Label(
            self.set_popup,
            text="Scrolls per scrape = ",
            padding=[pd * 3, pd, 0, pd],
            style="popup.small.TLabel",
        )
        self.set_ovr_label.grid(row=1, column=0)
        self.set_ovr = tk.StringVar(value=settings.scroll)
        self.set_ovr_entry = ttk.Entry(
            self.set_popup, width=5, textvariable=self.set_ovr
        )
        self.set_ovr_entry.grid(row=1, column=1)

        def trace_ovr_scroll(*args, **kwargs):
            try:
                if self.set_ovr.get():
                    settings.scroll = round(float(self.set_ovr.get()))
            except:
                pass

        self.set_ovr.trace_add("write", trace_ovr_scroll)

        # unhide chrome browser
        self.set_hdl_var = tk.IntVar()
        self.set_hdl_cb = ttk.Checkbutton(
            self.set_popup,
            text=" Unhide Chrome Browser",
            style="popup.TCheckbutton",
            variable=self.set_hdl_var,
        )
        self.set_hdl_cb.grid(row=2, column=0, columnspan=2, padx=pd * 3, pady=pd)

        def trace_set_hdl(*args, **kwargs):
            try:
                if self.set_hdl_var.get():
                    settings.headless = False
                else:
                    settings.headless = True
            except:
                pass

        self.set_hdl_var.trace_add("write", trace_set_hdl)
