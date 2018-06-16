import csv
import datetime
import logging
import os
import importlib.util

from .RequestForQuotes import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__).rsplit('\\', maxsplit=1)[0]))

spec = importlib.util.spec_from_file_location("Material", BASE_DIR + '\common\Materials.py')
common_material = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common_material)

spec = importlib.util.spec_from_file_location("ExtMaterial", BASE_DIR + '\common\ExtMaterials.py')
common_ext = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common_ext)


class RFQCreator:
    """clase para crear RFQs"""
    def __init__(self):
        self.rfq = RequestForQuotes()
        logging.basicConfig(filename='logs/rfqcreator.log', level=logging.DEBUG)

    def setRFQInformation(self, internalCode, externalCode, sender, company, receivedDate):
        self.rfq.setIntenalCode(internalCode)
        self.rfq.setExternalCode(externalCode)
        self.rfq.setSender(sender)
        self.rfq.setCompany(company)
        self.rfq.setReceivedDate(receivedDate)
        dt = datetime.datetime.now()
        self.rfq.setProcessedDate(dt.strftime('%d/%m/%Y'))

    def addRFQNote(self, note):
        self.rfq.setNote(note)

    def createRFQfromCSV(self, csvfile):
        try:
            with open(csvfile, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, dialect="excel-tab")
                extmaterials = []
                for row in reader:
                    try:
                        orderNum = row[0]
                        itemCode = row[1]
                        quantity = float(row[2])
                        unit = row[3]
                        material = common_material.Material()
                        material.setItemCode(itemCode)
                        extendedMaterial = common_ext.ExtMaterials(material)
                        extendedMaterial.setOrderNumber(orderNum)
                        extendedMaterial.setUnit(unit)
                        extendedMaterial.setQuantity(quantity)
                        extmaterials.append(extendedMaterial)

                    except ValueError:
                        logging.info('There is a wrong data format entry. Please check')
                        continue

                self.rfq.setMaterialList(extmaterials)

            rfq_json = self.rfq.__dict__
            rfq_json['materialList'] = self.rfq.to_json()

            total_materials = len(rfq_json['materialList'])
            logging.info('End of RFQ creation  \t' + str(total_materials))

            return rfq_json

        except IOError as error:
            print(error)
