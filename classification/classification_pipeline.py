from typing import List

from configuration.classification_config import Classification_Config as Config
from classify.classification import Classification
from classify.xgb_classification import Xgb_Classification
from data_classes.data_reader import Data_Reader
from data_classes.patient import Patient
from data.data import Data
from publish.publisher import Publisher


class Classification_Pipeline:
    def __init__(self):
        self.patients: List[Patient] = []
        self.data: Data or None = None
        self.classification: Classification or None = None
        self.publisher: Publisher or None = None

    def fetch_patients(self):
        data_reader = Data_Reader(raw_data_path=Config.RAW_DATA_PATH)
        self.patients = data_reader.patients

    def calc_data(self):
        self.data = Data(patients=self.patients)

    def run_general_classification(self):
        self.classification = Classification(data=self.data)

    def run_xgb_classification(self):
        self.classification = Xgb_Classification(data=self.data)

    def publish(self):
        self.publisher = Publisher(classification=self.classification)
