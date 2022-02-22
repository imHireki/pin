from typing import List, Dict, Union
import json
import os.path


class JsonFile:
    """ Deal with the storage using a Json file """

    def __init__(self, filename:str):
        self.filename = filename

    def insert(self, data:Dict[str, Union[str, list]]):
        """ Append the data to `self.filename` """

        json_data = self.select()
        json_data.update(data)

        json_file = open(self.filename, 'w')
        json.dump(obj=json_data, fp=json_file, indent=4)
        json_file.close()

    def select(self) -> Dict[str, Union[str, list]]:
        """ Return all the data from the `self.filename` file """

        if not os.path.exists(self.filename):
            return {}  # the file is created just on insert()

        json_file = open(self.filename, 'r')
        json_data = json.load(json_file)
        json_file.close()
        return json_data