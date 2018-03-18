class Page:
    def __init__(self):
        """clase basica de una pagina web"""
        self.domain = "X"
        self.url = "X"
        self.content = []

    def setDomain(self,dom):
        self.domain = dom

    def setUrl(self, url):
        self.url = url

    def setContent(self,words):
        self.content = words

    def getUrl(self):
        return self.url

    def getContent(self):
        return self.content

    def __str__(self):
        domain = self.domain
        url = self.url
        content = ','.join(self.content)
        return domain + " " + url + "\n" + content

