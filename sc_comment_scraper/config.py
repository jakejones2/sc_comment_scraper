from tkinter import ttk

class Config:

    '''Colours, fonts, and styles for ttk widgets.'''

    #colours
    tab_colour = '#2E3349'#blue/gray
    tab_colour2 = '#40465E' #lighter blue/gray
    tab_colour3 = '#292E45' #darker blue/gray
    background_colour = '#181E36'#darker blue/gray
    text_colour = '#E3E2E7' #light gray/white
    heading_colour = '#027EF9'#bright blue
    light_gray = '#E7E9F3' #light gray
    other_blue = '#1D4498'
    dark_colour = '#01274E'
    green = '#36ba8c'

    #fonts
    font_bold = 'Segoe UI Semibold'
    font_light = 'Segoe UI Semilight'


    #styles
    def __init__(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
    
        self.style.configure("TFrame", 
                        background=self.background_colour)
        self.style.configure("start.TFrame", 
                        background=self.background_colour)
        self.style.configure("TLabel", 
                        foreground=self.text_colour, 
                        background=self.tab_colour, 
                        font=(self.font_bold, '11'))
        self.style.configure("tab2.TLabel", 
                        foreground=self.text_colour, 
                        background=self.tab_colour2, 
                        font=(self.font_bold, '11'))
        self.style.configure('small.TLabel', 
                        foreground=self.text_colour,
                        background=self.tab_colour, 
                        font=(self.font_light, '10'))
        self.style.configure('tab2.small.TLabel', 
                        foreground=self.text_colour,
                        background=self.tab_colour2, 
                        font=(self.font_light, '10'))
        self.style.configure('TEntry', 
                        foreground='black',  
                        font=(self.font_light, '9'))
        self.style.configure('internal.TButton', 
                        foreground=self.text_colour, 
                        background=self.background_colour, 
                        font=(self.font_light, '9'))
        self.style.map('internal.TButton',
                        foreground=[('hover', 'black')])
        self.style.configure('internal2.TButton', 
                        foreground=self.text_colour, 
                        background=self.tab_colour, 
                        font=(self.font_light, '9'))
        self.style.map('internal2.TButton',
                        foreground=[('hover', 'black')])
        self.style.configure('inner.TFrame', 
                             background=self.tab_colour)
        self.style.configure('sub.TLabel', 
                             foreground=self.text_colour, 
                             background=self.tab_colour, 
                             font=(self.font_bold, '11'))
        self.style.configure('sub2.TLabel', 
                             foreground=self.text_colour, 
                             background=self.tab_colour2, 
                             font=(self.font_bold, '11'))
        self.style.configure('TRadiobutton', 
                             foreground=self.text_colour, 
                             background=self.tab_colour, 
                             font=(self.font_light, '10'))
        self.style.map('TRadiobutton', 
                       foreground=[('hover', 'white')], 
                       background=[('hover', self.tab_colour)], 
                       indicatorcolor=[('selected', self.heading_colour)])
        self.style.configure('tab2.TRadiobutton', 
                             foreground=self.text_colour, 
                             background=self.tab_colour2, 
                             font=(self.font_light, '10'))
        self.style.map('tab2.TRadiobutton', 
                       foreground=[('hover', 'white')], 
                       background=[('hover', self.tab_colour2)], 
                       indicatorcolor=[('selected', self.heading_colour)])
        self.style.configure('tab2.TCheckbutton',
                             foreground=self.text_colour,
                             background=self.tab_colour2,
                             font=(self.font_light, '10'))
        self.style.map('tab2.TCheckbutton', 
                       foreground=[('hover', 'white')], 
                       background=[('hover', self.tab_colour2)], 
                       indicatorcolor=[('selected', self.heading_colour)])
        self.style.configure('popup.small.TLabel', 
                        foreground=self.text_colour,
                        background=self.background_colour, 
                        font=(self.font_light, '10'))
        self.style.configure('popup.TCheckbutton',
                             foreground=self.text_colour,
                             background=self.background_colour,
                             font=(self.font_light, '10'))
        self.style.map('popup.TCheckbutton', 
                       foreground=[('hover', 'white')], 
                       background=[('hover', self.background_colour)], 
                       indicatorcolor=[('selected', self.heading_colour)])
        self.style.configure('filters.TCheckbutton',
                             foreground=self.text_colour,
                             background=self.tab_colour2,
                             font=(self.font_light, '10'))
        self.style.map('filters.TCheckbutton', 
                       foreground=[('hover', 'white'), ('disabled', 'gray')], 
                       background=[('hover', self.tab_colour2)], 
                       indicatorcolor=[('selected', self.heading_colour), ('disabled', 'gray')])
        
    @staticmethod
    def grid_configure(master, *args):
        for arg in args:
            if 'c' in arg:
                lst = arg.lstrip('c').split('w')
                master.columnconfigure(lst[0], weight=lst[1])
            elif 'r' in arg:
                lst = arg.lstrip('r').split('w')
                master.rowconfigure(lst[0], weight=lst[1])
            else:
                master.errorlog.append(
                    'func grid_configure: Incorrect grid parameter')

    def clear_widgets(self):
        try:
            for widget in self.widget_list:
                widget.destroy()
            self.widget_list = []
        except:
            self.errorlog.append(
                'func claer_widgets: Failed to destroy widget(s)')