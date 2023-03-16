from tkinter import ttk

from app.gui.config import Config


class DAFrame(Config):

    """Second page of notebook, contains all widgets pertaining
    to the clean-up and analysis of comments"""

    def __init__(self, notebook, pd):
        super().__init__()

        self.da_frame = ttk.Frame(notebook, style="TFrame")
        self.da_frame.pack(fill="both", expand=True)
