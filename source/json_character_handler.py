import json

class JsonCharacterHandler:
    def __init__(self, file):
        self.data = {}
        self.file = file
        self.load_data(self.file)

    def load_data(self, file):
        """Funcion que carga los datos del json"""
        with open(file) as json_file:
            self.data = json.load(json_file)

    def get_stats_by_name(self, name):
        return self.data[name.lower() + "/" + name.lower() + "_front.png"]["STATS"]
    
    def get_character_by_name(self, name):
        return self.data[name.lower() + "/" + name.lower() + "_front.png"]
