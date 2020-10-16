from typing import List

from .data_reader import Data_Reader
from .patient import Patient
from .data_fields import Data_Fields


class Data:
    def __init__(self):
        self.patients: List[Patient] = []

        self.__get_patients()
        self.__one_hot_encoding()

    def __get_patients(self):
        data_reader = Data_Reader()
        self.patients = data_reader.get_patients()

    def __one_hot_encoding(self):
        binary_data_fields = Data_Fields.get_binary_vars()

        for patient in self.patients:
            for field in binary_data_fields:
                if getattr(patient, field) is None:
                    continue
                elif getattr(patient, field) not in ('TRUE', 'Positive'):
                    setattr(patient, field, 0)
                else:
                    setattr(patient, field, 1)
