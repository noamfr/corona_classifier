from typing import List

from data_classes.data_reader import Data_Reader
from data_classes.patient import Patient

from configuration.classification_config import Classification_Config
from data.data import Data


class Classification_Pipeline:
    def __init__(self):
        self.patients: List[Patient] = []
        self.data: Data = None

    def fetch_patients(self):
        data_reader = Data_Reader(raw_data_path=Classification_Config.RAW_DATA_PATH)
        self.patients = data_reader.get_patients()

    def data(self):
        self.data = Data(patients=self.patients)

    def classification(self):
        pass

    def publish(self):
        pass
