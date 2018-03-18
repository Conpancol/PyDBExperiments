import json

class Data:
    def __init__(self):
        """Datos - impo expo"""
        self.description = "X"
        self.partida = "X"
        self.totalUSD = 0.0
        self.totalVol = 0.0

    def setDescription(self, desc):
        self.description = desc

    def setPartida(self, partida):
        self.partida = partida

    def setTotalUSD(self, usd):
        self.totalUSD = usd

    def setTotalVol(self, vol):
        self.totalVol = vol

    def getPartida(self):
        return self.partida

class Country:
    def __init__(self):
        """Clase para guardar la informacion disponible por pais"""
        self.country = "X"
        self.data = []
        self.year = 1900
        self.type = "Impo"

    def setName(self,name):
        self.country = name

    def addData(self,data):
        self.data.append(data)

    def setYear(self,year):
        self.year = year

    def setType(self,type):
        self.type = type

    def reset(self):
        self.data = []

    def getName(self):
        return self.country

    def __str__(self):
        name = self.country
        partidas = []
        for dt in self.data:
            partidas.append(dt.getPartida())
        outpartidas = ','.join(partidas)
        return name + '\n' + outpartidas

    def to_jason(self):
        obj_list = [ob.__dict__ for ob in self.data]
        return obj_list

