from CountryData import Country
from CountryData import Data
from pymongo import MongoClient
from Utilities import *
import csv
import json
import copy

client = MongoClient('localhost', 27017)
db = client.conpancol
collection = db.gtcomex

cursor = collection.find({"type": "Impo-Origen", "year" : 2017})

sulfonico = "290410"
acido = "280700"
lab = "3817001"


for doc in cursor:
    country = doc["country"]
    data = doc["data"]
    for dt in data:
        if dt["partida"].startswith(lab):
            results = country + '\t' + dt["partida"] + '\t' + str(dt["totalUSD"]) + '\t' + str(dt["totalVol"])
            print results






