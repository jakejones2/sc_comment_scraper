class Filters:

    def __init__(self):

        self.subtractive_filters = []
        self.additive_filters = []
        self.just_emojis = False
        self.no_filters = False
        self.case_sensitive = False
        self.filtername = ''

        self.current_no_cfilter = ''
        self.current_only_cfilter = ''
        self.current_omit_cfilter = ''

        self.current_no_cbutton = False
        self.current_only_cbutton = False
        self.current_omit_cbutton = False

    
    def add_or_remove_filter(self, action, *args): #no need for remove?
        for arg in args:
            if arg == 'N':
                if action == 'add':
                    self.no_filters = True
                elif action == 'remove':
                    self.no_filters = False
            elif arg == 'JE':
                if action == 'add':
                    self.just_emojis = True
                elif action == 'remove':
                    self.just_emojis = False
            elif arg == 'NT':
                nt = '''re.sub("@\S*", "", text)'''
                if action == 'add':
                    self.subtractive_filters.append(nt)
                elif action == 'remove':
                    if nt in self.subtractive_filters:
                        self.subtractive_filters.remove(nt)
            elif arg == 'NR':
                nr = '''re.sub("@.*", "", text)'''
                if action == 'add':
                    self.subtractive_filters.append(nr)                 
                elif action == 'remove':
                    if nr in self.subtractive_filters:
                        self.subtractive_filters.remove(nr)
            elif arg == 'NS':
                ns = '''re.sub(".*@.*", "", text)'''
                if action == 'add':
                    self.subtractive_filters.append(ns)               
                elif action == 'remove':
                    if ns in self.subtractive_filters:
                        self.subtractive_filters.remove(ns)
            elif arg == 'NE':
                ne = '''self.remove_emoji(text)'''
                if action == 'add':
                    self.subtractive_filters.append(ne)
                elif action == 'remove':
                    if ne in self.subtractive_filters:
                        self.subtractive_filters.remove(ne)
            if not arg == 'N':
                if action == 'add':
                    self.filtername += f'{arg}, '
                elif action == 'remove':
                    self.filtername = self.filtername.replace(f'{arg}, ', '')

    def add_or_remove_cfilter(self, action, mode, string):
        words = string.split(',')
        self.filtername += f'{mode} {words}, '
        if mode == 'exclude':
            for word in words:
                filt=[]
                filt = f'''re.sub(".*{word}.*", "", text)'''
                if self.case_sensitive:
                    filt = filt.rstrip(')') + ''', flags=re.IGNORECASE)'''
                if action == 'add':
                    self.subtractive_filters.append(filt)
                elif action == 'remove':
                    if filt in self.subtractive_filters:
                        self.subtractive_filters.remove(filt)
        if mode == 'include':
            for word in words:
                filt = f'''re.search("{word}", text)'''
                if self.case_sensitive:
                    filt = filt.rstrip(')') + ''', flags=re.IGNORECASE)'''
                if action == 'add':
                    self.additive_filters.append(filt)
                elif action == 'remove':
                    if filt in self.additive_filters:
                        self.additive_filters.remove(filt)
        if mode == 'omit':
            for word in words:
                filt = f'''re.sub("{word}", "", text)'''
                if self.case_sensitive:
                    filt = filt.rstrip(')') + ''', flags=re.IGNORECASE)'''
                if action == 'add':
                    self.subtractive_filters.append(filt)
                elif action == 'remove':
                    if filt in self.subtractive_filters:
                        self.subtractive_filters.remove(filt)
    
    def clear_filters(self):
        self.subtractive_filters = []
        self.additive_filters = []
        self.filtername = ''