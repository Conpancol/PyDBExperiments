import os
import importlib.util

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location("Material", BASE_DIR + '\common\Materials.py')
common_material = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common_material)


class ExtMaterials(common_material.Material):
    """Extended material class"""
    def __init__(self, material):
        super().__init__()
        self.orderNumber = "1"
        self.unit = "EA"
        self.quantity = 1.0
        self.setItemCode(material.getItemCode())

    def setOrderNumber(self, orderNum):
        self.orderNumber = orderNum

    def setUnit(self, unit):
        self.unit = unit

    def setQuantity(self, quantity):
        self.quantity = quantity

