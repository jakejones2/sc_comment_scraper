class Settings:

    def __init__(self):
        self.csv_merge = False
        self.csvfilename = ''
        self.max_num = 100
        self.wait = 0.5
        self.headless = True
        self.scroll = 10
        self.extra_scroll = 3

    #initial scroll
    def estimate_scroll(self):
        if self.max_num <= 10:
            self.scroll = 1
            self.extra_scroll = 1
        elif self.max_num >= 10000:
            self.scroll = 500
            self.extra_scroll = 125
        else:
            self.scroll = round(self.max_num / 10)
            self.extra_scroll = round(self.scroll / 4)

    def check_csvfilename(self):
        if self.csvfilename[-4] == '.csv':
            pass
        else:
            self.csvfilename += '.csv'
        