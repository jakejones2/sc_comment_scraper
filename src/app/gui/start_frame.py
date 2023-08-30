import tkinter as tk
from tkinter import ttk
from app.gui.config import Config
from app.backend.scraper import Scraper


class StartFrame(Config):
    def __init__(self, scr_frame, pd, master, url_input, settings, filters):
        super().__init__()
        self.start_frame = ttk.Frame(scr_frame, style="start.TFrame")

        # start button
        def debug():
            if filters.current_no_cbutton and filters.current_no_cfilter:
                filters.add_or_remove_cfilter(
                    "add", "exclude", filters.current_no_cfilter
                )
            if filters.current_only_cbutton and filters.current_only_cfilter:
                filters.add_or_remove_cfilter(
                    "add", "include", filters.current_only_cfilter
                )
            if filters.current_omit_cbutton and filters.current_omit_cfilter:
                filters.add_or_remove_cfilter(
                    "add", "omit", filters.current_omit_cfilter
                )
            self.scraper.debug(settings=settings, url_input=url_input, filters=filters)

        def start():
            # load urls
            self.scraper.load_urls(url_input, settings)
            # check for custom filters
            if filters.current_no_cbutton and filters.current_no_cfilter:
                filters.add_or_remove_cfilter(
                    "add", "exclude", filters.current_no_cfilter
                )
            if filters.current_only_cbutton and filters.current_only_cfilter:
                filters.add_or_remove_cfilter(
                    "add", "include", filters.current_only_cfilter
                )
            if filters.current_omit_cbutton and filters.current_omit_cfilter:
                filters.add_or_remove_cfilter(
                    "add", "omit", filters.current_omit_cfilter
                )
            self.start_button.config(state="disabled")
            # scrape
            self.scraper.scrape(url_input, settings, filters)
            self.start_button.config(state="normal")

            # remove previous custom filters -- do this automatically like built ins!!!
            if filters.current_no_cbutton and filters.current_no_cfilter:
                filters.add_or_remove_cfilter(
                    "remove", "exclude", filters.current_no_cfilter
                )
            if filters.current_only_cbutton and filters.current_only_cfilter:
                filters.add_or_remove_cfilter(
                    "remove", "include", filters.current_only_cfilter
                )
            if filters.current_omit_cbutton and filters.current_omit_cfilter:
                filters.add_or_remove_cfilter(
                    "remove", "omit", filters.current_omit_cfilter
                )

        self.style.configure(
            "start.TButton",
            foreground=self.text_colour,
            background=self.green,
            font=(self.font_bold, "12"),
        )
        self.style.map("start.TButton", foreground=[("active", "!disabled", "black")])

        self.start_button = ttk.Button(
            self.start_frame,
            text="Start",
            style="start.TButton",
            padding=[pd, int(pd / 1.3), int(pd / 1.3), pd],
            command=start,
        )

        self.start_button.pack(side="right", pady=pd)

        # create scraper instance
        self.scraper = Scraper(settings=settings, start_frame=self.start_frame, pd=pd)

        # run frame
        self.run_frame = self.scraper.run_frame
        self.run_frame.pack(side="right", fill="both", expand=True, pady=pd)
