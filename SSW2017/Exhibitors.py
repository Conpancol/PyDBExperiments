class Exhibitor:
    def __init__(self):
        """clase basica de un expositor en SSW"""
        self.name = "X"
        self.country = "XX"
        self.url = "XX"

    def setName(self,name):
        self.name = name

    def setCountry(self,country):
        self.country = country

    def setUrl(self,www):
        self.url = www

    def getName(self):
        return self.name

    def getCountry(self):
        return self.country

    def getUrl(self):
        return self.url


