class UrlInput:
    def __init__(self):
        self.url_list = []
        self.url_max = 10
        self.parent_url = ""
        self.artist = False

    def add_url_file(self, filename):
        try:
            with open(f"{filename}") as fh:
                for line in fh:
                    self.url_list.append(line.strip())
                self.url_list = [x for x in self.url_list if x.strip()]
        except:
            try:
                with open(f"{filename}.txt") as fh:
                    for line in fh:
                        self.url_list.append(line.strip())
                    self.url_list = [x for x in self.url_list if x.strip()]
            except:
                return "Invalid file"
