from tkinter import ttk
from app.gui.config import Config
from app.gui.start_frame import StartFrame
from app.gui.url_frame import UrlFrame
from app.gui.settings_frame import SettingsFrame


class ScrapingFrame(Config):

    """First page of notebook, contains all widgets pertaining
    to the scraping of comments"""

    def __init__(self, notebook, pd, master, url_input, settings, filters):
        super().__init__()

        self.scr_frame = ttk.Frame(notebook, style="TFrame")
        self.scr_frame.pack(fill="both", expand=True)

        self.url_frame = UrlFrame(
            self.scr_frame, pd=pd, url_input=url_input
        ).url_frame
        self.set_frame = SettingsFrame(
            self.scr_frame,
            pd=pd,
            master=master,
            settings=settings,
            filters=filters,
        ).set_frame

        # will this pass the updated filters and settings etc.?
        self.start_frame = StartFrame(
            self.scr_frame,
            pd=pd,
            master=master,
            url_input=url_input,
            settings=settings,
            filters=filters,
        ).start_frame

        self.start_frame.pack(side="bottom", fill="both", expand="False")
        self.url_frame.pack(side="left", fill="both", expand="true")
        self.set_frame.pack(side="right", fill="both", expand="true")
