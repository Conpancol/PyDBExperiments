from CountryData import Country
from CountryData import Data
from pymongo import MongoClient
from Utilities import *
import csv
import copy

client = MongoClient('localhost', 27017)
db = client.conpancol
collection = db.gtcomex
result = collection.delete_many({})

# with open('test_file.txt', 'rb') as csvfile:

def dbWriter( infile, tp, yr) :

    with open(infile, 'rb') as csvfile:

        csvreader = csv.reader(csvfile, delimiter='\t')
        cdata = Country()
        cdata.setYear(yr)
        cdata.setType(tp)
        nCountry = 0

        for row in csvreader:
            if len(row) != 5:
                print 'wrong info data length', len(row)
            else:
                if row[0] != '':
                    country = row[0]
                    if country != cdata.getName():
                        nCountry += 1
                        if nCountry > 1:
                            try:
                                ob1 = cdata.__dict__
                                ob1['data'] = cdata.to_jason()
                                output = copy.deepcopy(ob1)
                                convert2unicode(output)
                                obj_id = collection.insert_one(output)
                            except Exception as inst:
                                print(type(inst))
                                print(inst.args)
                                print(inst)
                                print "problem", nCountry
                            cdata.reset()
                        cdata.setName(country)

                    # extract this info from this row
                    data = Data()
                    data.setDescription(row[1])
                    data.setPartida(row[2])
                    data.setTotalUSD(getValue(row[3]))
                    data.setTotalVol(getValue(row[4]))
                    cdata.addData(data)
                else:
                    data = Data()
                    data.setDescription(row[1])
                    data.setPartida(row[2])
                    data.setTotalUSD(getValue(row[3]))
                    data.setTotalVol(getValue(row[4]))
                    cdata.addData(data)

        ob1 = cdata.__dict__
        ob1['data'] = cdata.to_jason()
        output = copy.deepcopy(ob1)
        convert2unicode(output)
        #print json.dumps(ob1, indent=2)
        obj_id = collection.insert_one(output)

    print nCountry

list_files = []
list_files.append("data/01_Impo-Origen_51_2014_Totals.txt")
list_files.append("data/01_Impo-Origen_51_2015_Totals.txt")
list_files.append("data/01_Impo-Origen_51_2016_Totals.txt")
list_files.append("data/01_Impo-Origen_51_2017_Totals.txt")

for f in list_files:
    info = f.split('_')
    year = int(info[3])
    tp = info[1]
    print f, tp, year
    dbWriter(f, tp, year)


