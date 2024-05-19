import os
import json


FLAG_DATA_FILE = "flag.json"


class FlagData:
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        
        self.path: str = ""
        
        self.colors: list[str] = []
    
    def load_from_json(self, json_data: dict):
        self.name = json_data.get("name", self.id)
        
        self.colors = json_data.get("colors", [])
        
        # for the objectively wrong people
        #
        # this is a joke
        if len(self.colors) == 0:
            self.colors = json_data.get("colours", [])


def get_data_from_dir(directory: str) -> list[FlagData]:
    flags = {}
    
    for flag_folder in os.listdir(directory):
        full_path = os.path.join(directory, flag_folder)
        if not os.path.isdir(full_path):
            continue
        
        flag_data = FlagData()
        flag_data.id = flag_folder
        flag_data.path = full_path
        
        # look for flag data file
        data_file_path = os.path.join(full_path, FLAG_DATA_FILE)
        if os.path.exists(data_file_path):
            json_file = open(data_file_path)
            json_data = json.load(json_file)
            
            flag_data.load_from_json(json_data)
        
        flags[flag_data.id] = flag_data
    
    return flags