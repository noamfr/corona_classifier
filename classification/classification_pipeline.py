from typing import List

from data_analysis.data.data_reader import Data_Reader
from data_analysis.data.patient import Patient

from .data.data import Data


class Classification_Pipeline:
    def __init__(self):
        self.patients: List[Patient] = []
        self.data: Data = None

    def fetch_patients(self):
        self.patients = Data_Reader.get_patients()

    def data(self):
        self.data = Data(patients=self.patients)

    def classification(self):
        pass

    def publish(self):
        pass
