from typing import List, Dict

from .data_reader import Data_Reader
from .vector_builder import Vector_Builder
from .patient import Patient
from .data_fields import Data_Fields


class Data:
    def __init__(self):
        self.patients: List[Patient] = []
        self.vectors: Dict = {}

        self.__calc()

    def __calc(self):
        self.__get_patients()
        self.__one_hot_encoding()
        self.__build_vectors()

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

    def __build_vectors(self):
        self.__build_target_vector()
        self.__build_binary_vectors()
        self.__build_continuous_vectors()

    def __build_target_vector(self):
        vector_builder = Vector_Builder(data_object_list=self.patients,
                                        data_fields=Data_Fields.get_target(),
                                        array_type=int)

        self.vectors['target'] = vector_builder.analysis_vectors

    def __build_binary_vectors(self):
        vector_builder = Vector_Builder(data_object_list=self.patients,
                                        data_fields=Data_Fields.get_binary_vars(),
                                        array_type=int)

        self.vectors['binary_vectors'] = vector_builder.analysis_vectors

    def __build_continuous_vectors(self):
        vector_builder = Vector_Builder(data_object_list=self.patients,
                                        data_fields=Data_Fields.get_continuous_vars(),
                                        array_type=float)

        self.vectors['continuous_vectors'] = vector_builder.analysis_vectors
