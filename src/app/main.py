import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import ctypes
from app.gui.config import Config
import os
from app.gui.scraping_frame import ScrapingFrame
from app.gui.da_frame import DAFrame
from app.backend.url_input import UrlInput
from app.backend.settings import Settings
from app.backend.filters import Filters

class MainWindow(Config):

    def __init__(self, master, dpi, scaling, pd):
        super().__init__()

        '''Window geometry and scaled images. 
            
            MainGUI boots up with arguments 'dpi', 'scaling', and 'uhd' 
            all set at 0. If the UHD button is pressed, the MainGUI tk.root 
            is destroyed, and a new instance of the MainGUI class is created 
            with new 'scaling', 'dpi' and 'uhd' values. The 'pd' (padding) 
            argument is also increased to maintain the appearance of the 
            new UHD window. '''
        
        #main window
        self.master = master
        self.master.configure(background=self.background_colour)
        self.master.title(' Soundcloud Data Tools v1.5')
        self.icon = ImageTk.PhotoImage(Image.open(self.icon_path))
        self.master.iconphoto(False, self.icon)
        self.widget_list = []
 
        
        MainWindow.grid_configure(self.master, 'c1w1', 'r1w1')

        def resize_screen():
            self.master.destroy()
            start_app_uhd()

        if dpi > 0:
            ctypes.windll.shcore.SetProcessDpiAwareness(dpi)
            self.master.tk.call('tk', 'scaling', scaling)
            self.master.geometry('2700x1500')
            self.img1 = ImageTk.PhotoImage(Image.open(self.tab1b_path))
            self.img2 = ImageTk.PhotoImage(Image.open(self.tab2b_path))
        else:
            self.master.geometry('1100x700')
            self.img1 = ImageTk.PhotoImage(Image.open(self.tab1s_path))
            self.img2 = ImageTk.PhotoImage(Image.open(self.tab2s_path))
            self.style.configure('uhd.TButton', 
                                 foreground=self.text_colour, 
                                 background=self.tab_colour, 
                                 relief=0, 
                                 font=(self.font_light, '9'))
            self.style.map('uhd.TButton', 
                           foreground = [('active', '!disabled', 'black')])
            self.uhd_button = ttk.Button(self.master, 
                                         text="Restart in UHD mode", 
                                         style='uhd.TButton', 
                                         command=resize_screen)
            self.uhd_button.grid(row=0, 
                                 column=1, 
                                 padx=pd, 
                                 pady=pd, 
                                 sticky='ne')


        #title banner
        self.style.configure("title.TLabel", 
                             foreground=self.heading_colour, 
                             background=self.background_colour, 
                             font=(self.font_bold, '24'))
        self.title = ttk.Label(self.master, 
                               text='SoundCloud Data Tools v1.5', 
                               style="title.TLabel") 
        self.title.grid(row=0, column=0, sticky='nw', pady=pd/2, padx=pd)


        #create notebook
        self.style.theme_settings('default', 
                                  {"TNotebook.Tab": 
                                  {"configure": 
                                  {"padding": [pd, 0]}}})
        self.style.configure("TNotebook", 
                             background=self.background_colour, 
                             borderwidth=0, 
                             highlightwidth=0)
        self.style.configure("TNotebook.Tab", 
                             foreground=self.text_colour, 
                             background=self.background_colour, 
                             font=(self.font_light, '11'), 
                             borderwidth=0, 
                             focuscolor=self.background_colour)
        self.style.map("TNotebook.Tab", 
                       background= [("selected", self.tab_colour)], 
                       focuscolor= [("selected", self.tab_colour)], 
                       expand=[("selected", 1), ("hover", 1)], 
                       foreground=[('hover', 'white')])        
        self.nb = ttk.Notebook(self.master, 
                               style="TNotebook", 
                               padding=[pd, pd, pd, pd])
        self.nb.grid(row=1, column=0, columnspan=2, sticky='nesw')

        #linking to backend
        self.url_input = UrlInput()
        self.settings = Settings()
        self.filters = Filters()

        #creating scraping frames and inner frames
        self.scr_frame = ScrapingFrame(self.nb, 
                                       pd, 
                                       master=master, 
                                       url_input=self.url_input,
                                       settings=self.settings,
                                       filters=self.filters).scr_frame
        self.da_frame = DAFrame(self.nb, pd).da_frame

        #add scraping and data analysis frames to notebook
        self.nb.add(self.scr_frame, 
                    text='Comment Scraper ', 
                    image=self.img1, 
                    compound=tk.RIGHT,)
        self.nb.add(self.da_frame, 
                    text='Data Clean-Up and Analysis ', 
                    image=self.img2, 
                    compound=tk.RIGHT)

def start_app(): 
    root = tk.Tk() 
    app = MainWindow(master=root, dpi=0, scaling=0, pd=10)
    app.master.mainloop()

def start_app_uhd():
    root = tk.Tk()
    app = MainWindow(master=root, dpi=2, scaling=3, pd=24)
    app.master.mainloop() 

if __name__ == '__main__':
    start_app()