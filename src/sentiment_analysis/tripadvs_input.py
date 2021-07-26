import csv
from pathlib import Path

from .input_data import InputData


class TripAdvisorFile(InputData):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path: Path = path
        self.read_csv_file()
        self.ids: list[int] = []

    def read_csv_file(self) -> None:
        data: list[str] = []
        ids: list[int] = []
        if not (self.path.is_file and self.path.suffix == '.csv'):
            raise Exception("Provide a valid path to a csv file")
        with open(self.path, 'r') as file:
            csv_data = csv.reader(file,
                                  delimiter=',',
                                  strict=True,
                                  skipinitialspace=True)
            for row in csv_data:
                d = ' '.join(row[3:]).strip().removesuffix('******')
                data.append(d)
                #print(row, csv_data.line_num)
                ids.append(int(row[0]))
        self.data = data
        self.ids = ids
