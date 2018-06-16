import os
import importlib.util

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location("ExtMaterial", BASE_DIR + '\common\ExtMaterials.py')
common_material = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common_material)


class QuotedMaterials(common_material.ExtMaterials):
    """clase basica de materiales metalicos con cotizacion"""
    def __init__(self, material):
        super().__init__(material)
        self.theoreticalWeight = 0.00
        self.givenWeight = 0.00
        self.unitPrice = 0.00
        self.totalPrice = 0.00
        self.countryOrigin = "NA"
        self.note = "NA"

    def setTheoreticalWeight(self, theoWeight):
        self.theoreticalWeight = theoWeight

    def setGivenWeight(self, givenWeight):
        self.givenWeight = givenWeight

    def setUnitPrice(self, unitPrice):
        self.unitPrice = unitPrice

    def setTotalPrice(self, total):
        self.totalPrice = total

    def setNote(self, note):
        self.note = note

    def setCountryOrigin(self, country):
        self.countryOrigin = country
