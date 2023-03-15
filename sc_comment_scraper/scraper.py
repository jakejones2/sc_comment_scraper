from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
import os
from datetime import datetime #check this one
import emoji
import re

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from config import Config
from backup_ui import UI
from check_dir import check_merged_dir, check_ind_dir

class Scraper(Config):
    
    def __init__(self, settings, start_frame, pd):
        super().__init__()

        #create widgets
        self.run_frame = ttk.Frame(start_frame,
                                   style='start.TFrame')
        
        self.style.configure('Horizontal.TProgressbar', 
                             troughcolor=self.tab_colour,
                             darkcolor=self.green,
                             lightcolor=self.other_blue,
                             background=self.green,
                             bordercolour=self.tab_colour)
        
        self.progress_bar = ttk.Progressbar(self.run_frame,
                                            length=pd*95,
                                            mode='determinate',
                                            orient=tk.HORIZONTAL,
                                            style='Horizontal.TProgressbar')
        self.progress_bar.grid(column=0, row=0, sticky='nw')

        self.style.configure('task.TLabel',
                             font=(self.font_light, 10),
                             foreground=self.text_colour,
                             background=self.background_colour)
        self.current_task = ttk.Label(self.run_frame,
                                      style='task.TLabel',
                                      text='Press start to begin scraping')
        self.current_task.grid(column=0, row=1, sticky='nw')

        #initialise headless chrome browser using driver manager
        try:
            self.current_task.config(text='Initialising Google Chrome driver...')
            self.options = Options()
            self.options.add_experimental_option("excludeSwitches", 
                                                    ["enable-logging"])
            prefs = {"profile.managed_default_content_settings.images": 2}
            self.options.add_experimental_option("prefs", prefs)
            if settings.headless:                                       
                self.options.add_argument('--headless')
                self.options.add_argument("--mute-audio")
            os.environ['WDM_PROGRESS_BAR'] = ''
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(path = r".\\Drivers").install()), options=self.options)
            self.current_task.config(text='Press start to begin scraping')
            
        except:
            messagebox.showerror('Scraping Error', 
                                 'Failed to initialise Google Chrome driver') 
        
    def load_urls(self, url_input, settings):
        if url_input.parent_url:
            self.current_task.config(
                text='Retrieving tracks from artist or playlist...')
            try:
                self.driver.get(url_input.parent_url)
            except:
                messagebox.showerror('Scraping Error',
                                     'Failed to retrieve artist/playlist URL')
            if url_input.url_max < 10:
                self.track_scroll = 0
            else:
                self.track_scroll = round(
                    int(url_input.url_max) / 10)
            try:
                while True:
                    for n in range(self.track_scroll):
                        try:
                            self.driver.execute_script(
                                "window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(settings.wait)
                        except:
                            time.sleep(0.5)
                    if url_input.artist:
                        self.links = self.driver.find_elements(
                            By.CLASS_NAME, "soundTitle__title")
                    else:
                        self.links = self.driver.find_elements(
                            By.CLASS_NAME, "trackItem__trackTitle")
                    if len(self.links) >= url_input.url_max:
                        break
                for count, link in enumerate(self.links, start=1):
                    if count > url_input.url_max:
                        break
                    else:
                        url_input.url_list.append(link.get_attribute('href'))
            except:
                messagebox.showerror('Scraping Error',
                                     'Failed to find links on track/playlist URL')


    def scrape(self, url_input, settings, filters):
        self.start_time = time.time()
        self.dt = datetime.now()
        self.comments_master_list = []
        self.timestamps_master_list = []
        self.datetimes_master_list = []
        self.previous_comments = []

        self.total_comments = len(url_input.url_list) * settings.max_num
        self.total_ops = ((3 * settings.max_num * len(url_input.url_list)) + (20 * len(url_input.url_list)))
        self.progress_bar.config(maximum=self.total_ops)

        for count, url in enumerate(url_input.url_list, start=1):
            #try destroy widget here????? see what happens lol
            self.progress_bar['value'] = (self.current_ops_update() + ((count - 1) * 20))
            self.progress_bar.update()
            self.current_task.config(text=f'Retrieving {url}...')
            self.current_task.update()
            try:
                self.driver.get(url)
            except: 
                messagebox.showerror('Scraping Error', 
                                     f'Failed to retrieve {url}')
            
            #accept cookies
            if not settings.headless:
                time.sleep(settings.wait)
                try:
                    self.driver.find_element(
                        By.ID, "onetrust-accept-btn-handler").click()
                except:
                    pass
            
            #scroll the page
            self.progress_bar['value'] = (self.current_ops_update() + ((count - 1) * 20) + 10)
            self.progress_bar.update()
            self.current_task.config(
                text=f'Scrolling {url} and searching for comments')
            self.current_task.update()
            
            try:
                #initial scroll
                for n in range(settings.scroll):
                    try:
                        self.driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(settings.wait)
                        #stop the gui from 'not responding'
                        self.current_task.update()
                    except:
                        time.sleep(0.5)
                
                self.comments_list = []
                self.index_list = []
                self.comments_list_length = []
                self.comment_count = -1

                #comment-retrieving loop
                while True:
                    self.comments = self.driver.find_elements(
                        By.CLASS_NAME, "commentItem__body")
                    for n in range(len(self.comments)):
                        #ignore previously scanned comments
                        if n <= self.comment_count:
                            continue
                        #filters
                        elif filters.no_filters:
                            self.comments_list.append(self.comments[n].text)
                            #index comments that pass filtering
                            #saves time when finding timestamps and datetimes
                            self.index_list.append(n)
                            self.comment_count = n
                        elif filters.just_emojis:
                            self.emoji_dict_list = emoji.emoji_list(
                                self.comments[n].text)
                            for emoji_dict in self.emoji_dict_list:
                                self.comments_list.append(emoji_dict['emoji'])
                                self.index_list.append(n)
                                self.comment_count = n
                        else:
                            text = self.comments[n].text
                            self.index_list.append(n)
                            self.comment_count = n
                            if filters.subtractive_filters:
                                for x in filters.subtractive_filters:
                                    #evaluate the filter, usually reg ex
                                    text = eval(x).strip()
                                    #if fails, delete index
                                    if text: continue
                                    if n in self.index_list:
                                        self.index_list.remove(n)
                                if filters.additive_filters:
                                    for x in filters.additive_filters:
                                        #if search criteria not met
                                        if eval(x): continue
                                        text = ""
                                        if n in self.index_list:
                                            self.index_list.remove(n)
                                #if passed both add/sub filters
                                self.comments_list.append(text)
                                #prevent gui from 'not responding'
                                self.current_task.update()
                    #removing empty strings
                    self.comments_list = [x for x in self.comments_list if x.strip()]
                    #halting if no new comments found in extra scroll
                    if self.previous_comments == len(self.comments): break
                    self.previous_comments = len(self.comments)
                    #ensuring max_num
                    if len(self.comments_list) >= settings.max_num:
                        self.comments_list = self.comments_list[:settings.max_num]
                        self.index_list = self.index_list[:settings.max_num] 
                        break
                    #extra scrolls if max_num not hit
                    for n in range(settings.extra_scroll):
                        try:
                            self.driver.execute_script(
                                "window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(settings.wait)
                        except:
                            time.sleep(0.5)
                #append final comments list to master
                for c in self.comments_list:
                    self.comments_master_list.append(c)
            except:
                messagebox.showerror('Scraping Error', 
                                     f'Failed to retrieve comments from {url}')
            
            #find all timestamps
            self.progress_bar['value'] = (self.current_ops_update() + ((count - 1) * 20) + 10)
            self.progress_bar.update()
            self.current_task.config(
                text=f'Retrieving timestamps from {url}')
            self.current_task.update()
            try:
                self.timestamps = self.driver.find_elements(
                    By.CLASS_NAME, "commentItem__timestampLink")
                self.timestamps_list = []
                for t in range(len(self.timestamps)):
                    if t in self.index_list:
                        self.timestamps_list.append(
                            self.timestamps[t].text)
                        self.timestamps_master_list.append(
                            self.timestamps[t].text)
            except:
                messagebox.showerror('Scraping Error', 
                                     f'Failed to find timestamps in {url} HTML')

            #find all dates posted
            self.progress_bar['value'] = (self.current_ops_update() + ((count - 1) * 20) + 10)
            self.progress_bar.update()
            self.current_task.config(
                text=f'Retrieving datetimes from {url}')
            self.current_task.update()
            try:
                self.dates = self.driver.find_elements(
                    By.CLASS_NAME, "relativeTime")
                self.datetimes_list = []
                for d in range(len(self.dates)):
                    if d in self.index_list:
                        self.datetimes_list.append(
                            self.dates[d].get_attribute('datetime'))
                        self.datetimes_master_list.append(
                            self.dates[d].get_attribute('datetime'))
            except:
                messagebox.showerror('Scraping Error', f'Failed to find datetimes in {url} HTML')

            #write data to individual csv
            self.progress_bar['value'] = (self.current_ops_update() + ((count - 1) * 20) + 9)
            self.progress_bar.update()
            if not settings.csv_merge:
                # extract title name from url and apply filtername
                # placing in csv_exports folder via relative path
                self.current_task.config(
                    text=f'Writing {url} comments to CSV')
                self.current_task.update()
                try:
                    self.track = url.split('/')[-1]
                    self.artist = url.split('/')[-2]
                    if '?' in self.track:
                        self.track = self.track.split('?')[0]
                    self.dir = f"csv_exports/{self.dt:%Y-%m-%d %H.%M}/{self.artist}, {self.track}"
                    self.dir = check_ind_dir(self.dir, filters)
                except:
                    messagebox.showwarning('Filename Error', 
                                         f'Failed to extract track name from {url}, file numbered instead.')
                    self.dir = (f"csv_exports/{self.dt:%Y-%m-%d %H.%M}/url_{count}")
                    self.dir = check_ind_dir(self.dir, filters)
                # write data 
                try:
                    os.makedirs(os.path.dirname(self.dir), exist_ok=True)
                    with open('{}'.format(f"{self.dir}.csv"), 
                              'w', 
                              encoding='utf-8', 
                              newline='') as csvfile:
                        self.writer = csv.writer(csvfile, 
                                                 dialect='excel', 
                                                 delimiter=',', 
                                                 quoting=csv.QUOTE_ALL)
                        self.writer.writerow(['comment',
                                              'timestamp',
                                              'datetime'])
                        for counter, comment in enumerate(self.comments_list):
                            #if counter == settings.max_num: break
                            self.writer.writerow([comment, 
                                             self.timestamps_list[counter], 
                                             self.datetimes_list[counter]])           
                except:
                    messagebox.showerror('CSV Error', 
                                         f'Failed to write {url} data to csv')
                    UI.print_data(self.comments_list, 
                                  self.timestamps_list, 
                                  self.datetimes_list)
                    
                    
        #quit browser and write data to merged csv
        self.driver.quit()
        if settings.csv_merge:
            self.progress_bar['value'] = (self.current_ops_update() + ((count - 1) *20) + 19)
            self.current_task.config(
                text='Writing comments to CSV')
            self.current_task.update()
            self.dir = f"csv_exports/{settings.csvfilename}"
            self.dir = check_merged_dir(self.dir)

            #write new data
            try:
                os.makedirs(os.path.dirname(self.dir), exist_ok=True)
                with open(self.dir, 'w', encoding='utf-8', newline='') as csvfile:
                    self.writer = csv.writer(csvfile, 
                                            dialect='excel', 
                                            delimiter=',', 
                                            quoting=csv.QUOTE_ALL)
                    self.writer.writerow(['Comment',
                                          'Timestamp',
                                          'Datetime Posted'])
                    for count, comment in enumerate(self.comments_master_list):
                        self.writer.writerow([comment, 
                                                self.timestamps_master_list[count], 
                                                self.datetimes_master_list[count]])         
            except:
                messagebox.showerror('CSV Error', 
                                        f'Failed to write {url} data to csv')
                UI.print_data(self.comments_master_list, 
                                self.timestamps_master_list, 
                                self.datetimes_master_list)
        self.progress_bar['value'] = (self.total_ops)
        self.current_task.config(
            text='Completed in %s seconds' % (round(time.time() - self.start_time, 2)))
        self.current_task.update()
        
                
    def current_ops_update(self):
        self.current_ops = len(self.comments_master_list) + len(self.timestamps_master_list) + len(self.datetimes_master_list)
        return self.current_ops

    def test(self, settings, url_input, filters):

        #url input
        print(f'URL list = {url_input.url_list}')
        print(f'Max urls = {url_input.url_max}')
        print(f'Parent url = {url_input.parent_url}')
        print(f'Artist = {url_input.artist}')

        #settings
        print(f'CSV Merge = {settings.csv_merge}')
        print(f'CSV Filename = {settings.csvfilename}')
        print(f'Maximum no. of urls = {settings.max_num}')
        print(f'Wait time = {settings.wait}')
        print(f'Headless = {settings.headless}')
        print(f'Folder = {settings.folder}')
        print(f'Extra scroll = {settings.extra_scroll}')
        print(f'Filtername = {filters.filtername}')
        print(f'Subtractive Filters = {filters.subtractive_filters}')
        print(f'Additive filters = {filters.additive_filters}')
        print(f'Just Emojis = {filters.just_emojis}')
        print(f'No filters = {filters.no_filters}')
        print('')

    @staticmethod
    def remove_emoji(txt):
        emoji_dict_list = emoji.emoji_list(txt)
        newtext = txt
        for emoji_dict in emoji_dict_list:
            newtext = newtext.replace('{}'.format(emoji_dict['emoji']), ' ')
        return newtext


if __name__ == '__main__':

    class testfilters:
        def __init__(self):
            self.no_filters = False
            self.just_emojis = False
            self.additive_filters = []
            self.subtractive_filters = ['self.remove_emoji(text)']
            self.filtername = ''
    
    class testsettings:
        def __init__(self):
            self.extra_scroll = 3
            self.folder = ''
            self.headless = True
            self.wait = 0.5
            self.max_num = 20
            self.csvfilename = 'test.csv'
            self.csv_merge = True
            self.scroll = 5
    
    class testurlinput:

        def __init__(self):
            self.artist = False
            self.parent_url = ''
            self.url_max = 1
            self.url_list = ['https://soundcloud.com/headieone/headie-one-martins-sofa']

    testurls = testurlinput()
    testsets = testsettings()
    testfilts = testfilters()
         
    test = Scraper(testsets, tk.Tk(), 10)
    test.scrape(testurls, testsets, testfilts)