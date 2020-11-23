from typing import List

from configuration.classification_config import Classification_Config as Config
from classify.classifier import Classifier
from data_classes.data_reader import Data_Reader
from data_classes.patient import Patient
from data.data import Data
from publish.publisher import Publisher


class Classification_Pipeline:
    def __init__(self):
        self.patients: List[Patient] = []
        self.data: Data or None = None
        self.classifier: Classifier or None = None
        self.publisher: Publisher or None = None

    def fetch_patients(self):
        data_reader = Data_Reader(raw_data_path=Config.RAW_DATA_PATH)
        self.patients = data_reader.get_patients()

    def calc_data(self):
        self.data = Data(patients=self.patients)

    def run_classification(self):
        self.classifier = Classifier(data=self.data)

    def publish(self):
        self.publisher = Publisher(classifier=self.classifier)
