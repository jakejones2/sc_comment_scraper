from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
import os
from datetime import datetime
import emoji
import re

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app.gui.config import Config
from app.backend.backup_ui import UI
from app.backend.check_dir import check_merged_dir, check_ind_dir
from app.backend.paths import MyPaths


class Scraper(Config):
    def __init__(self, settings, start_frame, pd):
        '''instance creates the tkinter progress bar and
        current operations label'''
        super().__init__()

        # create frame
        self.run_frame = ttk.Frame(start_frame, style="start.TFrame")

        # create progress bar
        self.style.configure(
            "Horizontal.TProgressbar",
            troughcolor=self.tab_colour,
            darkcolor=self.green,
            lightcolor=self.other_blue,
            background=self.green,
            bordercolour=self.tab_colour,
        )
        self.progress_bar = ttk.Progressbar(
            self.run_frame,
            length=pd * 95,
            mode="determinate",
            orient=tk.HORIZONTAL,
            style="Horizontal.TProgressbar",
        )
        self.progress_bar.grid(column=0, row=0, sticky="nw")

        # create current operation label
        self.style.configure(
            "task.TLabel",
            font=(self.font_light, 10),
            foreground=self.text_colour,
            background=self.background_colour,
        )
        self.current_task = ttk.Label(
            self.run_frame,
            style="task.TLabel",
            text="Press start to begin scraping",
        )
        self.current_task.grid(column=0, row=1, sticky="nw")
    
        # all attributes
        self.current_ops = 0 # tracks completed ops for progress bar
        self.options = Options() # chrome driver options
        self.driver = '' # will denote chromedriver
        self.track_scroll = 0 # estimated number of scrolls for parent url 
        self.comments_master_list = [] # all comments stored here
        self.timestamps_master_list = [] # all timestamps 
        self.datetimes_master_list = [] # all datetimes
        self.previous_comments = [] # used to prevent infinite comment loop

        self.comments_list = [] # temp storage used in comment loop
        self.index_list = [] # used to log position of retrieved comments
        self.comments_list_length = [] # prevents infinite loop
        self.comment_count = 0 # used in comment loop

        self.track = '' # used to generate csv filename
        self.artist = '' # used to generate csv filename
        self.dir = '' # path for csv file

    def current_ops_update(self):

        '''calculates the number of completed operations'''

        self.current_ops = (
            len(self.comments_master_list)
            + len(self.timestamps_master_list)
            + len(self.datetimes_master_list)
        )
        return self.current_ops
    

    def load_urls(self, url_input, settings):

        '''initialises chrome driver, and retrieves urls from the specified
        parent url (either a soundcloud playlist or artist 'track' page).
        These are added to url_input.url_list'''

        # ensure attributes are reset in case scrape repeated
        self.track_scroll = 0

        # estimates number of scrolls needed to find track urls
        # assumes each scroll generates 10 tracks on page
        # if url input set to manual or by file, this is skipped
        if url_input.parent_url:
            if url_input.url_max < 10:
                self.track_scroll = 0
            else:
                self.track_scroll = round(int(url_input.url_max) / 10)
        
        # calculating total operations and configuring progress bar
        if url_input.parent_url:
            self.total_ops = (
                (3 * settings.max_num * url_input.url_max)
                + (30 * url_input.url_max)
                + (len(url_input.parent_url) # adds ops if parent_url scraped
                + (5 * self.track_scroll)) # adds ops if parent_url scrolled
                + 10) # adds ops for driver boot
            self.progress_bar.config(maximum=self.total_ops)
        else:
            self.total_ops = (
                (3 * settings.max_num * len(url_input.url_list))
                + (30 * len(url_input.url_list))
                + 10) # adds ops for driver boot
            self.progress_bar.config(maximum=self.total_ops)

        # update progress bar
        self.progress_bar["value"]  = 1
        self.current_task.config(
            text="Initialising Google Chrome driver..."
        )
        self.progress_bar.update()

        # initialise headless chrome browser using driver manager
        try:
            self.options.add_experimental_option(
                "excludeSwitches", ["enable-logging"]
            )
            self.options.add_experimental_option(
                "prefs", 
                {"profile.managed_default_content_settings.images": 2}
            )
            if settings.headless:
                self.options.add_argument("--headless")
                self.options.add_argument("--mute-audio")

            # attempts to stop 'webdriver-manager' package from 
            # printing installation in terminal (not working)
            os.environ["WDM_PROGRESS_BAR"] = ""

            # creating chromedriver instance
            self.driver = webdriver.Chrome(
                service=Service(
                    ChromeDriverManager(path=r".\\Drivers").install()
                ),
                options=self.options,
            )
        except:
            messagebox.showerror(
                "Scraping Error", "Failed to initialise Google Chrome driver"
            )

        # if a parent_url attribute is present, scrape this url
        if url_input.parent_url:

            # update progress bar
            self.current_task.config(
                text="Retrieving artist or playlist url..."
            )
            self.progress_bar['value'] = 10 # driver booted ops
            self.progress_bar.update()

            # clears any previous url_list generated via parent url
            url_input.url_list = []

            # scrape parent url
            try:
                self.driver.get(url_input.parent_url)
            except:
                messagebox.showerror(
                    "Scraping Error", "Failed to retrieve artist/playlist URL"
                )

            # update progress bar
            self.current_task.config(
                text=f"Parent url: {url_input.parent_url}  |  Scrolling page and retrieving tracks"
            )
            self.progress_bar.update()

            # retrieving track urls
            try:
                previous_elements = []
                while True:

                    # scroll page the estimated number of times
                    for n in range(self.track_scroll):
                        try:
                            self.driver.execute_script(
                                "window.scrollTo(0, document.body.scrollHeight);"
                            )
                            time.sleep(settings.wait)
                        except:
                            time.sleep(0.5)

                    # search for track links
                    if url_input.artist:
                        track_elements = self.driver.find_elements(
                            By.CLASS_NAME, "soundTitle__title"
                        )
                    else:
                        track_elements = self.driver.find_elements(
                            By.CLASS_NAME, "trackItem__trackTitle"
                        )

                    # check there are enough elements
                    if len(track_elements) >= url_input.url_max:
                        break

                    # ensure scrolling loop breaks
                    if len(previous_elements) >= len(track_elements):
                        break
                    previous_elements = track_elements

                    # update progress bar
                    self.progress_bar['value'] += (
                        len(url_input.parent_url) # parent url scraped
                    )
                    self.progress_bar.update()

                # add the right amount of links to url_list
                for count, element in enumerate(track_elements, start=1):
                    if count > url_input.url_max:
                        break
                    else:
                        url_input.url_list.append(element.get_attribute("href"))
            except:
                messagebox.showerror(
                    "Scraping Error",
                    "Failed to find links on track/playlist URL",
                )
            
            # update progress bar (start frame now adds any custom filters)
            self.current_task.config(
                text=f"Parent url: {url_input.parent_url}  |  Loading filters"
            )
            self.progress_bar['value'] += (
                (5 * self.track_scroll) # parent url scrolled
            )
            self.progress_bar.update()

    def scrape(self, url_input, settings, filters):
        self.comments_master_list = []
        self.timestamps_master_list = []
        self.datetimes_master_list = []
        self.previous_comments = []

        scrape_start_time = time.time()
        scrape_datetime = datetime.now()

        for count, url in enumerate(url_input.url_list, start=1):
            
            # update progress bar
            self.current_task.config(
                text=f"url{count}: {url}  |  Retrieving url..."
            )
            self.progress_bar["value"] += 10 # driver ops
            self.current_task.update()

            #get url
            try:
                self.driver.get(url)
            except:
                messagebox.showerror(
                    "Scraping Error", f"Failed to retrieve {url}"
                )

            # accept cookies
            if not settings.headless:
                time.sleep(settings.wait)
                try:
                    self.driver.find_element(
                        By.ID, "onetrust-accept-btn-handler"
                    ).click()
                except:
                    pass

            # update progress bar
            self.progress_bar["value"] += 2 # got url/cookies
            self.current_task.config(
                text=f"url{count}: {url}  |  Scrolling page..."
            )
            self.current_task.update()

            # scroll page and find comments
            try:
                # initial scroll
                for n in range(settings.scroll):
                    try:
                        self.driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);"
                        )
                        time.sleep(settings.wait)
                        # update stops the gui from 'not responding'
                        self.current_task.update()
                    except:
                        time.sleep(0.5)

                # finishhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
                self.current_task.config(
                    text=f"url{count}: {url}  |  Retrieving comments..."
                )
                self.progress_bar["value"] += 18 # scrolled page
                self.current_task.update()

                self.comments_list = []
                self.index_list = []
                self.comments_list_length = []
                self.comment_count = -1

                # comment-retrieving loop
                while True:
                    # find all comments
                    self.comments = self.driver.find_elements(
                        By.CLASS_NAME, "commentItem__body"
                    )
                    for n in range(len(self.comments)):
                        # ignore previously scanned comments
                        if n <= self.comment_count:
                            continue
                        # filters
                        elif filters.no_filters:
                            self.comments_list.append(self.comments[n].text)
                            # index comments that pass filtering
                            # saves time when finding timestamps and datetimes
                            self.index_list.append(n)
                            self.comment_count = n
                        elif filters.just_emojis:
                            self.emoji_dict_list = emoji.emoji_list(
                                self.comments[n].text
                            )
                            for emoji_dict in self.emoji_dict_list:
                                self.comments_list.append(emoji_dict["emoji"])
                                self.index_list.append(n)
                                self.comment_count = n
                        else:
                            text = self.comments[n].text
                            self.index_list.append(n)
                            self.comment_count = n
                            if filters.subtractive_filters:
                                for x in filters.subtractive_filters:
                                    # evaluate the filter, usually reg ex
                                    text = eval(x).strip()
                                    # if fails, delete index
                                    if text:
                                        continue
                                    if n in self.index_list:
                                        self.index_list.remove(n)
                                if filters.additive_filters:
                                    for x in filters.additive_filters:
                                        # if search criteria not met
                                        if eval(x):
                                            continue
                                        text = ""
                                        if n in self.index_list:
                                            self.index_list.remove(n)
                                # if passed both add/sub filters
                                self.comments_list.append(text)
                                # prevent gui from 'not responding'
                                self.current_task.update()
                    # removing empty strings
                    self.comments_list = [
                        x for x in self.comments_list if x.strip()
                    ]
                    # halting if no new comments found in extra scroll
                    if self.previous_comments == len(self.comments):
                        break
                    self.previous_comments = len(self.comments)
                    # ensuring max_num
                    if len(self.comments_list) >= settings.max_num:
                        self.comments_list = self.comments_list[
                            : settings.max_num
                        ]
                        self.index_list = self.index_list[: settings.max_num]
                        break
                    # extra scrolls if max_num not hit
                    for n in range(settings.extra_scroll):
                        try:
                            self.driver.execute_script(
                                "window.scrollTo(0, document.body.scrollHeight);"
                            )
                            time.sleep(settings.wait)
                        except:
                            time.sleep(0.5)
                # append final comments list to master
                for c in self.comments_list:
                    self.comments_master_list.append(c)

                #update progress bar
                self.progress_bar["value"] += settings.max_num # one url's comments
                self.current_task.config(text=f"url{count}: {url}  |  Retrieving timestamps...")
                self.current_task.update()
            except:
                messagebox.showerror(
                    "Scraping Error", f"Failed to retrieve comments from {url}"
                )

            # find all timestamps
            try:
                self.timestamps = self.driver.find_elements(
                    By.CLASS_NAME, "commentItem__timestampLink"
                )
                self.timestamps_list = []
                for t in range(len(self.timestamps)):
                    if t in self.index_list:
                        self.timestamps_list.append(self.timestamps[t].text)
                        self.timestamps_master_list.append(
                            self.timestamps[t].text
                        )
            except:
                messagebox.showerror(
                    "Scraping Error",
                    f"Failed to find timestamps in {url} HTML",
                )

            # update progress bar
            self.progress_bar["value"] += settings.max_num # one url's timestamps
            self.current_task.config(
                text=f"url{count}: {url}  |  Retrieving datetimes..."
            )
            self.current_task.update()

            # find all datetimes posted
            try:
                self.dates = self.driver.find_elements(
                    By.CLASS_NAME, "relativeTime"
                )
                self.datetimes_list = []
                for d in range(len(self.dates)):
                    if d in self.index_list:
                        self.datetimes_list.append(
                            self.dates[d].get_attribute("datetime")
                        )
                        self.datetimes_master_list.append(
                            self.dates[d].get_attribute("datetime")
                        )
            except:
                messagebox.showerror(
                    "Scraping Error", f"Failed to find datetimes in {url} HTML"
                )

            # update progress bar
            self.progress_bar["value"] += settings.max_num # one url's datetimes


            # write data to individual csv
            if not settings.csv_merge:

                # update progress bar
                self.current_task.config(
                text=f"url{count}: {url}  |  Writing to CSV..."
                )
                self.current_task.update()

                # extract title name from url and apply filtername
                # placing in csv_exports folder via relative path
                try:
                    self.track = url.split("/")[-1]
                    self.artist = url.split("/")[-2]
                    if "?" in self.track:
                        self.track = self.track.split("?")[0]
                    self.dir = f"{MyPaths.csv_path}/{scrape_datetime:%Y-%m-%d %H.%M}/{self.artist}, {self.track}"
                    self.dir = check_ind_dir(self.dir, filters)
                except:
                    messagebox.showwarning(
                        "Filename Error",
                        f"Failed to extract track name from {url}, file numbered instead.",
                    )
                    self.dir = (
                        f"csv_exports/{scrape_datetime:%Y-%m-%d %H.%M}/url_{count}"
                    )
                    self.dir = check_ind_dir(self.dir, filters)
                # write data
                try:
                    os.makedirs(os.path.dirname(self.dir), exist_ok=True)
                    with open(
                        "{}".format(f"{self.dir}"),
                        "w",
                        encoding="utf-8",
                        newline="",
                    ) as csvfile:
                        self.writer = csv.writer(
                            csvfile,
                            dialect="excel",
                            delimiter=",",
                            quoting=csv.QUOTE_ALL,
                        )
                        self.writer.writerow(
                            ["comment", "timestamp", "datetime"]
                        )
                        for counter, comment in enumerate(self.comments_list):
                            # if counter == settings.max_num: break
                            self.writer.writerow(
                                [
                                    comment,
                                    self.timestamps_list[counter],
                                    self.datetimes_list[counter],
                                ]
                            )
                except:
                    messagebox.showerror(
                        "CSV Error", f"Failed to write {url} data to csv"
                    )
                    UI.print_data(
                        self.comments_list,
                        self.timestamps_list,
                        self.datetimes_list,
                    )
                
                # update progress bar
                self.progress_bar["value"] += 10 #csv writing

        # quit browser and write data to merged csv
        self.driver.quit()
        if settings.csv_merge:
            self.current_task.config(text="Writing all comments to CSV...")
            self.current_task.update()
            self.dir = f"csv_exports/{settings.csvfilename}"
            self.dir = check_merged_dir(self.dir)

            # write new data
            try:
                os.makedirs(os.path.dirname(self.dir), exist_ok=True)
                with open(
                    self.dir, "w", encoding="utf-8", newline=""
                ) as csvfile:
                    self.writer = csv.writer(
                        csvfile,
                        dialect="excel",
                        delimiter=",",
                        quoting=csv.QUOTE_ALL,
                    )
                    self.writer.writerow(
                        ["Comment", "Timestamp", "Datetime Posted"]
                    )
                    for count, comment in enumerate(self.comments_master_list):
                        self.writer.writerow(
                            [
                                comment,
                                self.timestamps_master_list[count],
                                self.datetimes_master_list[count],
                            ]
                        )
            except:
                messagebox.showerror(
                    "CSV Error", f"Failed to write {url} data to csv"
                )
                UI.print_data(
                    self.comments_master_list,
                    self.timestamps_master_list,
                    self.datetimes_master_list,
                )
        self.progress_bar["value"] = self.total_ops
        seconds = time.time() - scrape_start_time
        if seconds >= 60:
            min, sec = divmod(seconds, 60)
            self.current_task.config(
                text=f"Completed in {min:.0f} minutes and {sec:.2f} seconds"
            )
        else:
            self.current_task.config(
                text=f"Completed in {seconds:.2f} seconds"
            )
        self.current_task.update()

    def test(self, settings, url_input, filters):
        # url input
        print(f"URL list = {url_input.url_list}")
        print(f"Max urls = {url_input.url_max}")
        print(f"Parent url = {url_input.parent_url}")
        print(f"Artist = {url_input.artist}")

        # settings
        print(f"CSV Merge = {settings.csv_merge}")
        print(f"CSV Filename = {settings.csvfilename}")
        print(f"Maximum no. of urls = {settings.max_num}")
        print(f"Wait time = {settings.wait}")
        print(f"Headless = {settings.headless}")
        print(f"Folder = {settings.folder}")
        print(f"Extra scroll = {settings.extra_scroll}")
        print(f"Filtername = {filters.filtername}")
        print(f"Subtractive Filters = {filters.subtractive_filters}")
        print(f"Additive filters = {filters.additive_filters}")
        print(f"Just Emojis = {filters.just_emojis}")
        print(f"No filters = {filters.no_filters}")
        print("")

    @staticmethod
    def remove_emoji(txt):
        emoji_dict_list = emoji.emoji_list(txt)
        newtext = txt
        for emoji_dict in emoji_dict_list:
            newtext = newtext.replace("{}".format(emoji_dict["emoji"]), " ")
        return newtext


if __name__ == "__main__":

    class testfilters:
        def __init__(self):
            self.no_filters = False
            self.just_emojis = False
            self.additive_filters = []
            self.subtractive_filters = ["self.remove_emoji(text)"]
            self.filtername = ""

    class testsettings:
        def __init__(self):
            self.extra_scroll = 3
            self.folder = ""
            self.headless = True
            self.wait = 0.5
            self.max_num = 20
            self.csvfilename = "test.csv"
            self.csv_merge = True
            self.scroll = 5

    class testurlinput:
        def __init__(self):
            self.artist = False
            self.parent_url = ""
            self.url_max = 1
            self.url_list = [
                "https://soundcloud.com/headieone/headie-one-martins-sofa"
            ]

    testurls = testurlinput()
    testsets = testsettings()
    testfilts = testfilters()

    test = Scraper(testsets, tk.Tk(), 10)
    test.scrape(testurls, testsets, testfilts)
