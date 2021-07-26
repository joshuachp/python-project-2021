import json
from pathlib import Path
from .input_data import InputData


class AmazonJsonFile(InputData):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path: Path = path
        self.read_json_file()

    def read_json_file(self) -> None:
        if not self.path.is_file and self.path.suffix != '.json':
            raise Exception("Provide a valid path to a json file")
        with open(self.path, 'r') as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise Exception(
                "Error in json schema, it should be an array of objects")
        for review in data:
            if not isinstance(review, dict):
                raise Exception(
                    "Error in json schema, it should be an array of objects")
            if not ('text' in review and isinstance(review['text'], str)):
                raise Exception("Error in json schema, missing text field")
            self.data.append(review['text'])
