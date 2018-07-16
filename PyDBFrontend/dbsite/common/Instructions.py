import json


class Instructions:
    """Instrucciones de la funcionalidad de la apliacion"""
    def __init__(self, app, view):
        self.locale = "es_CO"
        self.app = app
        self.view = view
        self.resource = "resources/instructions/" + app + '.' + self.locale + '.json'

        json_data = open(self.resource,encoding='utf8').read()
        data = json.loads(json_data)
        self.title = data[self.view]['title']
        self.steps = data[self.view]['steps']
        print(self.title)
        for key,value in self.steps.items():
            print(self.steps[key])


